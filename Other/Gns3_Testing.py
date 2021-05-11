# -*- coding: UTF-8 -*-
import paramiko
import time
from getpass import getpass



username = 'admin'
password = 'admin'
tnow = time.strftime("%Y-%m-%d %H-%M-%S",time.localtime()) # 定义时间

print (tnow)
DEVICE_LIST = open(r"D:\backup\cisco\208-112\Test_route_list.txt") #设备IP地址列表文件
for RTR in DEVICE_LIST:
    RTR = RTR.strip()
    print('\n### Connecting to the device' + RTR +  '###\n')
    SESSION = paramiko.SSHClient()
    SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SESSION.connect(RTR,port=22,username=username,password=password)
    DEVICE_ACCESS = SESSION.invoke_shell()
    DEVICE_ACCESS.send(b'terminal len 0\n')
    DEVICE_ACCESS.send(b'show run\n')
    time.sleep(3)
    
    output = DEVICE_ACCESS.recv(65000)
    print (output.decode('ascii'))
    #filename = "ROUTER_" + RTR + '_' + str(tnow)
    SAVE_FILE = open(r'D:\backup\cisco\208-112\'Test-Router_Config'+ RTR +'_'+ str(tnow)+'.txt','w+')
    SAVE_FILE.write(output.decode('ascii'))
    SAVE_FILE.close 



name = str(tnow)+zabbix.sql


