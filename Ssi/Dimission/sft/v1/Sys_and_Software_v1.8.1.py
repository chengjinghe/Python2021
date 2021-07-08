from pathlib import Path
from shutil import copyfile
import os,time,winreg,sqlite3
from pathlib import PurePath
from shutil import copytree

h1 = os.popen('hostname')
h1 = h1.read()
localhostname = str(h1)
localhostname = localhostname.rstrip('\n')

sys_install_tables = ('eventid','hostname','clock','error','message')#数据表索引

def wsql(sql):
    try:
        conn = sqlite3.connect(r'\\192.168.208.1\Python\factory_Sys\install.db')
        cur = conn.execute(sql)
        search_result = cur.fetchall()
        conn.commit()
        conn.close()
        return search_result
    except:
        pass

#获取表当前索引号
def eventidindex():
    try:
        elist = []
        sql_install_tablts_list = wsql(sql='select * from sys_install_tables;')
        for tables_list in sql_install_tablts_list:
            tables_list_sn = sql_install_tablts_list.index(tables_list)
            elist.append(tables_list_sn)      
        return max(elist) + 1 #下一个索引号
    except:
        pass

def Runtime():
    t1 = time.localtime()
    Rtime = time.strftime("%Y-%m-%d %H-%M-%S:",t1)
    return Rtime  
   
def sql_insert(eventid=None,hostname= None,clock=None,error= None,message= None): 
    try:
        wsql(sql='''INSERT INTO sys_install_tables {0} VALUES ('{1}','{2}','{3}','{4}','{5}')'''.format(sys_install_tables,eventid,hostname,clock,error,message))
    except:
        return '数据写入错误'
        
try:
    Locate32_net_path = r"\\192.168.208.1\Python\Locate32"
    Locate32_local_path = r'C:\Program Files\Locate32'
    copytree(Locate32_net_path,Locate32_local_path)
    print('C:\Program Files\Locate32--放大镜搜索工具-已复制完成')
except Exception as Locate32_copy_err:
    print(Runtime(),Locate32_copy_err)
#修改本地时间显示样式
try:
    reg_time_path = r'Control Panel\International'
    time_reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg_time_path,0,winreg.KEY_WRITE)
    winreg.SetValueEx(time_reg,'sShortDate','',winreg.REG_SZ,'yyyy-M-d')
    winreg.FlushKey(time_reg)
    winreg.CloseKey(time_reg)
except OSError as winreg_error:
    reg_err_values = (Runtime(),winreg_error)
    # wsql(sql='''INSERT INTO sys_install_tables (clock,hostname,error) VALUES ('{0}','{1}','{2}')'''.format(reg_err_values[0],localhostname,reg_err_values[1]))
    sql_insert(clock=Runtime(),error=winreg_error,eventid=eventidindex(),hostname=localhostname)
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
except OSError as user_uac_err:
    print(Runtime(),user_uac_err,"用户帐户控制未修改")
    sql_insert(eventid=eventidindex(),clock=Runtime(),hostname=localhostname,error=user_uac_err)

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
    print(Runtime(),IERanges_err,"IE设置—未修改")
    sql_insert(eventid=eventidindex(),clock=Runtime(),hostname=localhostname,error=IERanges_err)
try:
    Starttime = Runtime()
    print('本次程序启动时间',Starttime)
    sql_insert(hostname=localhostname,clock=Runtime(),eventid=eventidindex())
except:
    pass

print('''
        ##### 如遇到错误 请尝试使用 管理员CMD 运行此脚本！！！####
        1,程序会自动跳过已经安装的系统，
        2,会自动打开SN文件,请手动关闭该文件
        ！请先输入192.168.0.17 用户名 ： Guest
        ！请先输入192.168.0.17 密码 ： Yscac2018
        ！请确保(0.17，208.1)网络共享能正常访问，否则程序将自动退出

                        更新版本时间 2021-4-13 HE
                        v1.8.1
        ''')

s = "正在安装通用系统_请稍后!!!"
b = "10秒后开始执行"

network= r'\\192.168.208.1\Python'
synetwork = r'\\192.168.0.17\CACUpdate'

#判断安装包存放路径是否正常
if os.access(network,os.F_OK) and os.access(synetwork,os.F_OK):
    print('{0:-^60}'.format(s))
    print('{0:>40}'.format(b))
    time.sleep(10)   
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
                    print(Runtime(),ifvalues)
                    sql_insert(clock=Runtime(),hostname=localhostname,message=ifvalues,eventid=eventidindex())
                else:
                    autoupdate_path = r"C:\Program Files"

                updatefile_name = 'autoupdate.exe'#系统更新更新文件名
            except:
                print('系统安装错误，请手动安装')
                ifosaccess_err = ('系统安装错误，请手动安装')
                sql_insert(clock=Runtime(),hostname=localhostname,error=ifosaccess_err)
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
                        print(Runtime(),sys_install_values)
                        sql_insert(clock=Runtime(),hostname=localhostname,message=sys_install_values,eventid=eventidindex())                             
                    else:
                        os.popen(str(sys_intstall_path[0])+" /s")
                        sys_install_values1 = ("!!正在安装{0}!!!".format(Yishion_sys_name[forsn]))
                        forsn +=1 
                        print(Runtime(),sys_install_values1)
                        sql_insert(clock=Runtime(),hostname=localhostname,message=sys_install_values1,eventid=eventidindex())                                 
                except Exception as sys_install_err1:                  
                    sys_general_install_err = ("通用系统安装出错，请手动执行安装")
                    print(Runtime(),sys_general_install_err,sys_install_err1)
                    sql_insert(clock=Runtime(),hostname=localhostname,error=sys_install_err1,eventid=eventidindex())
        else:
            print(Runtime(),'Yishion_sys_path文件夹异常,请确认网络正常')
            if_Yishion_sys_path_err = ('Yishion_sys_path文件夹异常,请确认网络正常')
            sql_insert(clock=Runtime(),error=if_Yishion_sys_path_err,hostname=localhostname)
    except:
        print(Runtime(),'请确认网络正常')

    waittime1 = ("正在等待更新程序启动，请稍后！")
    print(Runtime(),waittime1)
    sql_insert(clock=Runtime(),eventid=eventidindex(),hostname=localhostname)

    #打开序列号文件
    try:
        os.popen(r"\\192.168.208.1\Python\factory_Software\sn.txt")#打开SN文件
        keyfile_open_ok = ('序列号文件已成功打开')
        print(Runtime(),keyfile_open_ok)
        sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=keyfile_open_ok)
    except IOError as key_file_e:
        key_file_err = ('SN文件错误或不存在')
        print(Runtime(),key_file_err)
        sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=key_file_e)

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
                print(Runtime(),updatavalues)                
                sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=updatavalues)
        except:
            sys_updata_Err_values1 = ('系统更新失败，请手动检查更新')
            print(Runtime(),sys_updata_Err_values1)
            sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=sys_updata_Err_values1)
        #复制板房更新文件到本地
        try:
            if os.access(x86,os.F_OK):
                #复制板房更新文件到本地
                copyfile(banfangupdate_root,x86_banfang)
                #执行板房文件更新
                os.popen(x86_banfang)
                copy_banfang_updata_x32_ok_values1 = ("板房更新文件，复制到32位文件夹成功")
                print(Runtime(),copy_banfang_updata_x32_ok_values1)
                sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=copy_banfang_updata_x32_ok_values1)
            else:
                copyfile(banfangupdate_root,banfangpath_local)
                copy_banfang_updata_x64_ok_values1 = ("板房更新文件，复制到64位文件夹成功")
                print(Runtime(),copy_banfang_updata_x64_ok_values1)
                os.popen(banfangpath_local)
                sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=copy_banfang_updata_x64_ok_values1)
        except:           
            banfang_updata_Err1_values1 = ("板房更新文件复制失败，请手动复制更新")
            print(Runtime(),banfang_updata_Err1_values1)
            sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=banfang_updata_Err1_values1)
    except:
        update_err_values1 = ("更新文件路径查询错误")
        print(Runtime(),update_err_values1)
        sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=update_err_values1)

    wait_startup_software = ("正在启动软件安装，请稍后!")
    print(Runtime(),wait_startup_software)
    sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=wait_startup_software)

    print('='*60)#我是分割线
    time.sleep(30)
    #执行常办公软件安装
    software_patn = r"\\192.168.208.1\Python\factory_Software"#软件查询目录
    if os.access(software_patn,os.F_OK):
        try:
            
            software = sorted(Path(software_patn).glob('**/*.exe'))
            for z in software:
                os.popen(str(z))
                Software_name = PurePath(z).name
                Software_install_values = ("正在安装{0}".format(Software_name))
                print(Runtime(),Software_install_values)
                sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=Software_install_values)
        except:
            Software_install_err = ("软件安装错误，请手动安装")
            print(Runtime(),Software_install_err)
            sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=Software_install_err)
    else:
        software_patn_err = ('请确认网络文件夹factory_Software或共享正常')
        print(Runtime(),software_patn_err)
        sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=software_patn_err)

    #office安装 和 CAC注册表写入
    try:    
        os.system(r"\\192.168.208.1\Python\Office_2007\MicrosoftOfficeProfessionalPlus2007\Setup.exe")
        office2007_startup_ok = ("Microsoftware Office 2007 已经成功启动！")
        print(Runtime(),office2007_startup_ok)
        sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=office2007_startup_ok)
    except:
        office2007_install_Err = ("office 安装错误 请手动执行！")
        print(office2007_install_Err)
        sql_insert(Runtime(),eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=office2007_install_Err)

    try:
        os.system(r"\\192.168.208.1\Python\factory_Sys\所有CAC数据库注册表.reg")
        Cac_Reg_Open_ok = ('CAC默认注册表文件已经成功打开!!')
        print(Runtime(),Cac_Reg_Open_ok)
        sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=Cac_Reg_Open_ok)
    except:
        Cac_Reg_Open_Err = ("CAC注册表未成功写入！，请手动执行")
        print(Runtime(),Cac_Reg_Open_Err)
        sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),error=Cac_Reg_Open_Err)
        
    #关闭key文件
    close_key_file = ('请关闭SN文件')
    print(Runtime(),close_key_file)
    sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=close_key_file)

    #程度执行完成
    Setup_flish = ("程序执行完成")
    print(Runtime(),Setup_flish)
    sql_insert(eventid=eventidindex(),hostname=localhostname,clock=Runtime(),message=Setup_flish)

else:  
    Network_values = ('请检查网络或共享设置，请手动执行软件安装，或稍后再试') 
    print(Network_values)
    # wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(Network_values[0],Network_values[1],localhostname))
    sql_insert(clock=Runtime(),hostname=localhostname,error=Network_values)
    time.sleep(10)
    