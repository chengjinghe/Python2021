import winreg
class Reg(object):
    '''
    timezaone
    sec
    '''
    @property
    def timezaone(self):
        '''
        windows 10 Change local time zone to China (Beijing, Shanghai, Tianjin, Chongqing)
        
        '''
        root_local = r'SYSTEM\CurrentControlSet\Control\TimeZoneInformation' # root path
        data = {
        "Bias":int('fffffe20',16),
        "DaylightBias":int('ffffffc4',16),
        "ActiveTimeBias":int('fffffe20',16),
        }
        data1 = {
            "DaylightName":"@tzres.dll,-571",
            "StandardName":"@tzres.dll,-572",
            "TimeZoneKeyName":"China Standard Time",
        }       
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,root_local,0,winreg.KEY_WRITE)
            for keys,value in data.items():
                winreg.SetValueEx(key,keys,'',winreg.REG_DWORD,value)
            
            for keys1,value1 in data1.items():
                winreg.SetValueEx(key,keys1,'',winreg.REG_SZ,value1)
                  
        except Exception as err:
            print(err)
        finally:
            winreg.FlushKey(key)
            winreg.CloseKey(key)
        return 'Done'

    #The task file hides the search for Cortana
    @property
    def sec(self):
        '''
        The task file hides the search for Cortana
        '''       
        Secrah_root_local = r'Software\Microsoft\Windows\CurrentVersion\Search' #secrah
        try:
            sec_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,Secrah_root_local,0,winreg.KEY_WRITE)
            winreg.SetValueEx(sec_key,'SearchboxTaskbarMode','',winreg.REG_DWORD,0)#0 is so 1 is displayed
        except Exception as err:
            print(err)
        finally:          
            winreg.FlushKey(sec_key)
            winreg.CloseKey(sec_key)
        return 'Done'
    
    @property
    def get_desktop(self):
        '''
        #返回电脑的桌面路径
        '''
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)

        return winreg.QueryValueEx(key, "Desktop")[0]
if __name__=="__main__":
    r = Reg()
    print(r.timezaone)
