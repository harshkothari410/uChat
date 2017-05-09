from chatapp.wikidata import get_wikipedia_data
from textblob import TextBlob
from chatapp.yelpdata import get_yelp_data
from chatapp.uberdata import get_uber_data


keyword = {
	'do you know': 'wiki',
	'can you tell': 'wiki',
	'have you any idea': 'wiki',
	'can you suggest': 'yelp',
	'lets go for dinner tonight': 'yelp',
	'uber': 'uber'
}

def bot_message(data):
	message = data['message'].lower()

	helper_string = """I did not understand your command. Please try to following

Do you know about <name>? 
Can you tell me about <thing>?
Can you suggest some place for dinner at <place>?
uber:address"""
	service = None
	
	try:
		for k, v in keyword.items():
			if k in message:
				service = v
				break

		if service == 'wiki':
			noun = extract_noun(message)
			wikidata = get_wikipedia_data(noun)

			if wikidata:
				return create_reply(wikidata, True, service)
			else:
				return create_reply(helper_string, False)


		if service == 'yelp':
			noun = extract_noun(message)

			if noun == 'tonight':
				noun = ''
			yelpdata = get_yelp_data(noun)
			if yelpdata:
				return create_reply(yelpdata, True, service)

		if service == 'uber':
			location = message.split(':')[-1]

			uberdata = get_uber_data(location)

			if uberdata:
				return create_reply(uberdata, True, service)

	except:
		return create_reply(helper_string, False)
	
	return create_reply(helper_string, False)

	# if data['message'] == 'Hi' or data['message'] == 'hi':
 #        m = {
 #            'message': 'welcome to uchat',
 #            'handle': 'uChat-bot',
 #            'status': True
 #        }
 #        return m
 #    elif data['message'] == 'uchat':
 #        m = {
 #                'message': 'welcome to uchat',
 #                'handle': 'uChat-bot',
 #                'status': True
 #            }
 #        return m
 #    else:
 #        m = {
 #            'message': 'I did not recognize your command. Try use following\nHi\nuchat',
 #            'handle': 'uChat-bot',
 #            'status': False
 #        }
 #        return m

def create_reply(message, flag, service=None):
	return {
		'message': message,
		'handle': 'uChat-bot',
		'status': flag,
		'service': service
	}

def message_parse():
	pass

def extract_noun(sentence):

	blob = TextBlob(sentence)
	print blob.noun_phrases

	if blob.noun_phrases:
		return blob.noun_phrases[0]
	else:
		sentence = sentence.replace('?', '')
		sentence = sentence.strip()
		split_sentence = sentence.split(' ')

		print sentence, split_sentence
		if split_sentence[-1]:
			return sentence.split(' ')[-1]


