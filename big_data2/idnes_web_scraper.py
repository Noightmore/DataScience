import requests
from bs4 import BeautifulSoup
import re
from urlextract import URLExtract
import json
import os


URL_archiv = "https://www.idnes.cz/zpravy/archiv/"
extractor = URLExtract()
f_JSON = "Idnes_data_final.json"
SIZE = 1000


def fileSize():
    size = float(os.stat(f_JSON).st_size) / (1024 * 1024)
    print(size)
    return size


def write2json(data):
    if os.stat(f_JSON).st_size != 0:
        with open(f_JSON, 'rb+') as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()
    else:
        with open(f_JSON, 'w') as f:
            f.write("[")

    with open(f_JSON, "a", encoding='utf-8') as f:  # Open the file with utf-8 encoding
        for dat in data:
            if os.stat(f_JSON).st_size > 1:
                f.write(',')

            try:
                json.dump(dat, f, ensure_ascii=False, indent=4)
            except UnicodeEncodeError:
                print("Skipped an item due to encoding error.")
                continue  # Skip this item if an encoding error occurs

        f.write("]")



def readJSON():
    with open(f_JSON, 'r') as f:
        data = json.load(f)

    for dat in data:
        print(dat['title'])


def find_articles(page_num):
    page = requests.get(URL_archiv+str(page_num))
    soup = BeautifulSoup(page.text, "html.parser").prettify()
    x = " ".join(re.findall('<a class="art-link" .*', soup))
    return extractor.find_urls(x)


def read_article(url):
    data = dict()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    if re.compile(r'content=free').search(soup.prettify()):
        try:
            texta = soup.find(class_="bbtext")
            rel = ''
            for tex in texta.findAll('p'):
                rel += tex.text
            data['text'] = rel
            data['date'] = soup.find("span", {"class": "time-date"}).text
            soup = soup.prettify()
            data['title'] = re.sub('( - iDNES.cz)|(\s{2,})', '',re.findall("(?<=<title>\n)(.*)(?=\n)", soup)[0])
            data['category'] = re.findall('(?<="subSection": ")(.*)(?=", "pageType")', soup)[0]
            pocet_com = re.findall('(?<=\()(\d*)(?= příspěv)', soup)
            if not pocet_com:
                pocet_com = "0"
            data['num_comments'] = int(pocet_com[0])

            pocet_fot = re.findall('(?<=<b>\n)( *\d*\n *)(?=<\/b>\n *fotograf)', soup)
            if not pocet_fot:
                pocet_fot = "0"
            data['num_photos'] = int(re.sub('( *|\\n)','', pocet_fot[0]))
        except:
            print("MIStake")
            return None
    return data


if __name__ == '__main__':
    for i in range(3000, 7000):
        print("PAGE: " + str(i))
        urls = find_articles(i)
        data = []
        for url in urls:
            dat = (read_article(url))
            if dat:
                data.append(dat)
        if data:
            write2json(data)
    readJSON()

