# -*- coding: UTF-8 -*-
import paramiko
def sshCommand(hostname,port,username,password,command):
    sshClient = paramiko.SSHClient()

    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.load_system_host_keys()
    sshClient.connect(hostname,port,username,password)
    stdin,stdout,stderr = sshClient.exec_command(command)
    print (stdout.read())

if __name__=="__main__":
    sshCommand("192.168.208.240",22,"root","20knb328zabbix","mysqldump -u root -pccc.! zabbix > /mnt/w10share/2020-11-2-1zabbix.sql")  #  mysql - uroot - p123 测试 < test. sql 恢复文件路径  0201031-2zabbix.sql 恢复到zabbix数据中
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "uptime")  #查看电脑运行时长
#先接连接WIN10共享
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "mount -t cifs -o username="Administrator",password="ccc." //192.168.208.2/Zabbix_Mysql_Backup /mnt/w10share")

# 修复zabbix中文乱码问题
# 复制字体文件到指定目录
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "cp /mnt/w10share/simkai.ttf /usr/share/zabbix/assets/fonts/")
# 替换配置文件
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "mv  /usr/share/zabbix/include/defines.inc.php /usr/share/zabbix/include/defines.inc.php.old")
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "cp /mnt/w10share/defined.inc.php /usr/share/zabbix/include/defines.inc.php")

#查看文件是否替换成功
    #cat /usr/share/zabbix/include/defines.inc.php | grep FONT_NAME
    #sshCommand("192.168.208.240", 22, "root", "20knb328zabbix", "cat /usr/share/zabbix/include/defines.inc.php | grep FONT_NAME")
