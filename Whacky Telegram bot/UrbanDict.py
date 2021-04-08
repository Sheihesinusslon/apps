from udpy import UrbanClient

# init connection with Urban Dictionary
client = UrbanClient()


def get_urban_definition(word: str):
	'''Function sends a request to UD to get a definition for a provided word
	and returns text or unsuccess-notification'''
	defs = client.get_definition(word)
	text = ''.join(f'\n<b>{word}</b>\n' + d.definition.replace('[', '').replace(']', '') + '\n' for d in defs[:5])
	return text or "Couldn't find a definition for your request :/"

def get_urban_words():
	'''Function sends a request for 10 random slangs to UD and and returns text ''' 
	rand = client.get_random_definition()
	text = '\n'.join(f'\n<b>{d.word}</b>\n' + d.definition.replace('[', '').replace(']', '') for d in rand)
	return text 
