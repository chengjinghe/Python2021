# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def Py_zabbix_email_yishion(func):
    def wa(*args,**kw):
        mail_host = "192.168.0.252"
        mail_name = "hechengjin@yishion.net"
        mail_password = "20knb328"

        sender = "hechengjin@yishion.net"
        receivers = "hclzv@hotmail.com"

        message = MIMEText('文件更新执行完成了','plain','utf-8')
        # message['From'] = Header('reversed')
        message['To'] =  Header("hclzv@hotmail.com")
        
        subject = 'Yishion-Zabbix-Python-监控中心邮件'
        message['Subject'] = Header(subject, 'utf-8')      
        try:
            s = smtplib.SMTP(mail_host)
            # s.connect(mail_host,25)
            s.login(mail_name,mail_password)
            ok = s.sendmail(sender, receivers, message.as_string())
            # ok = ok.read()
        except Exception as e:
            print(e)
           
        return ok
    return wa

if __name__=='__main__':

    @Py_zabbix_email_yishion
    def b():       
        print('hello')
    b1 = b()
    print(b1)