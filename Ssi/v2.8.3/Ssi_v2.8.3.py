
from pathlib import Path, PureWindowsPath
from shutil import copyfile
import os,time,winreg,socket,sys,re
from pathlib import PurePath
from shutil import copytree
from marsql import MarDB
from he_psutil import IP_Psutil
from yishionreg import Reg
reg = Reg()
marsql = MarDB()
IP_name = IP_Psutil()
'''
v2.8.3 优化代码实现流程
 1 加入CAC物料系统，车辆管理系统安装
'''
localhostname = socket.gethostname()# 获取本地计算机名

# @property
def localip():
    '''
    获取本地IP地址
    '''
    ipconfig = os.popen('ipconfig')
    ipaddress_list = re.findall(r'[192]+\.+[168]+\.+[2][0-3][0-9]+\.+[0-9]*',ipconfig.read())#只匹配192.168.2xx.xxx网络端IP
    if ipaddress_list != None:
        return ipaddress_list[0]
    else:
        return 'IP配置错误 或IP属于非感兴趣网段'

local_ip = localip()
class Install_all():
    '''
    #软件安装脚本
    '''
    def __init__(self,Database_write=True):
        '''
        Database_write 是否写入数据库
        '''
        self.Database_write = Database_write #Log write to database
        self.Work_directory_NetWork= r'\\192.168.208.1\Python'
        self.CACUpdate = r'\\192.168.0.17\CACUpdate'
        self.Program_Files = r'C:\Program Files'
        self.Program_Files_x86 = r"C:\Program Files (x86)"
        self.autoupdate_path =''#更新文件路径
        self.updatefile_name = 'autoupdate.exe'#系统更新更新文件名

    @property
    def current_time(self):
        '''
        返回 Y-m-d H-M-S:时间样式
        '''
        localtime = time.localtime()
        Rtime = time.strftime("%Y-%m-%d %H-%M-%S:", localtime)
        return Rtime

    @property
    def marTime(self):
        '''
        返回 YmdHMS 时间样式
        '''
        localtime = time.localtime()
        rRtime = time.strftime("%Y%m%d%H%M%S", localtime)
        return rRtime

    # 搜索工具软件(放大镜)
    def Locate32_software(self):
        '''
        局域网文件搜索工具复制到本地目录
        '''       
        try:
            Locate32_net_path = os.path.join(self.Work_directory_NetWork,'Locate32')#Locate32 软件网络保存的路径
            Locate32_local_path = os.path.join(self.Program_Files,'Locate32')#本地Locate32软件保存路径
            if os.access(Locate32_local_path,os.F_OK):
                print('locate32已文件夹存在')
            else:
                copytree(Locate32_net_path,Locate32_local_path)#复制locate32程序文件到本地
                print(f'{self.Program_Files}\Locate32--放大镜搜索工具-已复制完成')
                locate32_lnk = os.path.join(reg.get_desktop,'locate32.lnk')#生成locate32.exe桌面快捷方式路径
                os.symlink(os.path.join(Locate32_local_path,'locate32.exe'),locate32_lnk)#创建locate32.exe桌面快捷方式
                os.popen(os.path.join(Locate32_local_path,'locate32.exe'))#启动搜索工具软件
        except Exception as Locate32_copy_err:
            print(Mar.current_time,Locate32_copy_err)

#修改本地时间显示样式
    def areg(self):
        '''
        修改本地系统的时间连接符为-（横线）
        '''
        try:
            reg_time_path = r'Control Panel\International'
            time_reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg_time_path,0,winreg.KEY_WRITE)
            winreg.SetValueEx(time_reg,'sShortDate','',winreg.REG_SZ,'yyyy-M-d')
            winreg.FlushKey(time_reg)
            winreg.CloseKey(time_reg)
            timeFormat = '时间格式已经修改为---'
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=timeFormat)
            else:
                pass
            print(timeFormat)
        except OSError as winreg_error:
            reg_err_values = (Mar.current_time,winreg_error)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,error=winreg_error,time=Mar.marTime)#写入mariadb 数据库
            else:
                pass
            print(reg_err_values)
            print("系统时间样式未修改")

        #修改windows10用户帐户控制
        try:
            reg_user_UAC= r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
            user_uac = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,reg_user_UAC,0,winreg.KEY_WRITE)
            winreg.SetValueEx(user_uac,'ConsentPromptBehaviorAdmin','',winreg.REG_DWORD,0)
            winreg.SetValueEx(user_uac,'PromptOnSecureDesktop','',winreg.REG_DWORD,0)
            winreg.FlushKey(user_uac)
            winreg.CloseKey(user_uac)
            win_uac = 'windows10用户帐户控制-已改为最低'
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=win_uac)
            else:
                pass
            print(win_uac)
        except OSError as user_uac_err:
            print(Mar.current_time,user_uac_err,"用户帐户控制未修改")
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,error=user_uac_err,time=Mar.marTime)
            else:
                pass
        #修IE设置——
        try:
            IERanges = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
            ie_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,IERanges,0,winreg.KEY_WRITE)
            ie_key = winreg.CreateKeyEx(ie_key,'Range1')#创建项
            winreg.SetValueEx(ie_key,':Range','',winreg.REG_SZ,'192.168.208.1')
            winreg.SetValueEx(ie_key,'file','',winreg.REG_DWORD,1)
            winreg.FlushKey(ie_key)
            winreg.CloseKey(ie_key)
        except OSError as IERanges_err:
            print(Mar.current_time,IERanges_err,"IE设置—未修改")
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=IERanges_err)

#实例化本地时间
    def localruntime(self):
        try:
            Starttime = Mar.current_time
            print('本次程序启动时间',Starttime)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime)
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

                                更新版本时间 2021-5-20 HE
                                v2.8.2
                ''')

        info1 = "正在安装通用系统_请稍后!!!"
        info2 = "10秒后开始执行"
        print('{0:-^60}'.format(info1))
        print('{0:>40}'.format(info2))
        time.sleep(10)

# 通用系统安装和更新
    def sys_install(self):    
        Yishion_sys_path = os.path.join(self.Work_directory_NetWork,'factory_Sys')
        try:
            if os.access(Yishion_sys_path,os.F_OK):
                #判断X86文件在存在
                try:
                    #Program Files (x86)
                    if os.access(self.Program_Files_x86,os.F_OK):
                        self.autoupdate_path = self.Program_Files_x86#确定软件安装路径赋值给全局
                        print(Mar.current_time,self.Program_Files_x86)
                        if self.Database_write == True:
                            marsql.ssiinsert(host=localhostname,message=self.Program_Files_x86,time=Mar.marTime,ip=local_ip)
                        else:
                            pass
                    #Program Files
                    else:
                        self.autoupdate_path = self.Program_Files#确定软件安装路径赋值给全局
                        print(Mar.current_time,self.Program_Files)
                        if self.Database_write == True:
                            marsql.ssiinsert(host=localhostname,message=self.Program_Files,time=Mar.marTime,ip=local_ip)
                        else:
                            pass
                   
                except Exception as err:
                    print('系统安装错误，请手动安装')
                    ifosaccess_err = ('系统安装错误，请手动安装')
                    if self.Database_write == True:
                        marsql.ssiinsert(host=localhostname,error=ifosaccess_err+err,time=Mar.marTime)
                    else:
                        pass

                full_software_name_list = [
                    "集团总部CAC查询系统","板房系统安装向导","质量检测管理系统","生产总部通知系统","客户加单系统","固定资产管理系统","CAC销售管理系统安装",\
                        "董事长通知系统","后勤采购管理系统","CAC工厂管理系统安装","生产总部人员管理系统安装程序","车辆管理系统","集团CAC物料系统"]

                full_software_root_path = [
                    r'alterreport\AlertReport.exe',#集团总部CAC查询系统
                    r'dsg\DsgSystem.exe',#板房系统
                    r'QualityInspection\QualityInspection.exe',#质量检测管理系统
                    r'mnotice\Mnotice.exe',#生产总部通知系统 
                    r'CustAddOrder\CustAddOrder.exe',#CAC客户加单系统
                    r'FixedAssets\FixedAssets.exe',#固定资产管理系统
                    r'SaleReport\SaleReport.exe',#CAC销售管理系统
                    r'notice\notice.exe',#董事长通知系统
                    r'Logistics\Logistics.exe',#后勤采购管理系统
                    r'FactoryReport\FactoryReport.exe',#CAC工厂管理系统
                    r'HRS\HRS.exe',#人事系统
                    r'expendmanage\ExpendManage.exe',#车辆管理系统
                    r'Greige\Greige.exe'#集团CAC物料系统
                ]

                #执行公司通用系统安装

                sys_Nmae = []
                for sysname_index,name in enumerate(full_software_name_list):
                    setup = name + '.exe'
                    sys_Nmae.append(setup)
                    #获取CAC安装文件路径
                    software_root_path = sorted(Path(Yishion_sys_path).glob(f"**/*{name}.exe"))#搜索排序指定后续名的软件
                    Program_Files = os.path.join(self.Program_Files,full_software_root_path[sysname_index])#C:\Program Files
                    Program_Files_x86 = os.path.join(self.Program_Files_x86,full_software_root_path[sysname_index])#C:\Program Files (x86)
                    #执行安装
                    try:
                        if os.path.exists(Program_Files) or os.path.exists(Program_Files_x86):#检查要安装的系统是否已经存在
                            sys_install_values = (f"已经安装{name}，已经成功跳过")
                            print(Mar.current_time,sys_install_values,Mar.marTime)
                            if self.Database_write == True:
                                marsql.ssiinsert(host=localhostname,message=sys_install_values,time=Mar.marTime,ip=local_ip)       #写入mariadb 数据库    
                            else:
                                pass                  
                        else:
                            rmessage = os.popen(str(software_root_path[0]) +" /s")
                            time.sleep(0.1)                                       
                            sys_install_values1 = (f"!!正在安装{name}!!!")
                            print(Mar.current_time,sys_install_values1)
                            if self.Database_write == True:
                                marsql.ssiinsert(host=localhostname,message=str(rmessage.buffer) + str(rmessage.errors),time=Mar.marTime,ip=local_ip)    
                            else:
                                pass                             
                    except Exception as sys_install_err1:                  
                        sys_general_install_err = ("通用系统安装出错，请手动执行安装")
                        print(Mar.current_time,sys_general_install_err,sys_install_err1)
                        if self.Database_write == True:
                            marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=sys_general_install_err,ip=local_ip)
                        else:
                            pass
                #状态检测
                try: 
                    print(sys_Nmae)              
                    p = IP_name.pid(PidName=sys_Nmae)
                    print(p)
                except:
                    pass
                    # print('hello,python')
                
            else:
                print(Mar.current_time,'Yishion_sys_path文件夹异常,请确认网络正常')
                if_Yishion_sys_path_err = ('Yishion_sys_path文件夹异常,请确认网络正常')
                if self.Database_write == True:
                    marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=if_Yishion_sys_path_err,ip=local_ip)
                else:
                    pass
        except Exception as err:
            print(Mar.current_time,'请确认网络正常',err)

        #打开序列号文件
        try:
            os.popen(os.path.join(self.Work_directory_NetWork,"factory_Software","sn.txt"))
            keyfile_open_ok = ('序列号文件已成功打开')
            print(Mar.current_time,keyfile_open_ok)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=keyfile_open_ok)
            else:
                pass
        except IOError as key_file_e:
            key_file_err = ('SN文件错误或不存在')
            print(Mar.current_time,key_file_e)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=key_file_err)
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
                    updatavalues = (f"正在更新{updatafile}")
                    print(Mar.current_time,updatavalues)
                    if self.Database_write == True:                
                        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=updatavalues)
                    else:
                        pass
            except:
                sys_updata_Err_values1 = ('系统更新失败，请手动检查更新')
                print(Mar.current_time,sys_updata_Err_values1)
                if self.Database_write == True:
                    marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=sys_updata_Err_values1,ip=local_ip)
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
                    print(Mar.current_time,copy_banfang_updata_x32_ok_values1)
                    if self.Database_write == True:
                        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=copy_banfang_updata_x32_ok_values1,ip=local_ip)
                    else:
                        pass
                else:
                    copyfile(banfangupdate_file_CACUpdate_path,banfangpath_file_local)
                    copy_banfang_updata_x64_ok_values1 = ("板房更新文件，复制到64位文件夹成功")
                    print(Mar.current_time,copy_banfang_updata_x64_ok_values1)
                    os.popen(banfangpath_file_local)
                    if self.Database_write == True:
                        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=copy_banfang_updata_x64_ok_values1,ip=local_ip)
                    else:
                        pass
            except:           
                banfang_updata_Err1_values1 = ("板房更新文件复制失败，请手动复制更新")
                print(Mar.current_time,banfang_updata_Err1_values1)
                if self.Database_write == True:
                    marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=banfang_updata_Err1_values1,ip=local_ip)
                else:
                    pass
        except Exception as err1:
            update_err_values1 = ("更新文件路径查询错误")
            print(Mar.current_time,update_err_values1,err1)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=err1,ip=local_ip)
            else:
                pass


#执行常办公软件安装
    def sft_install(self):
        software_patn = os.path.join(self.Work_directory_NetWork, "factory_Software")#软件查询目录
        if os.access(software_patn,os.F_OK):
            try:            
                full_software_list = sorted(Path(software_patn).glob('**/*.exe'))
                for sft_index,name in enumerate(full_software_list):
                    if name.name == 'skylarinst-winc(192.168.0.36_80).exe':
                        print('已跳过%s'%name.name)
                        continue
                    os.popen(str(name))
                    Software_name = PurePath(name).name
                    Software_install_values = (f"正在安装{name}")
                    print(Mar.current_time,Software_install_values)
                    if self.Database_write == True:
                        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=Software_install_values,ip=local_ip)
                    else:
                        pass
            except:
                Software_install_err = ("软件安装错误，请手动安装")
                print(Mar.current_time,Software_install_err)
                if self.Database_write == True:
                    marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=Software_install_err,ip=local_ip)
                else:
                    pass
        else:
            software_patn_err = ('请确认网络文件夹factory_Software或共享正常')
            print(Mar.current_time,software_patn_err)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=software_patn_err,ip=local_ip)
            else:
                pass

#office安装 和 CAC注册表写入
    def Other_sft_install(self):
        try:    
            os.system(r"\\192.168.208.1\Python\Office_2007\MicrosoftOfficeProfessionalPlus2007\Setup.exe")
            office2007_startup_ok = ("Microsoftware Office 2007 已经成功启动！")
            print(Mar.current_time,office2007_startup_ok)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=office2007_startup_ok,ip=local_ip)
            else:
                pass
        except:
            office2007_install_Err = ("office 安装错误 请手动执行！")
            print(office2007_install_Err)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,error=office2007_startup_ok,time=Mar.marTime,ip=local_ip)
            else:
                pass
            
        try:
            os.system(r"\\192.168.208.1\Python\factory_Sys\所有CAC数据库注册表.reg")
            Cac_Reg_Open_ok = ('CAC默认注册表文件已经成功打开!!')
            print(Mar.current_time,Cac_Reg_Open_ok)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=Cac_Reg_Open_ok,ip=local_ip)
            else:
                pass
        except:
            Cac_Reg_Open_Err = ("CAC注册表未成功写入！，请手动执行")
            print(Mar.current_time,Cac_Reg_Open_Err)
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=Cac_Reg_Open_Err,ip=local_ip)
            else:
                pass
            
        #关闭key文件
        close_key_file = ('请关闭SN文件')
        print(Mar.current_time,close_key_file)
        if self.Database_write == True:
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=close_key_file,ip=local_ip)
        else:
            pass

        #程序执行完成
        Setup_flish = ("程序执行完成")
        print(Mar.current_time,Setup_flish)
        if self.Database_write == True:
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=Setup_flish,ip=local_ip)
        else:
            pass

        #360企业版安装
        try:
            se360 = '"\\192.168.208.1\Python\factory_Software\skylarinst-winc(192.168.0.36_80).exe"'
            os.startfile(se360)#单独启动se360
            se360tianqin = '360天擎已经启动'
            print(se360,'已经启动')
            if self.Database_write == True:
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=se360tianqin,ip=local_ip)
            else:
                pass
        except:
            pass

Mar = Install_all()#实例化 

if __name__=='__main__':
    network= r'\\192.168.208.1\Python'
    synetwork = r'\\192.168.0.17\CACUpdate'
    if os.access(network,os.F_OK) and os.access(synetwork,os.F_OK):
        Mar.localruntime()
        Mar.info()
        Mar.Locate32_software()
        Mar.areg()
        Mar.sys_install()
        Mar.sys_update()
        print('='*60)
        print('正在系统程序更新')
        time.sleep(30)
        # Mar.sft_install()
        # print('='*60)
        # print('正在等待安装软件')
        # Mar.Other_sft_install()
    else:  
        Network_values = ('请检查网络或共享设置(0.17 和 208.1)，请手动执行软件安装，或稍后再试') 
        print(Network_values)
        try:
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=Network_values,ip=local_ip)
        except:
            pass
        time.sleep(10)
        sys.exit()
        