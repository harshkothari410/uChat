from chatapp.wikidata import get_wikipedia_data
from textblob import TextBlob


keyword = {
	'do you know': 'wiki',
	'can you tell': 'wiki',
	'have you any idea': 'wiki'
}

def bot_message(data):
	message = data['message'].lower()


	for k, v in keyword.items():
		if k in message:
			service = v
			break

	if service == 'wiki':
		noun = extract_noun(message)
		wikidata = get_wikipedia_data(noun)

		if wikidata:
			return create_reply(wikidata, True)
		else:
			return create_reply('I did not understand your command', False)
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

def create_reply(message, flag):
	return {
		'message': message,
		'handle': 'uChat-bot',
		'status': flag
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


