import time

from selenium import webdriver

path = 'D:/bin/chromedriver/chromedriver.exe'
wd = webdriver.Chrome(path)
wd.get('https://www.google.com')

time.sleep(2)
html = wd.page_source
print(html)

wd.quit()