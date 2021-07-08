import re,paramiko,time
from yishion.he_yishionTools import YishionTime
from he_email import Mail
class YishionMariadbBackup():
    mail = Mail()
    fileName = YishionTime()
    Exec = 'mysqldump -u root -pccc.!'
    host = '192.168.208.240'
    port = 22
    user = 'root'
    password = 'zabbixc...!'
    def __init__(self,sendMail=True):
        self.sendMail = sendMail

    def sshCommand(self,hostname,port,username,password,command):
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.load_system_host_keys()
        sshClient.connect(hostname,port,username,password)
        stdin,stdout,stderr = sshClient.exec_command(command)
        return stdout

    def isBackupPathOk(self):
        '''确定网络共享路径正常'''
        backupPath = r'//192.168.208.2/Zabbix_Mysql_Backup'
        setMount = 'mount -t cifs -o username="Administrator",password="ccc." //192.168.208.2/Zabbix_Mysql_Backup /mnt/w10' #挂载网络共享
        diskList = self.sshCommand(hostname=self.host,port=self.port,username=self.user,password=self.password,command='df')
        data = re.findall(backupPath,str(diskList.read()))
        r2 = str(data)[2:37] 
        if r2 == backupPath :
            pass
        else:
            self.sshCommand(hostname=self.host,port=self.port,username=self.user,password=self.password,command=setMount)

    def zabbixBackup(self):
        self.isBackupPathOk()
        zabbixSqlbackupExec = f'''{self.Exec} zabbix > /mnt/w10/{self.fileName.fileNameTime}-zabbix.sql'''#备份保存路径
        self.sshCommand(hostname=self.host,port=self.port,username=self.user,password=self.password,command=zabbixSqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='zabbix数据库备份')

    def devOpsBackup(self):
        self.isBackupPathOk()
        devOpsSqlbackupExec = f'''{self.Exec} DevOps > /mnt/w10/{self.fileName.fileNameTime}-DevOps.sql'''#备份保存路径
        self.sshCommand(hostname=self.host,port=self.port,username=self.user,password=self.password,command=devOpsSqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='devOps数据库备份')        
    
    def ssiAutoWin10Backup(self):
        self.isBackupPathOk()
        ssiAutoWin10SqlbackupExec = f'''{self.Exec} SsiAutoWin10 > /mnt/w10/{self.fileName.fileNameTime}-SsiAutoWin10Backup.sql'''#备份保存路径
        self.sshCommand(hostname=self.host,port=self.port,username=self.user,password=self.password,command=ssiAutoWin10SqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='ssiAutoWin10数据库备份')

    def ssiAutoWin7Backup(self):
        self.isBackupPathOk()
        ssiAutoWin7SqlbackupExec = f'''{self.Exec} SsiAutoWin7 > /mnt/w10/{self.fileName.fileNameTime}-SsiAutoWin7.sql'''#备份保存路径
        print(ssiAutoWin7SqlbackupExec)
        self.sshCommand(hostname=self.host,port=self.port,username=self.user,password=self.password,command=ssiAutoWin7SqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='ssiAutoWin7数据库备份')
if __name__ == "__main__":
    sy = YishionMariadbBackup()
    print('正在备份...请稍后')
    sy.ssiAutoWin7Backup()
    time.sleep(5)
    sy.ssiAutoWin10Backup()
    time.sleep(5)
    sy.devOpsBackup()
    time.sleep(5)
    sy.zabbixBackup()
    print('备份已完成！')
