import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
import os
from time import sleep
from random import randint
from re import search as research
from os.path import basename
from functools import partial


MAX_CHUNKS = 40


def write_row(file_index, line):

    with open("./temp/input_%d.txt" % file_index, 'a+', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_NONE,escapechar='\\')
        writer.writerow(line)


def cleanup():
    for f in os.listdir("./temp"):
        if research("[output|input]_.*", f):
            os.remove(os.path.join("./temp/", f))


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
                               quotechar='', quoting=csv.QUOTE_NONE, escapechar='\\')
        csvwriter.writerow(column)


def read_products(file="./temp/input_1.txt"):
    keyword_file = open(file, "r")

    lines = keyword_file.read().splitlines()

    return lines


def get_url(searchtext=""):
    parameter = searchtext.lower().replace(" ", "+")
    return 'https://www.google.com/search?q=%s&oq=%s' % (parameter, parameter)


def get_search_urls(file_path):
    search_urls=[]
    for product in read_products(file_path):
        search_urls.append(get_url(product))
    return search_urls


def add_execution_deplay():
    sleep(randint(3, 10))


def find_ranking():
    for f in os.listdir("./temp"):
        if research("input", f):
            url_list = get_search_urls(os.path.join("./temp/", f))
            p = Pool(processes=5)
            prod_x = partial(list_ranking_in_serp, source= os.path.splitext(basename(f))[0])  # prod_x has only one argument x (y is fixed to 10)
            print(p.map(prod_x, url_list))


        #print(p.map(list_ranking_in_serp, url_list))


def cut_input_file():
    with open("keyword.txt", "rt", encoding='utf8') as results:
        r = csv.reader(results, delimiter=',', quotechar='\"')
        idr = 1
        for i, x in enumerate(r):
            temp = i + 1
            if not (temp % (MAX_CHUNKS + 1)):
                idr += 1
            write_row(idr, x)


def list_ranking_in_serp(url, source='output_1'):
    add_execution_deplay()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('h3', class_='r')
    # remove image result
    for link in links:
        if 'Images' in link.text:
            links.remove(link)

    column_to_write = [research('q=(.+?)&oq', url).group(1)]

    # list the first five
    for search in links[:10]:
        # column_to_write += ";"+search.a['href'].split("//")[-1].split("/")[0]
        column_to_write.append([search.a['href'].split("//")[-1].split("/")[0]])
        print("URL: ", search.a['href'])
        print("Domain: ", search.a['href'].split("//")[-1].split("/")[0])

    write_ranking(column_to_write, file="./"+source+"_output-"+str(os.getpid())+".txt")


def main():
    #cleanup()

    #cut_input_file()

    find_ranking()

if __name__ == '__main__':

    main()
