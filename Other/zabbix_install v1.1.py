import time,re,paramiko,mariadb
networkdisk1 = r'//192.168.208.2/Zabbix_Mysql_Backup'
mount1 = 'mount -t cifs -o username="Administrator",password="ccc." //192.168.208.2/Zabbix_Mysql_Backup /mnt/w10' #挂载网络共享
tnow = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())#生成时间格式字符串
zabbix_sql_backup = 'mysqldump -u root -pccc.! zabbix > /mnt/w10/'+ str(tnow) +'-zabbix.sql'#备份保存路径
test_sql_backup = 'mysqldump -u root -pccc.! test > /mnt/w10/'+ str(tnow) +'-test.sql'#备份保存路径
df = 'df'
ping = 'ping -c 4 www.baidu.com'
uptime = 'uptime'

def marswl(sql):
    try:
        conn = mariadb.connect(
            user="root",
            password="db_user_passwd",
            host="192.168.208.167",
            port=3306,
            database="zabbix"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    

zabbix_install_command_list = [
    'ping -c 4 www.baidu.com',
    'rpm -Uvh https://repo.zabbix.com/zabbix/4.4/rhel/7/x86_64/zabbix-release-4.4-1.el7.noarch.rpm',
    'yum celan all',
    'yum install zabbix-server-mysql -y  zabbix-web-mysql -y zabbix-agent -y mariadb-server -y',
    'systemctl start mariadb',
    'systemctl status mariadb',
    'systemctl status mariadb',
    'systemctl enable mariadb',
    'systemctl disble firewalld.service'
]

#安装数据库
def sshCommand(hostname,port,username,password,command):
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.load_system_host_keys()
    sshClient.connect(hostname,port,username,password)
    stdin,stdout,stderr = sshClient.exec_command(command)   
    s = stdout.read()
    return s 
if __name__ == "__main__":
    for exec_command1 in zabbix_install_command_list:
        s1 = sshCommand("192.168.208.167",22,"root","ccc.",exec_command1)
        s1 = str(s1,encoding='utf-8')
        print(s1)
    # s1 = sshCommand("192.168.208.167",22,"root","zabbixc...!",ping)
    # s1 = sshCommand("192.168.208.167",22,"root","ccc.",yum_yuan)#ok 设置zabbix 安装yum源
    # s1 = sshCommand("192.168.208.167",22,"root","ccc.",yum_celan_all)#
    # s1 = sshCommand("192.168.208.167",22,"root","ccc.",install_mariadb)#安装zabbix mariadb 
    # s1 = sshCommand("192.168.208.167",22,"root","ccc.",start_mariadb)#启动mariadb
    # s1 = sshCommand("192.168.208.167",22,"root","ccc.",status_mariadb)#查看mariadb状态
    # s1 = sshCommand("192.168.208.167",22,"root","ccc.",host_start_enable_maradb)#开机启动mariadb
    # s1 = sshCommand("192.168.208.167",22,"root","ccc.",host_start_disable_firwalld)#开机禁用防火墙
    # s1 = str(s1,encoding='utf-8')
    # print(s1)

    