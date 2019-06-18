import ssl
import sys
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup

def crawling_pelicana():
    results = []
    for page in count(start=113):
        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page

        try:
            request = Request(url)

            # CERTIFICATE_VERIFY_FAILED 에러 해결
            # context = ssl._create_unverified_context()
            # response = urlopen(request, context=context)

            # 위 아래 둘 중 하나로 해결 가능!

            ssl._create_default_https_context = ssl._create_unverified_context
            response = urlopen(request)

            receive = response.read()
            html = receive.decode('utf-8', errors='replace')
            # print(html)
            print(f'{datetime.now()} : success for request [{url}')
        except Exception as e:
            print('%s : %s' % (e, datetime.now()), file=sys.stderr)
            continue


        bs = BeautifulSoup(html, 'html.parser')


        # # ---- 1
        # trs = bs.table.findAll("tr")
        # for i in range(1, len(trs) - 1):
        #     td = trs[i].findAll('td')
        #     title = td[0].text
        #     addr = td[1].text
        #     call = td[2].text.strip()
        #     sidogu = addr.split()[:2]
        #     print(f'가게 이름: {title}, 주소: {addr}, 전화번호: {call}, 시도구 : {sidogu[0], sidogu[1]}')
        #     print("--------------------------------")

        # ---- 2
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
            sidogu = address.split()[:2]
            results.append((name, address) + tuple(sidogu))

        # for t in results:
        #     print(t)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gu'])
    # print(table)
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=0)


def crawling_nene():
    results = []
    cnt = 0
    for page in count(start=1):
        try:
            url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page
            request = Request(url)
            response = urlopen(request)

            receive = response.read()
            html = receive.decode('utf-8')

            print(f'{datetime.now()} : success for request [{url}')

        except Exception as e:
            print('%s : %s' % (e, datetime.now()), file=sys.stderr)
            continue

        bs = BeautifulSoup(html, 'html.parser')

        divs = bs.select('.shopWrap > .shop')
        for info in divs:
            info_list = info.select('td')
            name = info_list[0].select('.shopName')[0].text
            addr = info_list[0].select('.shopAdd')[0].text
            sidogu = addr.split()[:2]
            call = info_list[1].a['href'].split(':')[1]

            results.append((name, addr, call) + tuple(sidogu))

        if page == 1:
            cnt = len(divs)
        elif len(divs) != cnt:
            break
    # store
    table = pd.DataFrame(results, columns=['name', 'address','tel', 'sido', 'gu'])
    table.to_csv('__results__/nene.csv', encoding='utf-8', mode='w', index=0)

if __name__ == '__main__':
    # pelicana
    crawling_pelicana()

    # nene 과제
    crawling_nene()
