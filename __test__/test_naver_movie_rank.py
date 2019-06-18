from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

request = Request("https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&date=20190617")
response = urlopen(request)
html = response.read().decode('cp949')
# print(html)

bs = BeautifulSoup(html, 'html.parser')
# print(bs.prettify())

divs = bs.findAll('div', attrs={'class':'tit3'})
# print(divs)

for rank, div in enumerate(divs, start=1):
    print(rank, div.a.text, 'https://movie.naver.com/'+div.a['href'], sep=" : ")
