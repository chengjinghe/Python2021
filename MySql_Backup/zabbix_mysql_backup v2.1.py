import time,re,paramiko
networkdisk1 = r'//192.168.208.2/Zabbix_Mysql_Backup'
mount1 = 'mount -t cifs -o username="Administrator",password="ccc." //192.168.208.2/Zabbix_Mysql_Backup /mnt/w10' #挂载网络共享
tnow = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())#生成时间格式字符串
zabbix_sql_backup = 'mysqldump -u root -pccc.! zabbix > /mnt/w10/'+ str(tnow) +'-zabbix.sql'#备份保存路径
Dimission_sql_backup = 'mysqldump -u root -pccc.! Dimission > /mnt/w10/'+ str(tnow) +'-Dimission.sql'#备份保存路径
IP_sql_backup = 'mysqldump -u root -pccc.! IP > /mnt/w10/'+ str(tnow) +'-IP.sql'#备份保存路径
df = 'df'
def sshCommand(hostname,port,username,password,command):
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.load_system_host_keys()
    sshClient.connect(hostname,port,username,password)
    stdin,stdout,stderr = sshClient.exec_command(command)   
    s = stdout.read()
    return s 
if __name__ == "__main__":
    s1 = sshCommand("192.168.208.240",22,"root","zabbixc...!",df)
    r1 = re.findall(networkdisk1,str(s1))
    r1 = str(r1)
    r2 = r1[2:37]  
    if r2 == networkdisk1:
        sshCommand("192.168.208.240",22,"root","zabbixc...!",zabbix_sql_backup)
        sshCommand("192.168.208.240",22,"root","zabbixc...!",Dimission_sql_backup)
        sshCommand("192.168.208.240",22,"root","zabbixc...!",IP_sql_backup)
    else:
        #挂载网络共享
        sshCommand("192.168.208.240",22,"root","zabbixc...!",mount1)
        s3 = sshCommand("192.168.208.240",22,"root","zabbixc...!",df)
        r3 = re.findall(networkdisk1,str(s3))
        r3 = str(r3)
        r3 = r3[2:37] 
        if r3 == networkdisk1:
            sshCommand("192.168.208.240",22,"root","zabbixc...!",zabbix_sql_backup)
            sshCommand("192.168.208.240",22,"root","zabbixc...!",Dimission_sql_backup)
            sshCommand("192.168.208.240",22,"root","zabbixc...!",IP_sql_backup)
        else:
            print("网络错误")
