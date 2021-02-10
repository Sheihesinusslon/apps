import requests
from bs4 import BeautifulSoup
import re
from collections import deque


urls = {'Urban Dictionary': 'https://www.urbandictionary.com/', 'Merriam-Webster Dictionary': 'https://www.merriam-webster.com/word-of-the-day'}
q = deque(urls.keys())


def get_html(url): 
	r = requests.get(url)
	return r.text


def get_head(dict, html):
	if dict == 'Urban Dictionary':
		soup = BeautifulSoup(html, 'lxml')
		text = soup.find('div', {'class': 'def-panel'}).find_all(text=True)
		return text
	else: 
		soup = BeautifulSoup(html, 'lxml')
		result = []
		head = soup.find('div', {'class': 'article-header-container wod-article-header'}).find_all(text=True)[:9]
		pattern = re.findall(r'\w+', ' '.join(head))
		result.append(' '.join(pattern[:-1]))
		result.append('\n'+pattern[-1])
		text = soup.find('div', {'class': 'wod-definition-container'}).find_all(text=True)
		text = re.split(r'Subscribe\sWOD\sBox', ' '.join(text))
		result.append(text[0])
		return result


def show_result(dict, text):
	if dict == 'Urban Dictionary':
		print(text[0]+'\n')
		print(text[1]+'\n')
		body = text[2:]
		print(body)
		i = re.split(r'\n+', ' '.join(body))
		print(i[0])
	else:
		for i in range(len(text)):
			print(text[i])


def main():
	for i in range(len(q)):
		dict = q.pop()
		print(dict + '\n')
		data = get_head(dict, get_html(urls[dict]))
		show_result(dict, data)


if __name__ == '__main__':
	main()


