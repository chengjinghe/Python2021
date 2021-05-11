from selenium import webdriver
import time
dr = webdriver.Chrome()
dr.implicitly_wait(30)
dr.maximize_window()
def mailaccount(s_username=None,adduser=None):
    dr.get('http://192.168.0.252:889/madmin/login.php')
    dr.find_element_by_id('txtname').send_keys('admin')#在帐号填入帐号
    dr.find_element_by_id('txtpwd').send_keys('yishionmail1049')#在帐号填入帐号
    dr.find_element_by_id('button').click()#单击登录按钮
    dr.find_element_by_link_text('用户管理').click()#进入用户管理
    dr.find_element_by_link_text('组织架构').click()#进入组织架构
    try:
        dr.find_element_by_xpath(r'/html/body/div[4]/div/div[2]/div[2]/div/div[1]/div[2]/label/input').send_keys(s_username)
    except TypeError as err:
        print(err)
    time.sleep(10)
    if adduser == None:
        return
    else:
        add_mailaccount(adduser)

def add_mailaccount(adduser):
    dr.find_element_by_id('add').click()
    dr.find_element_by_xpath('//*[@id="users_id"]').send_keys(adduser)#用户名
    dr.find_element_by_xpath('//*[@id="users_truename"]').send_keys('new_mailname')#真实姓名
    dr.find_element_by_xpath(r'/html/body/div[11]/div[2]/form/div/table[1]/tbody/tr[1]/td[2]/select/option[3]').click()#选择.net后缀
    dr.find_element_by_id('users_pass').send_keys(123456)
    dr.find_element_by_id('users_pass2').send_keys(123456)

if __name__=="__main__":
    mailaccount(s_username='廖婷',adduser='wangxiaoyue')