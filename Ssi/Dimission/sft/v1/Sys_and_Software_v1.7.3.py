from pathlib import Path
from shutil import copyfile
import os,time,winreg,sqlite3

h1 = os.popen('hostname')
h1 = h1.read()
localhostname = str(h1)
localhostname = localhostname.rstrip('\n')

def wsql(sql):
    conn = sqlite3.connect(r'\\192.168.208.1\Python\factory_Sys\install.db')
    t1 = conn.execute(sql)
    t = t1.fetchall()
    conn.commit()
    conn.close()
    return t

def Runtime():
    t1 = time.localtime()
    Rtime = time.strftime("%Y-%m-%d %H-%M-%S:",t1)
    return Rtime

#修改本地时间显示样式
try:
    reg_time_path = r'Control Panel\International'
    time_reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg_time_path,0,winreg.KEY_WRITE)
    winreg.SetValueEx(time_reg,'sShortDate','',winreg.REG_SZ,'yyyy-M-d')
    winreg.FlushKey(time_reg)
    winreg.CloseKey(time_reg)
except OSError as winreg_error:
    reg_err_values = (Runtime(),winreg_error)
    wsql(sql='''INSERT INTO sys_install_tables (clock,hostname,error) VALUES ('{0}','{1}','{2}')'''.format(reg_err_values[0],localhostname,reg_err_values[1]))
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
except OSError as e1:
    print(e1)
    print("用户帐户控制,未修改")

#修IE设置——
try:
    IERanges = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
    ie_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,IERanges,0,winreg.KEY_WRITE)
    ie_key = winreg.CreateKeyEx(ie_key,'Range1')#创建项
    winreg.SetValueEx(ie_key,':Range','',winreg.REG_SZ,'192.168.208.1')
    winreg.SetValueEx(ie_key,'file','',winreg.REG_DWORD,1)
    winreg.FlushKey(ie_key)
    winreg.CloseKey(ie_key)
except OSError as e2:
    print(e2)
    print("IE设置—未修改")

Starttime = Runtime()
print('本次程序启动时间',Starttime)
wsql(sql='''INSERT INTO sys_install_tables (clock,hostname) VALUES ('本次程序启动时间{0}','{1}')'''.format(Starttime,localhostname))

print('''
        1,程序会自动跳过已经安装的系统，
        2,会自动打开SN文件,请手动关闭该文件
        ！请先输入192.168.0.17 用户名 ： Guest
        ！请先输入192.168.0.17 密码 ： Yscac2018
        ！请确保(0.17，208.1)网络共享能正常访问，否则程序将自动退出

                        更新版本时间 2021-2-23 HE
                        v1.7.3
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
                    ifvalues = (Runtime(),"发现Program Files (x86)")
                    print(ifvalues)
                    wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostnmae) VALUES ('{0}','{1}','{2}')'''.format(ifvalues[0],ifvalues[1],localhostname))
                else:
                    autoupdate_path = r"C:\Program Files"

                updatefile_name = 'autoupdate.exe'#系统更新更新文件名
            except:
                print(Runtime(),'系统安装错误，请手动安装')
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
                "生产总部人员管理系统安装程序"
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
                r'HRS\HRS.exe'#人事系统          
            ]

            #执行公司通用系统安装
            forsn = 0
            for r in Yishion_sys_name:
                #获取CAC安装文件路径
                sys_intstall_path = sorted(Path(Yishion_sys_path).glob("**/*{0}.exe".format(Yishion_sys_name[forsn])))
                setup_local_No86 = os.path.join(NoX86,Startup_level_file[forsn])
                setup_local_X86 = os.path.join(x86,Startup_level_file[forsn])
                #执行安装
                try:
                    if os.path.exists(setup_local_No86) or os.path.exists(setup_local_X86):
                        sys_install_values = (Runtime(),"已经安装{0}，已经成功跳过".format(Yishion_sys_name[forsn]))
                        forsn +=1
                        print(sys_install_values)
                        wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(sys_install_values[0],\
                            sys_install_values[1],localhostname))
                                                      
                    else:
                        os.popen(str(sys_intstall_path[0])+" /s")
                        sys_install_values1 = (Runtime(),"!!正在安装{0}!!!".format(Yishion_sys_name[forsn]))
                        forsn +=1 
                        print(sys_install_values1)
                        wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(sys_install_values1[0],\
                            sys_install_values1[1],localhostname))                                       
                except:
                    print(Runtime(),"通用系统安装出错，请手动执行安装")
                    
        else:
            print(Runtime(),'请确认网络正常')
    except:
        print(Runtime(),'请确认网络正常')

    waittime1 = (Runtime(),"正在等待更新程序启动，请稍后！")
    print(waittime1)
    wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(waittime1[0],waittime1[1],localhostname))

    #打开序列号文件
    try:
        os.popen(r"\\192.168.208.1\Python\factory_Software\sn.txt")#打开SN文件
        keyfile_open_ok = (Runtime(),'序列号文件已成功打开')
        print(keyfile_open_ok)
        wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(keyfile_open_ok[0],keyfile_open_ok[1],localhostname))
    except:
        print(Runtime(),'SN文件错误或不存在')

    time.sleep(30)
    try:
        updatelen = sorted(Path(autoupdate_path).glob("**/autoupdate.exe"))#搜索更新文件所在路径
        #执行其他系统更新
        forsn1 = 0
        try:
            for x in updatelen:
                os.popen(str(x))
                updatavalues = (Runtime(),"正在更新{0}".format(Yishion_sys_name[forsn1]))
                forsn1 +=1
                print(updatavalues)                
                wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(updatavalues[0],updatavalues[1],localhostname))  
        except:
            sys_updata_Err_values1 = (Runtime(),'系统更新失败，请手动检查更新')
            print(sys_updata_Err_values1)
            wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(sys_updata_Err_values1[0],\
                sys_updata_Err_values1[1],localhostname))  

        #复制板房更新文件到本地
        try:
            if os.access(x86,os.F_OK):
                #复制板房更新文件到本地
                copyfile(banfangupdate_root,x86_banfang)
                #执行板房文件更新
                os.popen(x86_banfang)
                copy_banfang_updata_x32_ok_values1 = (Runtime(),"复制到32位文件夹成功")
                print(copy_banfang_updata_x32_ok_values1)
                wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(copy_banfang_updata_x32_ok_values1[0],\
                    copy_banfang_updata_x32_ok_values1[1],localhostname))
            else:
                copyfile(banfangupdate_root,banfangpath_local)
                copy_banfang_updata_x64_ok_values1 = (Runtime(),"复制到64位文件夹成功")
                wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(copy_banfang_updata_x64_ok_values1[0],\
                    copy_banfang_updata_x64_ok_values1[1],localhostname))
        except:           
            banfang_updata_Err1_values1 = (Runtime(),"板房更新文件复制失败，请手动复制更新")
            print(banfang_updata_Err1_values1)
            wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(banfang_updata_Err1_values1[0],\
                banfang_updata_Err1_values1[1],localhostname))  
    except:
        print(Runtime(),"更新文件路径查询错误")
   
    wait_startup_software = (Runtime(),"正在启动软件安装，请稍后!")
    print(wait_startup_software)
    wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(wait_startup_software[0],wait_startup_software[1],localhostname))
    
    time.sleep(30)
    #执行常办公软件安装
    software_patn = r"\\192.168.208.1\Python\factory_Software"#软件查询目录
    if os.access(software_patn,os.F_OK):
        try:
            software = sorted(Path(software_patn).glob('**/*.exe'))
            for z in software:
                os.popen(str(z))
                Software_install_values = (Runtime(),"正在安装{0}".format(z))
                print(Software_install_values)
                wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(Software_install_values[0],\
                    Software_install_values[1],localhostname))
        except:
            print(Runtime(),"软件安装错误，请手动安装")
    else:
        print(Runtime(),'请确认网络或共享正常')

    #office安装 和 CAC注册表写入
    try:    
        os.system(r"\\192.168.208.1\1.电脑部\03.【办公软件】\2007\MicrosoftOfficeProfessionalPlus2007\setup.exe")
        office2007_startup_ok = (Runtime(),"Microsoftware Office 2007 已经成功启动！")
        wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(office2007_startup_ok[0],office2007_startup_ok[1],localhostname))
        os.system(r"\\192.168.208.1\Python\factory_Sys\所有CAC数据库注册表.reg")
        Cac_Reg_Open_ok = (Runtime(),'CAC默认注册表文件已经成功打开!!')
        print(Cac_Reg_Open_ok)
        wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(Cac_Reg_Open_ok[0],Cac_Reg_Open_ok[1],localhostname))
    except:
        office2007_install_Err = (Runtime(),"office 安装错误 请手动执行！")
        print(office2007_install_Err)
        wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(office2007_install_Err[0],office2007_install_Err[1],localhostname))

        Cac_Reg_Open_Err = (Runtime(),"CAC注册表未成功写入！，请手动执行")
        print(Cac_Reg_Open_Err)
        wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(Cac_Reg_Open_Err[0],Cac_Reg_Open_Err[1],localhostname))
        
    #关闭key文件
    close_key_file = (Runtime(),'请关闭SN文件')
    print(close_key_file)
    wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(close_key_file[0],close_key_file[1],localhostname))

    #程度执行完成
    Setup_flish = (Runtime(),"程序执行完成")
    print(Setup_flish)
    wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(Setup_flish[0],Setup_flish[1],localhostname))
else:  
    Network_values = (Runtime(),'请检查网络或共享设置，请手动执行软件安装，或稍后再试') 
    print(Network_values)
    wsql(sql='''INSERT INTO sys_install_tables (clock,message,hostname) VALUES ('{0}','{1}','{2}')'''.format(Network_values[0],Network_values[1],localhostname))
    time.sleep(10)