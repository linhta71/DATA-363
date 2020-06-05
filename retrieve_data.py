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
        f.close()
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
    f.close()

def load_lists(soup, cache_folder = "./cache", data_folder = "./data"):
    '''
    soup : object
    flag: an interger
    cache_folder: string: path to the folder that we put temp files
    data_folder: string: path tothe data folder that we store our data
    data_fname: string: the name of the data file
    
    this function will take every data in the soup object in column order and replace all the nan value
    in the file into the flag. It then returns the matrix of the given file, which stores strings.
    '''
    data = []
    rows = soup.find_all('tr')
    rows.pop(0)
    f = open(cache_folder+"/"+'inspect.txt', 'w')
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
    f.close()
    return data

def serialize_list(parsed_matrix, data_folder = "./data/", data_fname = "project_data.csv"):
    """
    parsed_matrix: the matrix (list of list, [m][n] gives row m, column n)
        that is parsed and ready to be made into csv file
    data_folder: string: path to the folder that we store data for the project
    data_fname: string: file name of the data being parsed. Requires ".csv" suffix

    This function takes in parsed_matrix and write a file saved as data_folder + data_fname in
    .csv format.
    """
    #change to txt format in term of comma separation file
    data_path_name = data_folder+data_fname
    file = open(data_path_name, 'w')
    for row in parsed_matrix:
        string = '|'.join(row)+'\n'
        string = string.replace(',', '.')
        string = string.replace('|', ',')
        file.write(string)
    file.close()
    
def get_matrix(weblink = 'https://money.com/best-colleges/',
               cache_folder = "./cache/", data_folder = "./data/"):    
    print("Retrieving data")
    soup = get_soup(weblink)
    print("Saving soup obj")
    cache_html_name = cache_folder + "project.html"
    save_soup(cache_html_name, soup)
    print("Making matrix from given soup obj")
    data = load_lists(soup, cache_folder, data_folder)
    return data

def main():
    data = get_matrix()
    serialize_list(data)
    return data


if __name__ == '__main__':
    data = main()
