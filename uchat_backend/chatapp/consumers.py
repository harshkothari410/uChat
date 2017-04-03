import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import ChatRoom

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.db.models import Q

from chatapp.models import ChatRoom, Message
from userapp.models import UserProfile


Room = ChatRoom
log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    


    print "Connect"
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(label=label)

    except ValueError:
        print "tets"
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        print "no room in channel_session"
        log.debug('ws room does not exist label=%s', label)
        return

    # log.debug('chat connect room=%s client=%s:%s', 
    #     room.label, message['client'][0], message['client'][1])

    print 'chat connect room=%s client=%s:%s', room.label, message['client'][0], message['client'][1]
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.label

    message.reply_channel.send({'text': 'hello'})

    print Group.__dict__

    print message.__dict__

@channel_session
def ws_receive(message):
    print "I am receiving"
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        print room
    except KeyError:
        log.debug('no room in channel_session')
        print "no room in channel_session"
        return
    except Room.DoesNotExist:
        print "room does not exist"
        log.debug('recieved message, buy room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        print "ws message isn't json text="
        log.debug("ws message isn't json text=%s", text)
        return
    
    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s', 
            room.label, data['handle'], data['message'])
        m = room.messages.create(**data)
        # print m
        # See above for the note about Group
        print data['message']
        if data['message'] == 'uchat':
            m = {
                'message': 'welcome to uchat',
                'handle': 'uChat'
            }
            print "Hello"
            Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m)})  

        if data['message'] == 'Hi':
            m = {
                'message': 'Hello, How may I help you today ?',
                'handle': 'uChat'
            }
            print "Hello"
            Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m)})    
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass

