from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
dr = webdriver.Chrome()
dr.maximize_window()
dr.implicitly_wait(30)
def tianqin360():
    dr.get('https://192.168.0.36:8443/login')
    dr.find_element_by_id('details-button').click()
    dr.find_element_by_id('proceed-link').click()
    dr.find_element_by_id('username').send_keys('admin')
    dr.find_element_by_id('userpass').send_keys('yishion#0.36')
    dr.find_element_by_id('login').click()#
    dr.find_element_by_xpath(r'/html/body/div[6]/div/div[3]/button').click()#超出警告确定按钮
    dr.find_element_by_xpath(r'//*[@id="skylarLeft"]/div/div[2]/div/ul/li[2]/a/span').click()#终端管理
    dr.find_element_by_xpath(r'//*[@id="skylarLeft"]/div/div[2]/div/ul/li[2]/ul/li[1]/a/span').click()#终端概况
    dr.find_element_by_xpath(r'/html/body/div[6]/div/div[3]/button').click()#超出警告确定按钮
    # ip = pd.read_excel(r"D:\ip.xlsx")
    # ipaddress = ip['ip']
    # for x in ipaddress:
    #     dr.find_element_by_id('search-input').send_keys(x)
    #     time.sleep(1)
    #     dr.find_element_by_xpath(r'//*[@id="fa-search"]').click()#搜索按钮
    #     time.sleep(3)
    #     dr.find_element_by_xpath(r'//*[@id="clear"]').click()#清除搜索框数据
    
    time.sleep(3)
    
tianqin360()