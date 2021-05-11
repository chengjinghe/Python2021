import urllib.request as req
from bs4 import BeautifulSoup
import time
'''
测试爬虫
'''
def SD(func):   
    def sitedata(*args,**kwargs):
        time.sleep(2)
        request = req.Request(*args, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
        })
        with req.urlopen(request, timeout=30) as respose:
            data = respose.read()
            data = str(data, encoding='utf-8')
        up = BeautifulSoup(data, 'html.parser')
        func()
        return up
    return sitedata

if __name__ == "__main__":
    pass