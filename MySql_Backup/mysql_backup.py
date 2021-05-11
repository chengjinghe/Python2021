# -*- coding: latin-1 -*-
import configparser
import os
import time
import getpass

host = "192.168.208.240"
port = "3306"
db_user = "root"
db_pass = "ccc.!"
databases = ("test")
def get_dump(database):
    filestamp = time.strftime(r'/mnt/w10share','%Y-%m-%d-%I')
   # /mnt/w10share
    os.popen("mysqldump -h %s -P %s -u %s -p%s %s > %s.sql" % (host,port,db_user,db_pass,database,database+"_"+filestamp))
    print("\n|| Database dumped to "+database+"_"+filestamp+".sql || ")
if __name__=="__main__":
    for database in databases:
        get_dump(database)