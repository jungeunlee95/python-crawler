import os
import ssl
import sys
import time
from builtins import print
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

# import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler

# 베이스 폴더
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def crawling_pericana():
    results = []
    for page in count(start=11):

        url = 'https://pelicana.co.kr/store/stroe_search.html?page=1&branch_name=&gu=&si=&page=%d'
        # html = crawler.crawling(url, page)
        html = request_url(url, page)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split(' ')[:2]
            results.append((name, address) + tuple(sidogu))

        # store      -> pandas
        # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
        # table.to_csv('__results__/pericana.csv', encoding='utf-8', mode='w', index=True)
def crawling_nene():
    results = []
    for page in range(1, 5):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d'
        html = request_url(url, page)
        bs = BeautifulSoup(html, 'html.parser')
        names = bs.findAll('div', attrs={'class': 'shopName'})
        addresses = bs.findAll('div', attrs={'class': 'shopAdd'})

        for i in range(len(names)):
            sidogu = addresses[i].text.split(' ')[0:2]
            results.append((names[i].text, addresses[i].text) + tuple(sidogu))

        # 끝 검출
        if(len(names) != 24):
            break

        # store      -> pandas
        # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])

        # 실행 경로 찾기
        RESULT_DIR = f'{BASE_DIR}/__results__'

        print(BASE_DIR)
        print(RESULT_DIR)
        # table.to_csv(f'/root/crawling-results/nene.csv', encoding='utf-8', mode='w', index=True)


def crawling_kyochon():

    results = []

    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d' % (sido1, sido2)
            html = crawler.crawling(url)
            # 끝검출
            if html is None:
                break
            bs = BeautifulSoup(html, 'html.parser')

            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tag_spans = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tag_spans:
                strings = list(tag_span.strings)
                name = strings[1]
                address = strings[3].strip("\r\n\t")
                sidogu = address.split()[:2]

                results.append((name, address) + tuple(sidogu))
                print(name, address, sep=':')

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugon'])
    # table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)
    # print(table)

    for t in results:
        print(t)

def crawling_goobne():

    results = []

    url = 'http://goobne.co.kr/store/search_store.jsp'

    wd = webdriver.Chrome('D:\cafe24\libs\chromedriver\chromedriver.exe')

    wd.get(url)
    time.sleep(4)

    for page in count(start=1):
        # 자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{script}]')
        time.sleep(2)

        # 실행결과 HTML(동적으로 렌더링 된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')

        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    wd.quit()

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugon'])
    # table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)
    # print(table)

    for t in results:
        print(t)

def request_url(url, page):
    url = url % page
    try:
        request = Request(url)
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(request)
        receive = response.read()
        html = receive.decode('utf-8', errors='replace')
        # print(html)
        print(f'{datetime.now()}: success for request [{url}]')
    except Exception as e:
        print(f'{e} : {datetime.now()}', file=sys.stderr)
    return html

if __name__ == '__main__':
    # pericana
    # crawling_pericana()

    # nene 과제
    crawling_nene()
    # crawling_kyochon()
    # crawling_goobne()