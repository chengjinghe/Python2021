# -*- coding: utf-8 -*-
from multiprocessing import Process as mP
from multiprocessing import Queue as mQ
from multiprocessing import freeze_support
from pathlib import Path
from shutil import copyfile,copytree
import os,time,socket,sys
from marsql import MarDB
from yishion.he_yishionRegedit import YshionRegedit
from yishion.he_yishionSys import YishionPath
from yishion.he_yishionTools import YishionTime
from yishion.he_psutil import yishionPsutil
from yishion.he_Auto import Auto
from yishion.he_SsiAutoSql import YishionSsiAutoSql
from yishion.he_yishionServices import winServices

print('正在检查系统...请稍后.')
localhostname = socket.gethostname()# 获取本地计算机名

def localip():
    '''获取本地IP地址'''
    timeout = 0
    while True:
        try:
            timeout += 1
            if timeout == 10:
                break
            time.sleep(1)
            y = yishionPsutil()
            if y.IPV4 == None:
                pass
            else:
                return y.IPV4.address
        except:
            return 'localip-error'
local_ip = localip()

class YishionInstall(YishionPath,YishionTime,MarDB,YshionRegedit,yishionPsutil):
    '''SsiAuto3.0'''
    def __init__(self,writeDataBase=True,database='DevOps'):
        super().__init__(database)
        self.auto = Auto()
        self.ssiautosql = YishionSsiAutoSql()
        self.writeDataBase = writeDataBase #Log write to database
        self.Work_directory_NetWork= self.pythonNetworkRoot()
        self.CACUpdate = self.getCACUpdatePath()
        self.Program_Files = r'C:\Program Files'
        self.Program_Files_x86 = r"C:\Program Files (x86)"
        self.autoupdate_path =''#更新文件路径
        self.updatefile_name = 'autoupdate.exe'#系统更新更新文件名
        self.kiilList = [] #结束的任务进程名表

    def locate32Software(self):
        '''局域网文件搜索工具复制到本地目录'''       
        try:
            Locate32_net_path = os.path.join(self.Work_directory_NetWork,'Locate32')#Locate32 软件网络保存的路径
            Locate32_local_path = os.path.join(self.Program_Files,'Locate32')#本地Locate32软件保存路径
            if os.access(Locate32_local_path,os.F_OK):
                print(self.currentTime,'locate32已文件夹存在')
            else:
                copytree(Locate32_net_path,Locate32_local_path)#复制locate32程序文件到本地
                print(f'{self.Program_Files}\Locate32--放大镜搜索工具-已复制完成')
                locate32_lnk = os.path.join(self.get_desktop,'locate32.lnk')#生成locate32.exe桌面快捷方式路径
                os.symlink(os.path.join(Locate32_local_path,'locate32.exe'),locate32_lnk)#创建locate32.exe桌面快捷方式
                # os.popen(os.path.join(Locate32_local_path,'locate32.exe'))#启动搜索工具软件
        except Exception as Locate32_copy_err:
            print(self.currentTime,Locate32_copy_err)

    def systematicInspection(self):
        '''安装路径检查'''    
        Yishion_sys_path = os.path.join(self.Work_directory_NetWork,'factory_Sys')
        try:
            if os.access(Yishion_sys_path,os.F_OK):
                #判断X86文件在存在
                try:
                    #Program Files (x86)
                    if os.access(self.Program_Files_x86,os.F_OK):
                        self.autoupdate_path = self.Program_Files_x86#确定软件安装路径赋值给全局
                        print(self.currentTime,self.Program_Files_x86)
                        if self.writeDataBase == True:
                            self.ssiinsert(host=localhostname,message=self.Program_Files_x86,time=self.marTime,ip=local_ip)
                        else:
                            pass
                    #Program Files
                    else:
                        self.autoupdate_path = self.Program_Files#确定软件安装路径赋值给全局
                        print(self.currentTime,self.Program_Files)
                        if self.writeDataBase == True:
                            self.ssiinsert(host=localhostname,message=self.Program_Files,time=self.marTime,ip=local_ip)
                        else:
                            pass
                   
                except Exception as err:
                    print('系统安装错误，请手动安装',err)
                    ifosaccess_err = ('系统安装错误，请手动安装')
                    if self.writeDataBase == True:
                        self.ssiinsert(host=localhostname,error=ifosaccess_err+err,time=self.marTime)
                    else:
                        pass
        except Exception as e:
            print('systematicInspection',e)

    def internalSystemInstall(self):
            Yishion_sys_path = os.path.join(self.Work_directory_NetWork,'factory_Sys')
            try:    
                for sysname_index,name in enumerate(self.sysNameList()):
                    #获取CAC安装文件路径
                    softwareName = os.path.join(Yishion_sys_path,name +'.exe')
                    Program_Files = os.path.join(self.Program_Files,self.SyslocalRootPath()[sysname_index])#C:\Program Files 
                    Program_Files_x86 = os.path.join(self.Program_Files_x86,self.SyslocalRootPath()[sysname_index])#C:\Program Files (x86)
                    #执行安装
                    try:
                        if os.path.exists(Program_Files) or os.path.exists(Program_Files_x86):#检查要安装的系统是否已经存在
                            sys_install_values = (f"已经安装{name}，已经成功跳过")
                            print(self.currentTime,sys_install_values,self.marTime)
                            if self.writeDataBase == True:
                                self.ssiinsert(host=localhostname,message=sys_install_values,time=self.marTime,ip=local_ip)       #写入mariadb 数据库    
                            else:
                                pass                  
                        else:
                            os.system(str(softwareName) +" /s")                                      
                            sys_install_values1 = (f"!!!正在安装{name}!!!")
                            print(self.currentTime,sys_install_values1)
                            if self.writeDataBase == True:
                                self.ssiinsert(host=localhostname,message=str(softwareName),time=self.marTime,ip=local_ip)    
                            else:
                                pass                             
                    except Exception as sys_install_err1:                  
                        sys_general_install_err = ("通用系统安装出错，请手动执行安装")
                        print(self.currentTime,sys_general_install_err,sys_install_err1)
                        if self.writeDataBase == True:
                            self.ssiinsert(host=localhostname,time=self.marTime,error=sys_general_install_err,ip=local_ip)
                        else:
                            pass
            except Exception as err:
                print(self.currentTime,'请确认网络正常',err)

    def internalSystemAutoUpdata(self):
        '''以纯内部系统更新'''           
        try:
            full_update_file_path = sorted(Path(self.autoupdate_path).glob(f"**/{self.updatefile_name}"))#搜索本地更新文件所在路径
            banfangpath_file_local = os.path.join(self.Program_Files,"dsg","autoupdateNew.exe")#板房系统更新文件非X86文件夹
            banfangupdate_file_CACUpdate_path = os.path.join(self.CACUpdate, "板房系统","板房系统安装目录","autoupdateNew.exe")
            banfang_Program_Files_x86 = os.path.join(self.Program_Files_x86, "dsg","autoupdateNew.exe")#板房系统更新文件非文件夹
            #执行其他系统更新
            try:
                for updataindex,updatafile in enumerate(full_update_file_path):
                    os.popen(str(updatafile))
                    time.sleep(0.3)
                    updatavalues = (f"正在更新{updatafile}")
                    print(self.currentTime,updatavalues)
                    if self.writeDataBase == True:                
                        self.ssiinsert(host=localhostname,time=self.marTime,message=updatavalues,ip=local_ip)
                    else:
                        pass
            except:
                sys_updata_Err_values1 = ('系统更新失败，请手动检查更新')
                print(self.currentTime,sys_updata_Err_values1)
                if self.writeDataBase == True:
                    self.ssiinsert(host=localhostname,time=self.marTime,error=sys_updata_Err_values1,ip=local_ip)
                else:
                    pass
            #复制板房更新文件到本地
            try:
                if os.access(self.Program_Files,os.F_OK):
                    #复制板房更新文件到本地
                    copyfile(banfangupdate_file_CACUpdate_path,banfang_Program_Files_x86)
                    #执行板房文件更新
                    os.popen(banfang_Program_Files_x86)
                    copy_banfang_updata_x32_ok_values1 = ("板房更新文件，复制到32位文件夹成功")
                    print(self.currentTime,copy_banfang_updata_x32_ok_values1)
                    if self.writeDataBase == True:
                        self.ssiinsert(host=localhostname,time=self.marTime,message=copy_banfang_updata_x32_ok_values1,ip=local_ip)
                    else:
                        pass
                else:
                    copyfile(banfangupdate_file_CACUpdate_path,banfangpath_file_local)
                    copy_banfang_updata_x64_ok_values1 = ("板房更新文件，复制到64位文件夹成功")
                    print(self.currentTime,copy_banfang_updata_x64_ok_values1)
                    os.popen(banfangpath_file_local)
                    if self.writeDataBase == True:
                        self.ssiinsert(host=localhostname,time=self.marTime,message=copy_banfang_updata_x64_ok_values1,ip=local_ip)
                    else:
                        pass
            except Exception as e:           
                banfang_updata_Err1_values1 = ("板房更新文件复制失败，请手动复制更新")
                print(self.currentTime,banfang_updata_Err1_values1,e)
                if self.writeDataBase == True:
                    self.ssiinsert(host=localhostname,time=self.marTime,error=banfang_updata_Err1_values1,ip=local_ip)
                else:
                    pass
        except Exception as err1:
            update_err_values1 = ("更新文件路径查询错误")
            print(self.currentTime,update_err_values1,err1)
            if self.writeDataBase == True:
                self.ssiinsert(host=localhostname,time=self.marTime,error=err1,ip=local_ip)
            else:
                pass

    def commonSoftware(self,stopSignal):
        '''以纯内部通用办公软件安装'''
        autoRunAllSftwarelist = self.ssiautosql.ssiAutoQuery('autoRunAllSftwarelist')
        if os.access(self.sftNetworkRoot(),os.F_OK):
            try: 
                self.auto.setDisPlay()#设置屏幕分辨率为指定       
                for nameindex,name in autoRunAllSftwarelist:
                    if name == 'Setup.exe':
                        os.popen(str(self.office2007Path()))
                        self.auto.goInt(procName=name)
                        self.kiilList.append(name)
                    else:
                        os.popen(str(os.path.join(self.sftNetworkRoot(),name)))
                        self.auto.goInt(procName=name)
                        self.kiilList.append(name) #将进程添加到进程结束列表       
                    if self.writeDataBase == True:
                        self.ssiinsert(host=localhostname,time=self.marTime,message=str(os.path.join(self.sftNetworkRoot(),name)),ip=local_ip)
                    else:
                        pass
                stopSignal.put('Ok')
                print('stopSignal已发送！')
            except Exception as err:
                Software_install_err = ("软件安装错误，请手动安装",err)
                print(self.currentTime,Software_install_err)
                if self.writeDataBase == True:
                    self.ssiinsert(host=localhostname,time=self.marTime,error=Software_install_err,ip=local_ip)
                else:
                    pass
            finally:
                self.auto.setDisPlay(setBackupDisplay=True)#还原屏幕分辨率
        else:
            software_patn_err = ('请确认网络文件夹factory_Software或共享正常')
            print(self.currentTime,software_patn_err)
            if self.writeDataBase == True:
                self.ssiinsert(host=localhostname,time=self.marTime,error=software_patn_err,ip=local_ip)
            else:
                pass
    
    def sysProckill(self):
        '''结果指定的进程'''
        for proc in self.SyslocalRootPath():
            procNmae = proc.split('\\')[-1]
            try:
                self.kill(procNmae)
                print(f"{procNmae} 进程已执行完成清理")
            except Exception as e:
                time.sleep(2)
                self.kill(procNmae)
        print('进程已清理！')
    
    def stubbornProcesskill(self,stopSignal):
        '''清除多余的进程'''
        sn = 0
        stubbornProcesslist = self.ssiautosql.ssiAutoQuery(procName='stubbornProcesslist')
        while True:
            # print(f'清理顽固进程 {sn} 次')
            sn += 1
            time.sleep(1)
            if stubbornProcesslist == None:
                pass
            else:
                for stubbornProcesslistIndex,ProcessName in stubbornProcesslist:
                    try:
                        self.kill(ProcessName)
                    except:
                        time.sleep(2)
                        self.kill(ProcessName)
            if not stopSignal.empty() or sn == 10:
                print('stopSignal接收信号停止')
                break
                
    def checkProcKiil5sec(self):
        '''每5秒结束一次kill列表进程'''
        while True:
            time.sleep(5)
            for procname in self.kiilList:
                try:
                    self.kill(procname)
                except Exception as e:
                    time.sleep(2)
                    self.kill(procname)
            if len(self.kiilList) <= 10:
                break

Mar = YishionInstall(writeDataBase=True)#实例化 
if __name__ == '__main__':
    netWorkPath = r'\\192.168.0.17\CACUpdate'
    if os.access(netWorkPath,os.F_OK):
        # freeze_support()
        regSetting = YshionRegedit()
        # stopSignal = mQ()
        # regSetting.setDateTime
        # regSetting.setIE208
        # regSetting.setWindowsUAC
        # regSetting.visualFXSetting
        # Mar.systematicInspection()
        # Mar.internalSystemInstall()
        # Mar.internalSystemAutoUpdata()
        # print('准备执行进程清理...')
        # time.sleep(60)
        # Mar.sysProckill()
        # killproc1 = mP(target=Mar.checkProcKiil5sec)
        # killproc1.start()
        # sftIn1 = mP(target=Mar.commonSoftware,args=(stopSignal,))
        # sftIn1.start()
        # stubbornProcesskill = mP(target=Mar.stubbornProcesskill,args=(stopSignal,))
        # stubbornProcesskill.start()
        # regSetting.setCacGroupData
        # win10services =  winServices()
        # win10services.setConfigService()
    else:  
        Network_values = ('请检查网络或共享设置(0.17 和 208.1)，请手动执行软件安装，或稍后再试')
        print(Network_values) 
        time.sleep(10)
        sys.exit()

