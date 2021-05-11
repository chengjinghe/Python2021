import winreg
'''
修改时候服务器为 192.168.0.201
UAC修改为最低
IE增加信任192.168.208.1/python

'''
class Reg():
    #时间样式
    def timestyle(self):
            time_path_reg_root = r'Control Panel\International'
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,time_path_reg_root,0,winreg.KEY_WRITE) as time_reg:
                    winreg.SetValueEx(time_reg,'sShortDate','',winreg.REG_SZ,'yyyy-M-d')
                    winreg.FlushKey(time_reg)
                    print('timestyle_ok')
            except (OSError,NameError)as err:
                print(err)
    #设置时间服务器
    def ntp_server(self):       
            time_server_reg_root = r'SOFTWARE\Microsoft\Windows\CurrentVersion\DateTime\Servers' # DateTime_server
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,time_server_reg_root,0,winreg.KEY_WRITE) as ntp_server:
                    winreg.SetValueEx(ntp_server,'1','',winreg.REG_SZ,'192.168.0.201')
                    winreg.FlushKey(ntp_server)
                    print('time_server_ok')
            except (OSError,NameError)as err:
                print(err)
    #UAC修改为最低
    def user_uac(self):
            user_UAC_reg_root= r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
            try: 
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,user_UAC_reg_root,0,winreg.KEY_WRITE) as user_uac:
                    winreg.SetValueEx(user_uac,'ConsentPromptBehaviorAdmin','',winreg.REG_DWORD,0)
                    winreg.SetValueEx(user_uac,'PromptOnSecureDesktop','',winreg.REG_DWORD,0)
                    winreg.FlushKey(user_uac)
                    print('uac_ok')
            except (OSError,NameError)as err:
                print(err)
    #修改IE信任208.1
    def ie_seting(self):
            IERanges_reg = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,IERanges_reg,0,winreg.KEY_WRITE) as ie_key:
                    ie = winreg.CreateKeyEx(ie_key,'Range1')#创建项
                    winreg.SetValueEx(ie,':Range','',winreg.REG_SZ,'192.168.208.1')
                    winreg.SetValueEx(ie,'file','',winreg.REG_DWORD,1)
                    winreg.FlushKey(ie)
                    print('ie_seting_ok')
            except (OSError,NameError)as err:
                print(err)
if __name__=='__main__':
    r =Reg()
    r.timestyle()
    r.ntp_server()
    r.user_uac()
    r.ie_seting()