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
from userapp.models import UserProfile, Friend

from chatapp.messageparse import bot_message

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
        print 'invalid ws path=%s', message['path']
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        print 'ws room does not exist label=%s', label
        log.debug('ws room does not exist label=%s', label)
        return

    # log.debug('chat connect room=%s client=%s:%s', 
    #     room.label, message['client'][0], message['client'][1])

    print 'chat connect room=%s client=%s:%s', room.label, message['client'][0], message['client'][1]
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

    # message.channel_session['room'] = {'main': room.label}
    message.channel_session['room'] = room.label

    message.reply_channel.send({'text': 'hello'})

@channel_session
def ws_receive(message):
    print "I am receiving"
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)

        # Add bot channel for bot the user 
        room_friend_record = Friend.objects.filter(room=room)

        flag = 0
        if len(room_friend_record) == 2:
            flag = 1
            # creator = room_friend_record[0].creator
            # friend = room_friend_record[0].friend

            # uchatbot = UserProfile.objects.get(username='uChat-bot')

            # creator_bot = creator.get_bot(uchatbot)
            # friend_bot = creator.get_bot(uchatbot)
        
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
        # frienddata = Friend.objects.get(room=room)
        # frienddata.save()
        room.save()
        log.debug('chat message room=%s handle=%s message=%s', 
            room.label, data['handle'], data['message'])
        

        _bot_message = bot_message(data)

        main_message = room.messages.create(**data)
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(main_message.as_dict())})
        
        if flag:
            if _bot_message['status']:
                Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(_bot_message)})
        else:
            Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(_bot_message)})
        
@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass


# def bot_message(data):
#     if data['message'] == 'Hi' or data['message'] == 'hi':
#         m = {
#             'message': 'welcome to uchat',
#             'handle': 'uChat-bot',
#             'status': True
#         }
#         return m
#     elif data['message'] == 'uchat':
#         m = {
#                 'message': 'welcome to uchat',
#                 'handle': 'uChat-bot',
#                 'status': True
#             }
#         return m
#     else:
#         m = {
#             'message': 'I did not recognize your command. Try use following\nHi\nuchat',
#             'handle': 'uChat-bot',
#             'status': False
#         }
#         return m

