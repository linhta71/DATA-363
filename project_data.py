import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests, os, gzip, json
from bs4 import BeautifulSoup
def get_soup(url = None, fname = None, gzipped = False):
    '''
    url: string. defaulk is None
    fname: string. default is None
    gzipped: boolean. default as False. if the html to be parsed is zipped, then True will be passed in.
    This function will open the file if it is not None, then it will pass the the pointer to the beautifulSoup
    constructor and return the object. if the url is None then it will raise a RuntimeError. if the filename is not
    None, this function will request the server, if the response from the server is zipped type, then this function 
    will unzip it and pass the content to the BeautifulSoup constrictor then return the object.
    '''
    if not fname is None:
        f = open(fname)
        soup = BeautifulSoup(f)
        return soup
    if url is None:
        raise RuntimeError('Either url or filename must be specified.')
    else:
        r = requests.get(url)
        if gzipped:
            info = gzip.decompress(r.content)
            soup = BeautifulSoup(info)
        else:
            soup = BeautifulSoup(r.content)
        return soup
def save_soup(fname, soup):
    '''
    fname: string. a name of the file
    soup: soup object
    this function will save a textual representation of the soup object to a file. this function will open 
    the fname in "write" mode and write the repr() of the soup object to the file.
    '''
    f = open(fname, 'w')
    f.write(repr(soup))

def load_lists(soup):
    '''
    soup : object
    flag: an interger
    this function will take every data in the soup object in column order and replace all the nan value
    in the file into the flag
    '''
    data = []
    rows = soup.find_all('tr')
    rows.pop(0)
    f = open('inspect.txt', 'w')
    f.write(repr(rows))
    for i in range(len(rows)):
        data.append([])
    for div in rows[0].find_all('div'):
        i = 0
        a = div.get_text().strip()
        data[i].append(div.get_text().strip())
    # first row
    new = [x for x in data[0] if len(x.strip())>0]
    data[0] = new[1::]

    for i in range(1,len(data)):
        data[i].append(str(i))
    for i in range(1,len(data)):
        for td in rows[i].find_all('td'):
            if td.get_text != '':
                data[i].append(td.get_text())
    
    # delete 2 elements list in data
    data = [x for x in data if len(x) == 8]

    for line in data[1:]:
        new_char = ''
        while line[1][0].isdigit():
            new_char += line[1][0]
            line[1] = line[1][1:]
        line[0] = new_char

    #change to txt format in term of comma separation file
    file = open('project_data.csv', 'w')
    for row in data:
        string = '|'.join(row)+'\n'
        string = string.replace(',', '.')
        string = string.replace('|', ',')
        file.write(string)


def main():
    soup = get_soup('https://money.com/best-colleges/')
    save_soup("project.html", soup)
    load_lists(soup)


if __name__ == '__main__':
    main()