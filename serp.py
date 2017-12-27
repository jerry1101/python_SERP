
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.google.com/search?q=tower+vodka&oq=tower+vodka')

soup= BeautifulSoup(page.text,'html.parser')

urls = soup.find_all('h3', class_='r')

# remove image result
for url in urls:
	if 'Images' in url.text:
		urls.remove(url)

# list the first five
for search in urls[:5]:
		print(search.text)
		print("URL: ",search.a['href'])

