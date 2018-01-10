
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
import os


def empty_output_file(file="output.txt"):
    if os.path.isfile(file):
        os.remove(file)
    with open(file, 'a+') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                               quotechar='"', quoting=csv.QUOTE_NONE,escapechar='\\')
        csvwriter.writerow(['keyWord']+["rank#1"]+["rank#2"]+["rank#3"]+["rank#4"]+["rank#5"])


def write_ranking(column, file="./output.txt"):
    with open(file, 'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                               quotechar='', quoting=csv.QUOTE_NONE,escapechar='\\')
        csvwriter.writerow(column)


def read_products(file="./productlist1.txt"):
    productfile = open(file, "r")

    lines= productfile.read().splitlines()

    return lines


def get_url(searchtext=""):
    parameter = searchtext.lower().replace(" ", "+")
    return 'https://www.google.com/search?q=%s&oq=%s' % (parameter, parameter)


def get_search_urls():
    search_urls=[]
    for product in read_products():
        search_urls.append(get_url(product))
    return search_urls

############################################################


empty_output_file()

urls = get_search_urls()


def list_ranking_in_serp(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('h3', class_='r')
    # remove image result
    for link in links:
        if 'Images' in link.text:
            links.remove(link)

    columnToWrite = [url]

    # list the first five
    for search in links[:10]:
        # columnToWrite += ";"+search.a['href'].split("//")[-1].split("/")[0]
        columnToWrite.append([search.a['href'].split("//")[-1].split("/")[0]])
        print("URL: ", search.a['href'])
        print("Domain: ", search.a['href'].split("//")[-1].split("/")[0])

    write_ranking(columnToWrite, file="./output-"+str(os.getpid())+".txt")


if __name__ == '__main__':
        p = Pool(processes=3)
        print(p.map(list_ranking_in_serp, urls))
