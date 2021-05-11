from pathlib import Path
from shutil import copyfile
import os,time,winreg,socket,sys
from pathlib import PurePath
from shutil import copytree
from marsql import MarDB
marsql = MarDB()
'''
v2.8.1 优化代码实现流程
 1 加入CAC物料系统，车辆管理系统安装
'''
localhostname = socket.gethostname()# 获取本地计算机名

class Install_all():
    network= r'\\192.168.208.1\Python'
    synetwork = r'\\192.168.0.17\CACUpdate'
    @property
    def current_time(self):
        localtime = time.localtime()
        Rtime = time.strftime("%Y-%m-%d %H-%M-%S:", localtime)
        return Rtime

    @property
    def marTime(self):
        localtime = time.localtime()
        rRtime = time.strftime("%Y%m%d%H%M%S", localtime)
        return rRtime

    #获取表当前索引号
    @property
    def eventidindex(self):
        try:
            elist = []
            sql_install_tablts_list = wsql(sql='select * from sys_install_tables;')
            for tables_list in sql_install_tablts_list:
                tables_list_sn = sql_install_tablts_list.index(tables_list)
                elist.append(tables_list_sn)      
            return max(elist) + 1 #返回下一个索引号
        except:
            pass

l_data_time = Install_all()#实例化本地时间
Mar = Install_all()#实例化本地时间

# 搜索工具软件(放大镜)
def Locate32_software():       
    try:
        Locate32_net_path = r"\\192.168.208.1\Python\Locate32"
        Locate32_local_path = r'C:\Program Files\Locate32'
        if os.access(Locate32_local_path,os.F_OK):
            print('locate32已存在')
        else:
            copytree(Locate32_net_path,Locate32_local_path)
            print('C:\Program Files\Locate32--放大镜搜索工具-已复制完成')
            os.system('mklink %userprofile%\desktop\locate32 "C:\Program Files\Locate32\locate32.exe"')
            os.popen("C:\Program Files\Locate32\locate32.exe")
    except Exception as Locate32_copy_err:
        print(l_data_time.current_time,Locate32_copy_err)

#修改本地时间显示样式
def areg():
    try:
        reg_time_path = r'Control Panel\International'
        time_reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg_time_path,0,winreg.KEY_WRITE)
        winreg.SetValueEx(time_reg,'sShortDate','',winreg.REG_SZ,'yyyy-M-d')
        winreg.FlushKey(time_reg)
        winreg.CloseKey(time_reg)
        timeFormat = '时间格式已经修改为---'
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=timeFormat)
        print(timeFormat)
    except OSError as winreg_error:
        reg_err_values = (l_data_time.current_time,winreg_error)
        marsql.ssiinsert(host=localhostname,error=winreg_error,time=Mar.marTime)#写入mariadb 数据库
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
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=win_uac)
        print(win_uac)
    except OSError as user_uac_err:
        print(l_data_time.current_time,user_uac_err,"用户帐户控制未修改")
        marsql.ssiinsert(host=localhostname,error=user_uac_err,time=Mar.marTime)

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
        print(l_data_time.current_time,IERanges_err,"IE设置—未修改")
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=IERanges_err)

#实例化本地时间
def localruntime():
    try:
        Starttime = l_data_time.current_time
        print('本次程序启动时间',Starttime)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime)
    except:
        pass

#提示信息
def info():
    print('''
            1,程序会自动跳过已经安装的系统，
            2,会自动打开SN文件,请手动关闭该文件
            ！请先输入192.168.0.17 用户名 ： Guest
            ！请先输入192.168.0.17 密码 ： Yscac2018
            ！请确保(0.17，208.1)网络共享能正常访问，否则程序将自动退出

                            更新版本时间 2021-5-20 HE
                            v2.8.2
            ''')

    s = "正在安装通用系统_请稍后!!!"
    b = "10秒后开始执行"
    print('{0:-^60}'.format(s))
    print('{0:>40}'.format(b))
    time.sleep(10)

# 通用系统安装和更新
def sys_install():    
    Yishion_sys_path = r'\\192.168.208.1\Python\factory_Sys'
    try:
        if os.access(Yishion_sys_path,os.F_OK):
            #判断X86文件在存在
            x86 = r"C:\Program Files (x86)" #x86文件路径
            NoX86 = r"C:\Program Files"#非X86文件路径
            try:
                if os.access(x86,os.F_OK):
                    autoupdate_path = r"C:\Program Files (x86)"
                    ifvalues = ("发现Program Files (x86)")
                    print(l_data_time.current_time,ifvalues)
                    marsql.ssiinsert(host=localhostname,message=ifvalues,time=Mar.marTime)
                else:
                    autoupdate_path = r"C:\Program Files"

                updatefile_name = 'autoupdate.exe'#系统更新更新文件名
            except:
                print('系统安装错误，请手动安装')
                ifosaccess_err = ('系统安装错误，请手动安装')
                marsql.ssiinsert(host=localhostname,error=ifosaccess_err,time=Mar.marTime)
            banfangpath_local = r"C:\Program Files\dsg\autoupdateNew.exe"#板房系统更新文件非X86文件夹
            banfangupdate_root =  r"\\192.168.0.17\CACUpdate\板房系统\板房系统安装目录\autoupdateNew.exe"
            x86_banfang = r"C:\Program Files (x86)\dsg\autoupdateNew.exe"#板房系统更新文件非文件夹
            Yishion_sys_name = [
                "集团总部CAC查询系统",
                "板房系统安装向导",
                "质量检测管理系统",
                "生产总部通知系统",
                "客户加单系统",
                "固定资产管理系统",
                "CAC销售管理系统安装",
                "董事长通知系统",
                "后勤采购管理系统",
                "CAC工厂管理系统安装",
                "生产总部人员管理系统安装程序",
                "车辆管理系统",
                "集团CAC物料系统"
            ]

            Startup_level_file = [
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
            forsn = 0
            for r in Yishion_sys_name:
                #获取CAC安装文件路径
                sys_intstall_path = sorted(Path(Yishion_sys_path).glob("**/*{0}.exe".format(Yishion_sys_name[forsn])))
                setup_local_No86 = os.path.join(NoX86,Startup_level_file[forsn])#本地非X86路径
                setup_local_X86 = os.path.join(x86,Startup_level_file[forsn])#本地非X86路径
                #执行安装
                try:
                    if os.path.exists(setup_local_No86) or os.path.exists(setup_local_X86):#检查要安装的系统是否已经存在
                        sys_install_values = ("已经安装{0}，已经成功跳过".format(Yishion_sys_name[forsn]))
                        forsn +=1
                        print(l_data_time.current_time,sys_install_values,Mar.marTime)
                        marsql.ssiinsert(host=localhostname,message=sys_install_values,time=Mar.marTime)       #写入mariadb 数据库                      
                    else:
                        os.popen(str(sys_intstall_path[0])+" /s")
                        sys_install_values1 = ("!!正在安装{0}!!!".format(Yishion_sys_name[forsn]))
                        forsn +=1 
                        print(l_data_time.current_time,sys_install_values1,Mar.marTime)
                        marsql.ssiinsert(host=localhostname,message=sys_install_values1,time=Mar.marTime)                                 
                except Exception as sys_install_err1:                  
                    sys_general_install_err = ("通用系统安装出错，请手动执行安装")
                    print(l_data_time.current_time,sys_general_install_err,sys_install_err1)
                    marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=sys_general_install_err)
        else:
            print(l_data_time.current_time,'Yishion_sys_path文件夹异常,请确认网络正常')
            if_Yishion_sys_path_err = ('Yishion_sys_path文件夹异常,请确认网络正常')
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=if_Yishion_sys_path_err)
    except:
        print(l_data_time.current_time,'请确认网络正常')

    waittime1 = ("正在等待更新程序启动，请稍后！")
    print(l_data_time.current_time,waittime1)
    marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=waittime1)

    #打开序列号文件
    try:
        os.popen(r"\\192.168.208.1\Python\factory_Software\sn.txt")#打开SN文件
        keyfile_open_ok = ('序列号文件已成功打开')
        print(l_data_time.current_time,keyfile_open_ok)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=keyfile_open_ok)
    except IOError as key_file_e:
        key_file_err = ('SN文件错误或不存在')
        print(l_data_time.current_time,key_file_err)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=key_file_err)

    print('='*60)#我是分割线
    time.sleep(30)

    try:
        updatelen = sorted(Path(autoupdate_path).glob("**/autoupdate.exe"))#搜索更新文件所在路径
        #执行其他系统更新
        forsn1 = 0
        try:
            for x in updatelen:
                os.popen(str(x))
                updatavalues = ("正在更新{0}".format(Yishion_sys_name[forsn1]))
                forsn1 +=1
                print(l_data_time.current_time,updatavalues)                
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=updatavalues)
        except:
            sys_updata_Err_values1 = ('系统更新失败，请手动检查更新')
            print(l_data_time.current_time,sys_updata_Err_values1)
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=sys_updata_Err_values1)
        #复制板房更新文件到本地
        try:
            if os.access(x86,os.F_OK):
                #复制板房更新文件到本地
                copyfile(banfangupdate_root,x86_banfang)
                #执行板房文件更新
                os.popen(x86_banfang)
                copy_banfang_updata_x32_ok_values1 = ("板房更新文件，复制到32位文件夹成功")
                print(l_data_time.current_time,copy_banfang_updata_x32_ok_values1)
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=copy_banfang_updata_x32_ok_values1)
            else:
                copyfile(banfangupdate_root,banfangpath_local)
                copy_banfang_updata_x64_ok_values1 = ("板房更新文件，复制到64位文件夹成功")
                print(l_data_time.current_time,copy_banfang_updata_x64_ok_values1)
                os.popen(banfangpath_local)
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=copy_banfang_updata_x64_ok_values1)
        except:           
            banfang_updata_Err1_values1 = ("板房更新文件复制失败，请手动复制更新")
            print(l_data_time.current_time,banfang_updata_Err1_values1)
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=banfang_updata_Err1_values1)
    except:
        update_err_values1 = ("更新文件路径查询错误")
        print(l_data_time.current_time,update_err_values1)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=update_err_values1)

    wait_startup_software = ("正在启动软件安装，请稍后!")
    print(l_data_time.current_time,wait_startup_software)
    marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=wait_startup_software)

#执行常办公软件安装
def sft_install():
    software_patn = r"\\192.168.208.1\Python\factory_Software"#软件查询目录
    if os.access(software_patn,os.F_OK):
        try:            
            software = sorted(Path(software_patn).glob('**/*.exe'))
            for z in software:
                if z.name == 'skylarinst-winc(192.168.0.36_80).exe':
                    print('已跳过%s'%z.name)
                    continue
                os.popen(str(z))
                Software_name = PurePath(z).name
                Software_install_values = ("正在安装{0}".format(Software_name))
                print(l_data_time.current_time,Software_install_values)
                marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=Software_install_values)
        except:
            Software_install_err = ("软件安装错误，请手动安装")
            print(l_data_time.current_time,Software_install_err)
            marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=Software_install_err)
    else:
        software_patn_err = ('请确认网络文件夹factory_Software或共享正常')
        print(l_data_time.current_time,software_patn_err)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=software_patn_err)

#office安装 和 CAC注册表写入
def Other_sft_install():
    try:    
        os.system(r"\\192.168.208.1\Python\Office_2007\MicrosoftOfficeProfessionalPlus2007\Setup.exe")
        office2007_startup_ok = ("Microsoftware Office 2007 已经成功启动！")
        print(l_data_time.current_time,office2007_startup_ok)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=office2007_startup_ok)
    except:
        office2007_install_Err = ("office 安装错误 请手动执行！")
        print(office2007_install_Err)
        marsql.ssiinsert(host=localhostname,error=office2007_startup_ok,time=Mar.marTime)

    try:
        os.system(r"\\192.168.208.1\Python\factory_Sys\所有CAC数据库注册表.reg")
        Cac_Reg_Open_ok = ('CAC默认注册表文件已经成功打开!!')
        print(l_data_time.current_time,Cac_Reg_Open_ok)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=Cac_Reg_Open_ok)
    except:
        Cac_Reg_Open_Err = ("CAC注册表未成功写入！，请手动执行")
        print(l_data_time.current_time,Cac_Reg_Open_Err)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=Cac_Reg_Open_Err)
        
    #关闭key文件
    close_key_file = ('请关闭SN文件')
    print(l_data_time.current_time,close_key_file)
    marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=close_key_file)

    #程序执行完成
    Setup_flish = ("程序执行完成")
    print(l_data_time.current_time,Setup_flish)
    marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=Setup_flish)

    #360企业版安装
    try:
        se360 = '"\\192.168.208.1\Python\factory_Software\skylarinst-winc(192.168.0.36_80).exe"'
        os.startfile(se360)#单独启动se360
        se360tianqin = '360天擎已经启动'
        print(se360,'已经启动')
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=se360tianqin)
    except:
        pass
#判断安装包存放路径是否正常
if __name__=='__main__':
    network= r'\\192.168.208.1\Python'
    synetwork = r'\\192.168.0.17\CACUpdate'
    if os.access(network,os.F_OK) and os.access(synetwork,os.F_OK):
        localruntime()
        info()
        Locate32_software()
        areg()
        sys_install()
        print('='*60)
        print('正在系统程序更新')
        time.sleep(30)
        sft_install()
        print('='*60)
        print('正在等待安装软件')
        Other_sft_install()
    else:  
        Network_values = ('请检查网络或共享设置，请手动执行软件安装，或稍后再试') 
        print(Network_values)
        marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=Network_values)
        time.sleep(10)
        sys.exit()
        