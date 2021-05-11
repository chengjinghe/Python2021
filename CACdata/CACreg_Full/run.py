# -*- coding: UTF-8 -*-
import re,winreg,os
class CACdata():
    
    root = (r"D:\regchdir")#注册文件根目录
    rootlist = os.listdir(r"D:\regchdir")#注册文件列表
    no_root_path_1 = r'Software\BHDevelopGroup\Yishion'

    root_path = r'Software\BHDevelopGroup\Yishion\AlertReport'#注册表根目录
    DBType = 1
    DBname = "DBType"
    ODBname = "OtherDBConStr"
    LSSname = "LinkSQLString"
    autologin_name = "autologin"#REG_DOWORD
    autologin_value = 0
    connects_name = "connects"#REG_DOWORD
    connects_value = 
    DefaultAction_name = ""#REG_SZ
    defaultdatacenter_name = "默认"#REG_SZ
    savelogin_name = 

    def __init__(self,LinkSQLStringmunber=0,factorymunber=0,valuemunber=0):
        self.LinkSQLStringmunber = LinkSQLStringmunber
        self.factorymunber = factorymunber
        self.valuemunber = valuemunber
        # self.filepath = filepath
        # self.temp = temp
    
    #  写的入的值   
    def reg_value(self):
        return self.factory_value[self.valuemunber]
    
    #工厂名称
    def reg_run(self):

        for o1 in self.rootlist:
            filepath = os.path.join(self.root,o1)#获取文件路径
        
            with open(filepath) as filepathto:
                temp = filepathto.read()#读取文件数据
            factory_name = re.findall(r't\\[\s\S]*?]',temp)#获取需写的工厂名称
            factory_value = re.findall(r'"9D[\s\S]*?"',temp)#获取需写的入的值
            LinkSQLString = re.findall(r'"96[\s\S]*?="',temp)#匹配LinkSQLString的值
            reg_path = re.findall(r'Yishion\\[AlertR]*?eport\\',temp)#Yithion后的路径是否为Al
            no_AL = re.findall(r'on\\[\s\S]*?rt',temp)#非CAC默认工厂名称

            
            for AlertReport in reg_path:
                Al = reg_path[0][8:10] #路径切片判断是不为Al全部
                if Al == "Al":
                    cacname = []#名称列表
                    sn = 0 
                    for hostname in factory_name:
                        pass
                        # n1 = hostname[2:-1]
                        # key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,self.root_path)#主目录
                        # winreg.CreateKeyEx(key,n1) #生成对象
                        # cpath = os.path.join(self.root_path,n1)#对象路径
                        # wr = winreg.OpenKey(winreg.HKEY_CURRENT_USER,cpath,0,winreg.KEY_SET_VALUE) #   wr = 写入对象                 
                        # winreg.SetValueEx(wr,self.DBname,0,winreg.REG_DWORD,1)#写入DB的名称
                        # winreg.SetValueEx(wr,self.ODBname,0,winreg.REG_SZ,factory_value[sn])#写入ODB的值
                        # winreg.SetValueEx(wr,self.LSSname,0,winreg.REG_SZ,LinkSQLString[0]) #写入LinkSQLString的名称和值         
                        # #写入列表
                        # cacname.append(n1)
                        # sn += 1
                        # winreg.CloseKey(key)    

                else:
                    for_sn1 = 0
                for x in no_AL:
                    no_factory = x[0][3:0]                       
                    no_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,self.no_root_path_1)
                    winreg.CreateKeyEx(no_key,no_factory)
                    no_factory_path = os.path.join(self.no_root_path_1,no_factory)
                    no_wr = winreg.OpenKey(winreg.HKEY_CURRENT_USER,no_factory_path,0,winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(no_wr,self)
                    winreg.fu




o  = CACdata()
o.reg_run()
print("注册表写入完成")

