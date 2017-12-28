
import requests
from bs4 import BeautifulSoup
import csv
import os

def emptyOutputFile(file="output.txt"):
    if os.path.isfile(file):
        os.remove(file)
    with open(file, 'a+') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                               quotechar='"', quoting=csv.QUOTE_NONE,escapechar='\\')
        csvwriter.writerow(['keyWord']+["rank#1"]+["rank#2"]+["rank#3"]+["rank#4"]+["rank#5"])

def writeRanking(column,file="./output.txt"):
    with open(file, 'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                               quotechar='', quoting=csv.QUOTE_NONE,escapechar='\\')
        csvwriter.writerow(column)

def readProducts(file="./productlist.txt"):
    productfile = open(file,"r")

    lines= productfile.read().splitlines()

    return lines


def getURL(querytxt=""):
    parameter = querytxt.lower().replace(" ","+")
    return 'https://www.google.com/search?q=%s&oq=%s'% (parameter,parameter)

# writeRanking()



############################################################


emptyOutputFile()


for keyword in readProducts():
    print("-->>>>>",keyword,"<<<<<<---")
    page = requests.get(getURL(keyword))
    soup= BeautifulSoup(page.text,'html.parser')
    urls = soup.find_all('h3', class_='r')
    # remove image result
    for url in urls:
        if 'Images' in url.text:
            urls.remove(url)

    columnToWrite =[keyword]

    # list the first five
    for search in urls[:5]:
        #columnToWrite += ";"+search.a['href'].split("//")[-1].split("/")[0]
        columnToWrite += [search.a['href'].split("//")[-1].split("/")[0]]
        print("URL: ",search.a['href'])
        print("Domain: ",search.a['href'].split("//")[-1].split("/")[0])


    writeRanking(columnToWrite)