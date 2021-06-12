# -*- coding: UTF-8 -*-
import urllib.request as req
import bs4,re,time
from bs4 import BeautifulSoup

class Web():
    def reqdata(self,url):
        request = req.Request(url=url,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
            })
        with req.urlopen(request) as response:
            data = response.read()#.encoding='utf-8'  
            

        soup = BeautifulSoup(data,"html.parser")
        return soup,data
if __name__ == "__main__":
    w = Web()
    w.reqdata(url='http://www.qqc.net/gushi/chunqiu/')

