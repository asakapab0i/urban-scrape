from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep # be nice
from slugify import slugify

import sys

import MySQLdb
import pprint

#setup database
db = MySQLdb.connect(host="localhost",
        user="",passwd="",db="")
#end database

BASE_URL = "http://www.urbandictionary.com"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_page_link(link):

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

    pages = get_page_link(word_url)

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


        """
        word_data = []
        for i in range(0,len(word_boxdiv)):
            words = []
            for div in word_boxdiv:
                words.append(word_boxdiv[i].find("div", class_="word"))
            word_data.append(words)

        print words
        """


        """
        word_data = []
        i = 0
        for div in word_boxdiv:
            #wordbox = BeautifulSoup(div, 'lxml')
            word_data.insert(i, div.find("div", class_="word"))
            word_data[i].append(div.find("div", class_="meaning"))
            word_data[i].append(div.find("div", class_="example"))
            word_data[i].append(div.find("div", class_="contributor"))
            word_data[i].append(div.find("a", class_="up")).find('span',class_="count")
            word_data[i].append(div.find("a", class_="down")).find('span',class_="count")
            #print wordbox.find("div", {"class":"word"}).find('a').string
            i+=1

        for word in word_data:
            if word is not None:
                print word.get_text()
                sys.exit(0)
        """
    """
    word_name = word_boxdiv.find('div', {"class" : "word"}).find('a').string
    word_meaning = word_boxdiv.find("div",{"class" : "meaning"}).get_text()
    word_example = word_boxdiv.find("div", {"class" : "example"}).get_text()
    """

    #return {"word_name":word_name,"word_meaning":word_meaning,"word_example":word_example}

if __name__ == '__main__':

    #letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    #letters = ['N','O','P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']



    print get_page_link("http://www.urbandictionary.com/browse.php?word=aa")

    """
    word_links = get_category_links("http://www.urbandictionary.com/popular.php?character=A");

    dictionary = []
    for l in word_links:
        print len(dictionary.append(get_word_details(l)))
        sys.exit(0)



    """
    """
    for l in letters:
        url = "http://www.urbandictionary.com/popular.php?character="+l;
        word_links = get_category_links(url)

        word_details = []
        for word_url in word_links:
            words = get_word_details(word_url)

            word = words['word_name'].encode('utf-8')
            meaning = words['word_meaning'].encode('utf-8')
            example = words['word_example'].encode('utf-8')
            word_slug = slugify(words['word_name'])

            cursor = db.cursor()
            cursor.execute("INSERT INTO words (word, word_slug)VALUES(%s, %s);", (word,word_slug))
            wordid = cursor.lastrowid
            cursor.execute("INSERT INTO definitions (word_id,account_id,definition,definition_example)VALUES(%s,%s, %s, %s);",(wordid, 1, meaning, example))
        db.commit()

    db.close()
    """
