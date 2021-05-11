import pathlib
from shutil import copy
import shutil
import time,os
class Files():
    allfiles= []

    def __init__(self,soupath=None,backup_path=None):
        '''
        soupath 源路径
        backup_path 备份保存文件夹
        '''
        self.soupath = soupath
        self.backup_path = backup_path

    '''
    mt3d 处理三天以内的文件
    Path = 需要处理的文件夹目录
    name_fuffix = 文件后缀名 默认为'.sql'
    backup_path = 备份的文件的保存路径
    '''
    def showFile(self,name_suffix='',recursion=False,Day=1):
        '''
        name_suffix 显示文件的后缀名
        recursion 否是递归目录 默认为False
        day 显示多少天的以内的文件
        '''
        atime = 86400 #秒（一天86400）
        if recursion == False:
            allfile = sorted(pathlib.Path(self.soupath).glob('*{0}'.format(name_suffix)))#获取*.sql后缀所有文件路径
        elif recursion == True:
            allfile = sorted(pathlib.Path(self.soupath).glob('**/*{0}'.format(name_suffix)))
        localtime = time.time()#本地时间
        for file in allfile:
            filetime = os.stat(file)#获取时间
            Ttime = localtime - filetime.st_atime 
            if Day == 0:
               self.allfiles.append(file)
               print('0'*100)                     
            elif Ttime > atime*Day: # 
                self.allfiles.append(file)#访问时间大于三天以上的文件              
        return self.allfiles

    def backup(self,remove=False):
        '''
        remove 是否删除
        '''
        try:
            if self.backup_path == None:
                print('backup_path_error')
            else:
                for x in self.allfiles:
                    copy(x,self.backup_path)
                    if remove == True:
                        os.remove(x)
                        print('已经删除%s'%x)                       
        except Exception as e:
            print(e)

            
if __name__=='__main__':
    f = Files(soupath='D:\Zabbix_Mysql_Backup',backup_path=r'D:\Zabbix_Mysql_Backup\t')
    
    F1 = f.showFile(name_suffix='.sql',Day=3)
    f.backup(remove=True)