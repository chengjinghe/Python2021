from pathlib import Path
from shutil import copyfile
from shutil import copytree
import os,winreg,time,sys
from yishionreg import Reg
print('''
            提示！
    如有报错，请右键以管理员的方式运行！
    CMD报错，需要将本程序复制到本地再运行

''')

#获取桌面路径
def get_desktop():
    
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)

    return winreg.QueryValueEx(key, "Desktop")[0]

def areg():
    try:
        reg_time_path = r'Control Panel\International'
        time_reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg_time_path,0,winreg.KEY_WRITE)
        winreg.SetValueEx(time_reg,'sShortDate','',winreg.REG_SZ,'yyyy-M-d')
        winreg.FlushKey(time_reg)
        winreg.CloseKey(time_reg)
        timeFormat = '时间格式已经修改为---'
        # marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=timeFormat)
        print(timeFormat)
    except OSError as winreg_error:
        # reg_err_values = (l_data_time.current_time,winreg_error)
        # marsql.ssiinsert(host=localhostname,error=winreg_error,time=Mar.marTime)#写入mariadb 数据库
        # print(reg_err_values)
        # print("系统时间样式未修改")
        pass

#修改windows10用户帐户控制
    try:
        reg_user_UAC= r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
        user_uac = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,reg_user_UAC,0,winreg.KEY_WRITE)
        winreg.SetValueEx(user_uac,'ConsentPromptBehaviorAdmin','',winreg.REG_DWORD,0)
        winreg.SetValueEx(user_uac,'PromptOnSecureDesktop','',winreg.REG_DWORD,0)
        winreg.FlushKey(user_uac)
        winreg.CloseKey(user_uac)
        win_uac = 'windows10用户帐户控制-已改为最低'
        # marsql.ssiinsert(host=localhostname,time=Mar.marTime,message=win_uac)
        print(win_uac)
    except OSError as user_uac_err:
        # print(l_data_time.current_time,user_uac_err,"用户帐户控制未修改")
        # marsql.ssiinsert(host=localhostname,error=user_uac_err,time=Mar.marTime)
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
        # print(l_data_time.current_time,IERanges_err,"IE设置—未修改")
        # marsql.ssiinsert(host=localhostname,time=Mar.marTime,error=IERanges_err)
        pass

    try:
        timeserver = r'SOFTWARE\Microsoft\Windows\CurrentVersion\DateTime\Servers'
        timeserver_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,timeserver,0,winreg.KEY_WRITE)
        winreg.SetValueEx(timeserver_key,'1','',winreg.REG_SZ,'192.168.0.201')
        winreg.SetValueEx(timeserver_key,'2','',winreg.REG_SZ,'192.168.0.200')
        winreg.FlushKey(timeserver_key)
        winreg.CloseKey(timeserver_key)
    except:
        pass
def fact_erp():
    try:
        Root_Path = r'\\192.168.208.1\Python\FactoryERP'
        local_Path = r'C:\FactoryERP'
        local_ShutDown_file = r'c:\shutdown.bat'
        local_ShutDown_Profile = r'c:\shutdown1.xml'
        Root_Shutdown_file = r"\\192.168.208.1\Python\shutdown.bat"
        Root_ShutDown_Profile = r"\\192.168.208.1\Python\shutdown1.xml"
        g = get_desktop()
        FactoryERP_lnk = (g + r'\FactoryERP.lnk')
        if os.access(local_Path,os.F_OK):
            print('FactoryERP目录已经存在','*'*10)
        else:
            try:
                copytree(Root_Path,local_Path)
                print('FactoryERP目录已经制','*'*10)
            except Exception as e:
                print('FactoryERP目录复制失败 ','*'*10,e)

        for file in (FactoryERP_lnk,local_ShutDown_file,local_ShutDown_Profile):
            if os.path.exists(file):
                print('%s文件夹已经在存在！'%file,'*'*10)
            else:
                if file == FactoryERP_lnk:
                    try:
                        os.symlink("c:\FactoryERP\StartERP2.exe",FactoryERP_lnk)
                        print('FactoryERP快捷方式已创建完成','*'*10)
                    except Exception as e1 :
                        print('FactoryERP快捷方式无法创建',e1,'*'*10)
                elif file == local_ShutDown_file:
                    try:                   
                        copyfile(Root_Shutdown_file,local_ShutDown_file)
                        print('关机脚本已完成复制','*'*10)
                    except Exception as e2:
                        print('关机脚本复制失败',e2,'*'*10)
                else:
                    try:
                        copyfile(Root_ShutDown_Profile,local_ShutDown_Profile)
                        print("关机计划任务配置文件已完成复制",'*'*10)
                    except Exception as e3:
                        print("关机计划任务配置文件复制失败",e3,'*'*10)
        os.popen('taskschd.msc')
        os.popen(r"c:\FactoryERP\StartERP2.exe")
    except Exception as e:
        print(e)
r = Reg()
r.timezaone
r.sec
areg()
print('正在复制文件...','*'*10)
fact_erp()
print('设置已完成...','*'*10)
time.sleep(5)
sys.exit()