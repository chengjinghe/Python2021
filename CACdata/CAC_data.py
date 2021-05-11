# -*- coding: UTF-8 -*-
import re,winreg,os
class CACdata():
    with open(r"D:\Cac_reg_full.txt") as filepath:
        temp = filepath.read()#读取文件数据
    factory_name = re.findall(r't\\[\s\S]*?]',temp)#获取需写的工厂名称
    factory_value = re.findall(r'"9D[\s\S]*?"',temp)#获取需写的入的值
    LinkSQLString = re.findall(r'"96[\s\S]*?="',temp)
    root_path = r'Software\BHDevelopGroup\Yishion\AlertReport'#注册表根目录
    DBType = 1
    DBname = "DBType"
    ODBname = "OtherDBConStr"
    LSSname = "LinkSQLString"

    def __init__(self,filepath=filepath,temp=temp,LinkSQLStringmunber=0,factorymunber=0,valuemunber=0):
        self.LinkSQLStringmunber = LinkSQLStringmunber
        self.factorymunber = factorymunber
        self.valuemunber = valuemunber
        self.filepath = filepath
        self.temp = temp
    
    #  写的入的值   
    def reg_value(self):
        return self.factory_value[self.valuemunber]
    
    #工厂名称
    def reg_run(self):

        cacname = []#名称列表
        sn = 0 
        for hostname in self.factory_name:
            n1 = hostname[2:-1]
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,self.root_path)#主目录
            winreg.CreateKeyEx(key,n1) #生成对象
            cpath = os.path.join(self.root_path,n1)#对象路径
            wr = winreg.OpenKey(winreg.HKEY_CURRENT_USER,cpath,0,winreg.KEY_SET_VALUE) #   wr = 写入对象                 
            winreg.SetValueEx(wr,self.DBname,0,winreg.REG_DWORD,1)
            winreg.SetValueEx(wr,self.ODBname,0,winreg.REG_SZ,self.factory_value[sn])
            winreg.SetValueEx(wr,self.LSSname,0,winreg.REG_SZ,self.LinkSQLString[0])          
            #写入列表
            cacname.append(n1)
            sn += 1
            winreg.CloseKey(key)    

o  = CACdata()
o.reg_run()
print("注册表写入完成")

