# -*- coding: utf-8 -*-
from pathlib import Path
from shutil import copyfile
import os,time,socket,sys,re
import multiprocessing
from shutil import copytree
from marsql import MarDB
from yishion.he_yishionRegedit import YshionRegedit
from yishion.he_yishionSys import YishionSys
from yishion.he_yishionTools import YishionTime
from yishion.he_psutil import yishionPsutil
from yishion.he_Auto import Auto

'''
v2.8.3 优化代码实现流程
 1 加入CAC物料系统，车辆管理系统安装
'''
localhostname = socket.gethostname()# 获取本地计算机名

# @property
def localip():
    '''获取本地IP地址'''
    try:
        ipconfig = os.popen('ipconfig')
        ipaddress_list = re.findall(r'[192]+\.+[168]+\.+[0-9]+\.+[0-9]*',ipconfig.read())#只匹配192.168.2xx.xxx网络端IP
        if ipaddress_list != None:
            try:
                return ipaddress_list[0]
            except Exception as e:
                print(e)
                return e
        else:
            return 'IP配置错误 或IP属于非感兴趣网段'
    except:
        return 'error'
local_ip = localip()

class Install(YishionSys,YishionTime,MarDB,YshionRegedit,yishionPsutil):
    '''软件安装脚本,writeDataBase 是否写入数据库'''
    def __init__(self,writeDataBase=True,database='DevOps'):
        super().__init__(database)
        self.writeDataBase = writeDataBase #Log write to database
        self.Work_directory_NetWork= r'\\192.168.208.1\Python'
        self.CACUpdate = r'\\192.168.0.17\CACUpdate'
        self.Program_Files = r'C:\Program Files'
        self.Program_Files_x86 = r"C:\Program Files (x86)"
        self.autoupdate_path =''#更新文件路径
        self.updatefile_name = 'autoupdate.exe'#系统更新更新文件名
    # 搜索工具软件(放大镜)
    def Locate32_software(self):
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

#实例化本地时间
    def localruntime(self):
        try:
            print('本次程序启动时间',self.currentTime)
            if self.writeDataBase == True:
                self.ssiinsert(host=localhostname,time=self.marTime)
            else:
                pass
        except:
            pass

#提示信息
    def info(self):
        print('''
                1,程序会自动跳过已经安装的系统，
                2,会自动打开SN文件,请手动关闭该文件
                ！请先输入192.168.0.17 用户名 ： Guest
                ！请先输入192.168.0.17 密码 ： Yscac2018
                ！请确保(0.17，208.1)网络共享能正常访问，否则程序将自动退出

                                更新版本时间 2021-6-20 HE
                                v2.8.3
                ''')

        info1 = "正在安装通用系统_请稍后!!!"
        info2 = "10秒后开始执行"
        print('{0:-^60}'.format(info1))
        print('{0:>35}'.format(info2))
        time.sleep(10)

# 通用系统安装
    def sys_install(self):    
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
                    print('系统安装错误，请手动安装')
                    ifosaccess_err = ('系统安装错误，请手动安装')
                    if self.writeDataBase == True:
                        self.ssiinsert(host=localhostname,error=ifosaccess_err+err,time=self.marTime)
                    else:
                        pass

                #执行公司通用系统安装

                sys_Nmae = []
                for sysname_index,name in enumerate(self.sysNameList()):
                    setup = name + '.exe'
                    sys_Nmae.append(setup)
                    #获取CAC安装文件路径
                    software_root_path = sorted(Path(Yishion_sys_path).glob(f"**/*{name}.exe"))#搜索排序指定后续名的软件
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
                            os.system(str(software_root_path[0]) +" /s")                                      
                            sys_install_values1 = (f"!!正在安装{name}!!!")
                            print(self.currentTime,sys_install_values1)
                            if self.writeDataBase == True:
                                self.ssiinsert(host=localhostname,message=str(sys_install_values1),time=self.marTime,ip=local_ip)    
                            else:
                                pass                             
                    except Exception as sys_install_err1:                  
                        sys_general_install_err = ("通用系统安装出错，请手动执行安装")
                        print(self.currentTime,sys_general_install_err,sys_install_err1)
                        if self.writeDataBase == True:
                            self.ssiinsert(host=localhostname,time=self.marTime,error=sys_general_install_err,ip=local_ip)
                        else:
                            pass
                
            else:
                print(self.currentTime,'Yishion_sys_path文件夹异常,请确认网络正常')
                if_Yishion_sys_path_err = ('Yishion_sys_path文件夹异常,请确认网络正常')
                if self.writeDataBase == True:
                    self.ssiinsert(host=localhostname,time=self.marTime,error=if_Yishion_sys_path_err,ip=local_ip)
                else:
                    pass
        except Exception as err:
            print(self.currentTime,'请确认网络正常',err)

        #打开序列号文件
        try:
            # os.popen(os.path.join(self.Work_directory_NetWork,"factory_Software","sn.txt"))
            keyfile_open_ok = ('序列号文件已成功打开')
            print(self.currentTime,keyfile_open_ok)
            if self.writeDataBase == True:
                self.ssiinsert(host=localhostname,time=self.marTime,message=keyfile_open_ok)
            else:
                pass
        except IOError as key_file_e:
            key_file_err = ('SN文件错误或不存在')
            print(self.currentTime,key_file_e)
            if self.writeDataBase == True:
                self.ssiinsert(host=localhostname,time=self.marTime,error=key_file_err)
            else:
                pass
    
    #系统更新函数
    def sys_update(self):           
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

#执行常办公软件安装
    def sftInstall(self,affirm):
        autoRunAllSftwarelist = ['WeChatSetup.exe','WeCom.exe','rtxcsetup.exe','realvncsetup.exe','sougouwubi.exe','AdbeRdr930.exe','pdfprochs.exe',
                            'zip360setup.exe','sougoupingying.exe','FirefoxSetup.exe','ChromeStandalone.exe','zzskylarinst-winc(192.168.0.36_80).exe']
        if os.access(self.sftNetworkRoot(),os.F_OK):
            try:            
                for nameindex,name in enumerate(autoRunAllSftwarelist):
                    os.system(str(os.path.join(self.sftNetworkRoot(),name)))
                    time.sleep(30)
                    #进程检测是否存活
                    while True:
                        affirm1 = affirm.get()#判断监控操作进程是否返回确认完成数据
                        if affirm1 == name:
                            break
                        pass              
                    if self.writeDataBase == True:
                        self.ssiinsert(host=localhostname,time=self.marTime,message=str(name),ip=local_ip)
                    else:
                        pass
            except Exception as err:
                Software_install_err = ("软件安装错误，请手动安装",err)
                print(self.currentTime,Software_install_err)
                if self.writeDataBase == True:
                    self.ssiinsert(host=localhostname,time=self.marTime,error=Software_install_err,ip=local_ip)
                else:
                    pass
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

Mar = Install(writeDataBase=False)#实例化 
autoinstall = Auto()
if __name__=='__main__':
    multiprocessing.freeze_support()
    network= r'\\192.168.208.1\Python'
    # synetwork = r'\\192.168.0.17\CACUpdate'
    # if os.access(network,os.F_OK) and os.access(synetwork,os.F_OK):
    if os.access(network,os.F_OK): #and os.access(synetwork,os.F_OK):
        # YshionRegedit.setDateTime
        # YshionRegedit.setIE208
        # YshionRegedit.setWindowsUAC
        # YshionRegedit.visualFXSetting
        # Mar.localruntime()
        # Mar.Locate32_software()
        # Mar.info()
        # Mar.sys_install()
        # print('正在完成系统安装...')
        # Mar.sys_update()
        # time.sleep(40)
        # print('准备执行进程清理...')
        # syskill = multiprocessing.Process(target=Mar.sysProckill)
        # syskill.start()
        # syskill.join()
        affirmQueue = multiprocessing.Queue()
        goInt = multiprocessing.Process(target=autoinstall.goInt,args=(affirmQueue,))
        sftinstall = multiprocessing.Process(target=Mar.sftInstall,args=(affirmQueue,))
        goInt.start()
        sftinstall.start()
        sftinstall.join()
    else:  
        Network_values = ('请检查网络或共享设置(0.17 和 208.1)，请手动执行软件安装，或稍后再试')
        print(Network_values) 
        time.sleep(10)
        sys.exit()
        