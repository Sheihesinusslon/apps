import requests
from bs4 import BeautifulSoup
import re

# set dict with resources and URLs
urls = {'Urban Dictionary': 'https://www.urbandictionary.com/',
		'Merriam-Webster Dictionary': 'https://www.merriam-webster.com/word-of-the-day'}


def _get_html(url: str) -> str:
	''' Parse all text from given URL '''
	r = requests.get(url)
	return r.text


def _get_post(dict_: str, html: str):
	''' Process html text and get the first post with latest word of the day '''
	if dict_ == 'Urban Dictionary':
		soup = BeautifulSoup(html, 'lxml')
		post = soup.find('div', {'class': 'def-panel'}).find_all(text=True)
		return post
	if dict_ == 'Merriam-Webster Dictionary':
		soup = BeautifulSoup(html, 'lxml')
		post = []
		head = soup.find('div', {'class': 'article-header-container wod-article-header'}).find_all(text=True)[:9]
		pattern = re.findall(r'\w+', ' '.join(head))
		post.append(' '.join(pattern[:-1]))
		post.append('\n'+pattern[-1])
		text = soup.find('div', {'class': 'wod-definition-container'}).find_all(text=True)
		text = re.split(r'Subscribe\sWOD\sBox', ' '.join(text))
		post.append(text[0])
		return post


def _edit_post(dict_: str, text: str):
	''' Process post, edit text '''
	processed = []
	if dict_ == 'Urban Dictionary':
		processed.append(text[0]+'\n')
		processed.append(text[1]+'\n')
		body = text[2:]
		i = re.split(r'\n+', ' '.join(body))
		processed.append(i[0]+'\n\n')
	if dict_ == 'Merriam-Webster Dictionary':
		for i in range(len(text)):
			processed.append(text[i])
	return ''.join(processed)


def word_of_the_day() -> str:
	''' Main function, starts requests to resources listed in urls dict,
	parses latest 'Word of the Day' posts, returns ready processed text '''
	response = ''
	for dict_, url in urls.items():
		response += '<a href="{0}">{1}</a>\n\n'.format(url, dict_)
		data = _get_post(dict_, _get_html(url))
		response += _edit_post(dict_, data)
	return response
