import re
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class StopGame:
	url = 'https://funpay.ru/lots/468/'
	response = requests.get(url)
	soup = BS(response.text, 'lxml')

	def __init__(self, url):
		self.url = url

	def new_games(self):
		url = 'https://funpay.ru/lots/468/'
		r = requests.get(url)
		soup = BS(r.text, 'lxml')
		f = open('l_desc.txt', 'r', encoding='utf-8')
		l_d = f.read()

		new = ""
		item = soup.find('div', class_ = 'tc-desc-text')
		new = f"{item.text}"
		if new != l_d:
			f = open('l_desc.txt', 'w', encoding='utf-8')
			f.write(f"{new}")
			f.close()
			return new
		
		else:
			f.close()
			

	def find_cost(self):
		url = 'https://funpay.ru/lots/468/'
		r = requests.get(url)
		soup = BS(r.text, 'lxml')

		c = soup.find_all('div', class_ = 'tc-price')[1]
		cost = str(c.text)
		price = re.sub("[^1234567890|\.]","",f"{cost}")

		return price

	
	def find_link(self):
		url = 'https://funpay.ru/lots/468/'
		r = requests.get(url)
		soup = BS(r.text, 'lxml')

		l = soup.find('a', class_ = 'tc-item')
		link = l.get('href')

		return str(link)