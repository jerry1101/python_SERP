import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
import os
import pandas as pd

from time import sleep
from random import randint
from re import search as research
from os.path import basename
from functools import partial

from serp_input_helper import load_keywords, reformat_dataframe, split_dataframe, dataframe_to_excel

MAX_CHUNKS = 5000


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
            p = Pool(processes=8)
            prod_x = partial(list_ranking_in_serp, source= os.path.splitext(basename(f))[0])  # prod_x has only one argument x (y is fixed to 10)
            print(p.map(prod_x, url_list))


        #print(p.map(list_ranking_in_serp, url_list))


def cut_input_file(keyword_file='./pname_keyword.txt'):
    with open(keyword_file, "rt", encoding='utf8') as results:
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



def load_dataframe_from_excel(file_path):
    with open(file_path,'rt', encoding='utf8') as f:
        excel_file = pd.ExcelFile(file_path)

        return excel_file.parse(excel_file.sheet_names[0])



def list_ranking_in_serp_df(input, source='output_1'):
    add_execution_deplay()

    try:
        url = get_url(input[0])
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('h3', class_='r')
        # remove image result
        column_to_write =[input[1]]
        for link in links:
            if 'Images' in link.text:
                links.remove(link)

        #column_to_write.append([research('q=(.+?)&oq', url).group(1)])
        column_to_write.append([input[0]])
        # list the first five
        for search in links[:10]:
            # column_to_write += ";"+search.a['href'].split("//")[-1].split("/")[0]

            column_to_write.append([search.a['href'].split("//")[-1].split("/")[0]])
            print("URL: ", search.a['href'])
            print("Domain: ", search.a['href'].split("//")[-1].split("/")[0])

        write_ranking(column_to_write, file="./"+source+"_output-"+str(os.getpid())+".txt")
    except Exception as e:
        print(e)
        pass


def parallel_serp(title_list,type_list):
    # spark given number of processes
    p = Pool(10)
    # set each matching item into a tuple
    job_args = [(title_list[i], type_list[i]) for i, item_a in enumerate(title_list)]
    #print(job_args)
    # map to pool
    p.map(list_ranking_in_serp_df, job_args)



def find_ranking_with_df():
    for f in os.listdir("./temp"):
        if research("excel_input", f):

            df = load_dataframe_from_excel(os.path.join("./temp/", f))

            title_list = df['title'].tolist()
            type_list = df['product_type'].tolist()


            parallel_serp(title_list, type_list)


            """
            p = Pool(processes=8)
            prod_x = partial(list_ranking_in_serp_df, source= os.path.splitext(basename(f))[0])  # prod_x has only one argument x (y is fixed to 10)
            print(p.map(prod_x, df['title','product_type']))
            """


def main():

    # read keyword from excel

    #df = load_keywords()

    # clean data in dataframe
    #formatted_df = reformat_dataframe(df)

    #print(formated_df.head())

    # save to small batch
    """
    df_list= split_dataframe(formatted_df)
    print('size of list: '+str(len(df_list)))
    for index, entry in enumerate(df_list, start=1):
        dataframe_to_excel(entry, index)

    """
    #cleanup()

    #cut_input_file()

    find_ranking_with_df()


if __name__ == '__main__':

    main()
