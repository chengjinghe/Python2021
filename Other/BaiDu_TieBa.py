import urllib.request as req
import bs4,re,time,random
def title(url=None):
    whilesn = 0

    sleeptime = random.randint(1,5)
    print("程序暂停{0}秒，请稍后".format(sleeptime))
    time.sleep(sleeptime)
    url = url
    request = req.Request(url,headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
        })
    with req.urlopen(request) as response:
        data = response.read()
        data = str(data,encoding='utf-8')   
    #提取文章标题
    data0 = re.findall(r'title="主题作者:[\s\S]+?"',data)
    data1 = re.findall(r'<a rel="noreferrer" href="[\s\S]*?</a>',data)
    # print(data1)
    data1 = str(data1)
    data1 = re.findall(r'title="[\s\S]*?" target',data1)
    #删除前三行
    del data1[0:3:1]
    b = []
    tsn = 0
    for i in data1:
        
        j = (i[6:-7],tsn)
        b.append(j)
        tsn += 1
        headline = i[6:-7]
        # print(headline)
    return b
    whilesn += 1
     
        
if __name__ == "__main__":
    dongguan_changan = title(url='https://tieba.baidu.com/f?kw=%E4%B8%9C%E8%8E%9E%E9%95%BF%E5%AE%89')
    print(dongguan_changan)
#https://tieba.baidu.com/f?kw=%E4%B8%9C%E8%8E%9E%E9%95%BF%E5%AE%89 东莞长安
# t1 = title(url='https://tieba.baidu.com/f?kw=%D6%D8%C7%EC&fr=ala0&tpl=5')#重庆贴吧
# t2 = title(url='https://tieba.baidu.com/f?kw=%B6%AB%DD%B8&fr=ala0&tpl=5')#东莞贴吧
# t3 = title(url='https://tieba.baidu.com/f?kw=%B9%E3%D6%DD&fr=ala0&tpl=5')#广州贴吧
# b = title(url='https://tieba.baidu.com/f?kw=%B1%B1%BE%A9%CC%F9&fr=ala0&tpl=5')#北京贴吧