# -*- coding: UTF-8 -*-
import os,time
from pathlib import Path
from shutil import copyfile

def Datatime(bbc):
    def d(*args):
        t1 = time.time()
        bbc(*args)
        return time.time() - t1
    return d

class Del():
    #备份文件存放路径
    # backup_dir = r"\\192.168.208.1\Python\factory_Sys"
    filePath=r"\\192.168.208.1\1.电脑部"
    def __init__(self,filePath=filePath):
        self.filePath = filePath

    @Datatime
    def __exe(self):
        #列出所有.exe的文件 不递归文件夹
        __exe = sorted(Path(self.filePath).glob('**/*.exe'))
        # print("exe已经调用")
        return __exe
        
    @Datatime  
    def __txt(self):
        #列出所有.txt的文件 不递归文件夹
        __txt = sorted(Path(self.filePath).glob('*/*.txt'))
        # print("txt已经调用")
        return __txt
    def __del_txt(self):
        #删除
        __os.remove(self.txt)
        #删除
    def __del_txt(self):
        __os.remove(self.exe)

    def __backup_files(self):
        pass

        # copyfile(self.filePath,self.backup_dir)
    @Datatime 
    def start(self):        
        return self.__exe()

        
a = Del()
print(a.start())


