import sys
import urllib
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup

def find_bus():

    url = 'https://map.kakao.com/?busStopId=BS82847'
    request = Request(url)
    response = urlopen(request)

    receive = response.read()
    html = receive.decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')

    print(bs)


if __name__ == '__main__':
    find_bus()
