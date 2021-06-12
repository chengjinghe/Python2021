
from bs4 import BeautifulSoup
from he_webreq import Web
import time
url = 'http://www.qqc.net/cydq/abcd/'
webside = 'http://www.qqc.net'
w = Web()
def test1():
    
    time.sleep(1)
    try:
        for x1,r1 in enumerate(data.find_all('a')[37:141]):
            time.sleep(2)
            textorsedi = r1.string,webside + r1.get('href')
            r = w.reqdata(url=textorsedi[1])
            for x2,r2 in enumerate(r.find_all('p')):
                if x2 == 0: #Begin site prompt notifications
                    kaishi = r2.string 
                elif r2.string == kaishi: #Simple whether or not to switch notification             
                    continue
                elif r2.string == None:#Whether the content string is empty
                    continue
                else:
                    print(x1,r1.string,':',r2.string)#Get the content string      
        #Find the button URL on the next page
        for x,r in enumerate(data.find_all('a')):
            if r.string == '下一页':
                nextbutton =webside + r.get('href') #Next page URL splicing
                global url
                url = nextbutton #  修改全局变量为下一页网址         
                return url
    except Exception as err:
        print(err)

while True:
    data = w.reqdata(url=url)
    x =  test1()
