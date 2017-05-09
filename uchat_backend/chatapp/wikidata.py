import wikipedia


def get_wikipedia_data(topic):

	try:
		return wikipedia.summary(topic, sentences=2)
	except wikipedia.exceptions.DisambiguationError as e:
		print e.options
		return wikipedia.summary(e.options[0], sentences=2)
	except:
		search = wikipedia.search(topic)

		try:
			return wikipedia.summary(search[0], sentences=2)
		except:
			return wikipedia.summary(search[1], sentences=2)


	return False