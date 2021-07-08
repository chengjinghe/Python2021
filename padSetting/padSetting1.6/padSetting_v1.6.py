# -*- coding: utf-8 -*-
from shutil import rmtree
from shutil import copyfile
from shutil import copytree
import os,time,sys
from yishion.he_yishionRegedit import YshionRegedit
from he_padpowerSetting import PadPowerSetting
from he_YishionNetPath import FactoryErpPath
print('''
            提示！
    如有报错，请右键以管理员的方式运行！
    CMD报错，需要将本程序复制到本地再运行
               2021-6-16   ver 1.6  

''')

class padSetting(FactoryErpPath):
    def __init__(self):
        super().__init__()
        self.factoryNetPath = os.path.join(self.networkPath208_1,self.pythonpath,self.factorypath)
        self.localFactoryEerPath = os.path.join('C:\\','FactoryERP')
        self.localShutDownFile = os.path.join('c:\\','shutdown.bat')
        self.shutDownNetFile = os.path.join(self.networkPath208_1,self.pythonpath,'shutdown.bat')
        self.FactoryERP_lnk = os.path.join(regedit.get_desktop,'FactoryERP.lnk')

    @property
    def copyFacetry(self):
        '''复制设置工厂扫描系统'''
        try:

            if os.path.isdir(self.localFactoryEerPath):#判断本地是否已经存在FactoryERP目录
                try:
                    rmtree(self.localFactoryEerPath,ignore_errors=True)#删除原来的目录
                    print('正在复制文件...')
                    copytree(self.factoryNetPath,self.localFactoryEerPath)#复制新的FactoryERP目录文件到本地
                    if os.path.isfile(self.FactoryERP_lnk):#桌面是否FactoryERP有快捷方式
                        os.remove(self.FactoryERP_lnk)#删除桌面现在的FactoryERP快捷方式
                except Exception as e1:
                    print(e1,'10001')
            else:
                try:
                    print('正在复制文件...')
                    copytree(self.factoryNetPath,self.localFactoryEerPath)#复制新的FactoryERP目录文件到本地
                    print('FactoryERP目录已经制','*'*10)
                except Exception as e:
                    print('FactoryERP目录复制失败 ','*'*10,e)
        except:
            pass
    def copySetFile(self):
        # '''复制关机脚本，创建工厂扫描系统快捷方式'''    
            for file in (self.FactoryERP_lnk,self.shutDownNetFile):
                    if file == self.FactoryERP_lnk:
                        try:
                            if os.path.isfile(file):
                                os.remove(file)
                                os.symlink("c:\FactoryERP\StartERP2.exe",self.FactoryERP_lnk)
                                print('FactoryERP快捷方式已创建完成','*'*10)
                            else:
                                os.symlink("c:\FactoryERP\StartERP2.exe",self.FactoryERP_lnk)
                                print('FactoryERP快捷方式已创建完成','*'*10)
                        except Exception as e1 :
                            print('FactoryERP快捷方式无法创建',e1,'*'*10)
                    elif file == self.localShutDownFile:
                        try: 
                            if os.path.isfile(file):
                                os.remove(file)                  
                                copyfile(self.shutDownNetFile,self.localShutDownfile)
                                print('关机脚本文件已复制...')
                            else:
                                copyfile(self.shutDownNetFile,self.localShutDownfile)
                                print('关机脚本文件已复制...')
                        except Exception as e2:
                            print('10002')
                    else:
                        pass
    @property               
    def schAutoShudown(self):
        '''创建计划关机任务'''
        try:
            os.popen('''schtasks /create /sc weekly /d mon,tue,wed,thu,fri,sat /tn "autoShutdown" /tr "c:\shutdown.bat" /st 23:40 /np''')
            print('关机任务创建完成')
        except:
            print('请注意,关机脚本创建失败！')

if __name__ == '__main__':
    regedit = YshionRegedit()
    pad = padSetting()
    power = PadPowerSetting()
    regedit.setWindowsUAC
    regedit.setDateTime
    regedit.setIE208
    regedit.visualFXSetting
    power.setPadPowerSetting#激活pad专用设置
    regedit.timezaone#设置时区为中国
    regedit.sec#隐藏任务搜索框
    pad.copyFacetry#复制工厂系统文件到本地
    pad.copySetFile()#复制设置文件
    pad.schAutoShudown#创建自动关机脚本
    regedit.get_and_setTime#同步时间
    os.popen(r"c:\FactoryERP\StartERP2.exe")#启动程序
    print('设置已完成...','*'*10)
    time.sleep(2)
    sys.exit()