from selenium import webdriver
import time

class Mail():
    '''
    yishion 内网邮件查询 和用户增加
    mailQueryUser 输入在查询的用户名
    add_mailaccount 要新增加的用户名
    '''
    dr = webdriver.Chrome()
    dr.implicitly_wait(30)
    dr.maximize_window()
    dr.get('http://192.168.0.252:889/madmin/login.php')
    dr.find_element_by_id('txtname').send_keys('admin')#在帐号填入帐号
    dr.find_element_by_id('txtpwd').send_keys('yishionmail1049')#在帐号填入帐号
    dr.find_element_by_id('button').click()#单击登录按钮
    dr.find_element_by_link_text('用户管理').click()#进入用户管理
    dr.find_element_by_link_text('组织架构').click()#进入组织架构
    def mailQueryUser(self,s_username=None,username=None):
        '''
        s_username 要查询的用户名
        username 要新增加的用户名
        '''
        try:
           self.dr.find_element_by_xpath(r'/html/body/div[4]/div/div[2]/div[2]/div/div[1]/div[2]/label/input').send_keys(s_username)
        except TypeError as err:
            print(err)
        time.sleep(10)
        if adduser == None:
            return s
        else:
            add_mailaccount(username)

    def add_mailaccount(self,username,password=None):
        '''
        username 要新增加的用户名
        password 新用户的密码 默认123456
        '''
        self.dr.find_element_by_id('add').click()
        self.dr.find_element_by_xpath('//*[@id="users_id"]').send_keys(username)#用户名
        self.dr.find_element_by_xpath('//*[@id="users_truename"]').send_keys('new_mailname')#真实姓名
        self.dr.find_element_by_xpath(r'/html/body/div[11]/div[2]/form/div/table[1]/tbody/tr[1]/td[2]/select/option[3]').click()#选择.net后缀
        if password ==None:
            self.dr.find_element_by_id('users_pass').send_keys(123456)#设置用户密码123456
            self.dr.find_element_by_id('users_pass2').send_keys(123456)#设置用户密码123456
        else:
            self.dr.find_element_by_id('users_pass').send_keys(password)#设置用户密码
            self.dr.find_element_by_id('users_pass2').send_keys(password)#设置用户密码
