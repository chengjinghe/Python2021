import urllib.request as req
from bs4 import BeautifulSoup
import time,random
def beijin(url):
    url = url
    sleeptime = random.randint(8,28)
    print('Program closed pause {0} seconds, please wait'.format(sleeptime))
    # time.sleep(sleeptime)
    # request = req.Request(url,headers={
    #             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
    #             })
    #写入数据到文件
    # with req.urlopen(request,timeout=30) as beijindata:   #encoding='utf-8'
    #     beijindata = beijindata.read()
    #     beijindata = BeautifulSoup(beijindata,'html.parser')
    #     beijin = open(r'd:\beijin.txt','w+',encoding='utf-8')
    #     beijin.write(str(beijindata))

    #读取文件数据
    with open(r'd:\beijin.txt',encoding='utf-8') as beijin:
        beijingdata = beijin.read()
        beupdata = BeautifulSoup(beijingdata)
        beupdata = beupdata.find_all('a')

        print(beupdata)
    
    # print(bj)


b = beijin(url='https://tieba.baidu.com/f?kw=%B1%B1%BE%A9%CC%F9&fr=ala0&tpl=5')
<a rel=#武夷山纪念币#</span></a>