from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep # be nice
from slugify import slugify
import string

import sys

import MySQLdb

BASE_URL = "http://www.urbandictionary.com"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_page_links(link):
    #set alphabet
    alpha = list(string.ascii_lowercase)

    soup = make_soup(link)
    #get pagination number
    try:
        page = soup.find('ul', class_="pagination").find('li',class_="next").find_previous_sibling('li')
        if page is not None:
            page = int(page.get_text())
        print page
    except:
        return

    pages  = []
    for n in range(1, page+1):
        for l in alpha:
            pages.append(link + "&page="+str(n))

    return pages

def get_category_links(section_url):
    soup = make_soup(section_url)

    column = soup.find("div", id="columnist")
    links = []
    for link in column.findAll('a'):
        links.append(BASE_URL+link.get('href'))
    return links

def get_word_details(word_url):
    soup = make_soup(word_url)
    #find all pages for a word

    #get pagination number
    try:
        page = soup.find('ul', class_="pagination").find('li',class_="next").find_previous_sibling('li')
        if page is not None:
            page = int(page.get_text())
        print page
    except:
        return

    pages  = []
    for n in range(1, page+1):
        pages.append(link + "&page="+str(n))


    #iterate to page link and get the words
    for p in pages:
        page_link = make_soup(p)
        print p

        #find all wordbox class
        word_boxdiv = page_link.findAll("div",{"class" : "box"})

        #create a multi dimensional array
        word_data = []
        for div in word_boxdiv:
            #word
            try:
                word = div.find("div", class_="word")
                word = word.find('a').string
                print word
                #meaning
                meaning = div.find("div", class_="meaning")
                meaning = meaning.get_text()
                #example
                example = div.find("div", class_="example")
                example = example.get_text()
                #contributor
                contrib = div.find("div", class_="contributor")
                contrib = contrib.find('a').string
            except:
                pass

            word_data.append({
                "word":word,
                "meaning":meaning,
                "example":example,
                "contributor":contrib,
                })

            return word_data


if __name__ == '__main__':
    alpha = list(string.ascii_lowercase)
    alpha2 = list(string.ascii_lowercase)

    suffix = []
    for l in alpha:
        for l2 in alpha2:
            suffix.append(str(l)+str(l2))

    pages = []
    for l in suffix:
        pages.append(get_page_links("http://www.urbandictionary.com/browse.php?"+l))
        print pages
        sys.exit(0)




