# -*- coding: UTF-8 -*-

import paramiko,time
start = time.time()
tnow = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
com1 = "uptime"
# path = 'mysqldump -u root -pccc.! zabbix > /mnt/w10/'+ str(tnow) +'-zabbix.sql'
class Ssh():
    hostname = str(input("Please enter hostname or IP："))
    port = 22
    username = str(input("Please enter Username："))
    password = str(input("Please enter Password："))
    # command = com1
    def sshCommand(hostname=hostname,port=port,username=username,password=password,command=com1):
        sshClient = paramiko.SSHClient()       
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.load_system_host_keys()
        sshClient.connect(hostname,port,username,password)
        stdin,stdout,stderr = sshClient.exec_command(command)
        print(stdout.read())
            
        

Ssh()
endtime = time.time()

runtime = start - endtime
print(runtime)

# print (stderr.read())
    
# if __name__=="__main__":
    # sshCommand("192.168.208.240",22,"root","zabbixc...!",path)  #  mysql - uroot - p123 测试 < test. sql 恢复文件路径  0201031-2zabbix.sql 恢复到zabbix数据中
# print ('Backup execution complete!')
# Ssh("192.168.208.240", 22, "root", "zabbixc...!", "uptime")  #查看电脑运行时长
#先接连接WIN10共享
    # sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "mount -t cifs -o username="Administrator",password="ccc." //192.168.208.2/Zabbix_Mysql_Backup /mnt/w10")

# 修复zabbix中文乱码问题
# 复制字体文件到指定目录
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "cp /mnt/w10share/simkai.ttf /usr/share/zabbix/assets/fonts/")
# 替换配置文件
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "mv  /usr/share/zabbix/include/defines.inc.php /usr/share/zabbix/include/defines.inc.php.old")
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "cp /mnt/w10share/defined.inc.php /usr/share/zabbix/include/defines.inc.php")

#查看文件是否替换成功
    #cat /usr/share/zabbix/include/defines.inc.php | grep FONT_NAME
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "cat /usr/share/zabbix/include/defines.inc.php | grep FONT_NAME")
