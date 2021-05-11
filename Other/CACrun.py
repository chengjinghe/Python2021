import os,winreg


from CACdata import *

sys_time = 'yyyy-M-d'
class CACrun(CAC_data):

    root_path = r'Software\BHDevelopGroup\Yishion\AlertReport'
    reg_time_path = r'HKEY_CURRENT_USER\Control Panel\International'

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,root_path)#cac数据写入路径

    def __init__(self,key=key,name):
        self.key = key
        self.name = name

    def reg(self):
        winreg.CreateKey(self.name,self.name)

    def cpath(self):#路径名称
        os.path.join(self.root_path,self.name)
        
    def set_write_access(self):
        winreg.OpenKey(winreg.HKEY_CURRENT_USER,self.cpath,0,winreg.KEY_SET_VALUE)
    

        
print()