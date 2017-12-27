
import requests
from bs4 import BeautifulSoup


def readProducts(file="./productlist.txt"):
    productfile = open(file,"r")

    lines= productfile.read().splitlines()

    return lines


def getURL(querytxt=""):
    parameter = querytxt.lower().replace(" ","+")
    return 'https://www.google.com/search?q=%s&oq=%s'% (parameter,parameter)

#print(readProducts())


for keyword in readProducts():
    print("-->>>>>",keyword,"<<<<<<---")
    page = requests.get(getURL(keyword))
    soup= BeautifulSoup(page.text,'html.parser')
    urls = soup.find_all('h3', class_='r')
    for url in urls:
        if 'Images' in url.text:
            urls.remove(url)
    for search in urls[:5]:
            print(search.text)
            print("URL: ",search.a['href'])



#print(getURL("toWer vodka"))

# page = requests.get('https://www.google.com/search?q=tower+vodka&oq=tower+vodka')


# remove image result

# list the first five

