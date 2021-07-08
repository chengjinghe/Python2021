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
        self.sshClient = paramiko.SSHClient()
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshClient.load_system_host_keys()
        self.sshClient.connect(username=self.user,hostname=self.host,port=self.port,password=self.password)

    def isBackupPathOk(self):
        '''确定网络共享路径正常'''
        backupPath = r'//192.168.208.2/Zabbix_Mysql_Backup'
        setMount = 'mount -t cifs -o username="Administrator",password="ccc." //192.168.208.2/Zabbix_Mysql_Backup /mnt/w10' #挂载网络共享
        stdin,stdout,stderr = self.sshClient.exec_command(command='df')
        data = re.findall(backupPath,str(stdout.read()))
        r2 = str(data)[2:37] 
        if r2 == backupPath :
            print(f'ok{self.fileName.marTime}')
            pass
        else:
            self.sshClient.exec_command(command=setMount)

    def zabbixBackup(self):
        self.isBackupPathOk()
        zabbixSqlbackupExec = f'''{self.Exec} zabbix > /mnt/w10/{self.fileName.fileNameTime}-zabbix.sql'''#备份保存路径
        self.sshClient.exec_command(command=zabbixSqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='zabbix数据库备份')

    def devOpsBackup(self):
        self.isBackupPathOk()
        devOpsSqlbackupExec = f'''{self.Exec} DevOps > /mnt/w10/{self.fileName.fileNameTime}-DevOps.sql'''#备份保存路径
        self.sshClient.exec_command(command=devOpsSqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='devOps数据库备份')        
    
    def ssiAutoWin10Backup(self):
        self.isBackupPathOk()
        ssiAutoWin10SqlbackupExec = f'''{self.Exec} SsiAutoWin10 > /mnt/w10/{self.fileName.fileNameTime}-SsiAutoWin10Backup.sql'''#备份保存路径
        self.sshClient.exec_command(command=ssiAutoWin10SqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='ssiAutoWin10数据库备份')

    def ssiAutoWin7Backup(self):
        self.isBackupPathOk()
        ssiAutoWin7SqlbackupExec = f'''{self.Exec} SsiAutoWin7 > /mnt/w10/{self.fileName.fileNameTime}-SsiAutoWin7.sql'''#备份保存路径
        print(ssiAutoWin7SqlbackupExec)
        self.sshClient.exec_command(command=ssiAutoWin7SqlbackupExec)#执行zabbix数据库备份
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='ssiAutoWin7数据库备份')
    
    def mysqlBackup(self):
        self.isBackupPathOk()
        mysqlBackupExec = f'''{self.Exec} mysql > /mnt/w10/{self.fileName.fileNameTime}-mysql.sql'''
        self.sshClient.exec_command(command=mysqlBackupExec)
        if self.sendMail == True:
            self.mail.sendmail(messages=f'发送时间{self.fileName.currentTime} 数据库备份完成',title='mysql数据库备份')
        pass
if __name__ == "__main__":
    sy = YishionMariadbBackup(sendMail=False)
    sy.isBackupPathOk()
