from lxml import html
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.google.com/search?q=tower+vodka&oq=tower+vodka')

soup= BeautifulSoup(page.text,'html.parser')

urls = soup.find_all('h3', class_='r')


for search in urls[5:]:
	print(search.text)
	print("URL: ",search.a['href'])

