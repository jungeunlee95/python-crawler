from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from collection import crawler

def ex01():
    request = Request("https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&date=20190617")
    response = urlopen(request)
    html = response.read().decode('cp949')
    # print(html)

    bs = BeautifulSoup(html, 'html.parser')
    # print(bs.prettify()) # 예쁘게 출력

    divs = bs.findAll('div', attrs={'class':'tit3'})
    # print(divs)

    for rank, div in enumerate(divs, start=1):
        print(rank, div.a.text, 'https://movie.naver.com/'+div.a['href'], sep=" : ")

def ex02():
    crawler.crawling(url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&date=20190617',
                    encoding='cp949',
                    err=error,
                    proc1=proc_naver_movie_rank,
                    proc2=lambda data: list(map(lambda div: print(div.a.text, 'https://movie.naver.com/'+div.a['href'], sep=" : "), data)))

def error(e):
    pass

def proc_naver_movie_rank(data):
    bs = BeautifulSoup(data, 'html.parser')
    results = bs.findAll('div', attrs={'class': 'tit3'})
    return results

def store_naver_movie_rank(data):
    # output
    for rank, div in enumerate(data, start=1):
        print(rank, div.a.text, 'https://movie.naver.com/'+div.a['href'], sep=" : ")
    return data

__name__ == '__main__' \
and not ex01() \
and ex02()
# ex01()이 return이 없으니까, 그 차제가 false잖아 그래서 ex02()실헹