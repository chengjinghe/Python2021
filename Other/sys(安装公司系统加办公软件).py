from pathlib import Path
from shutil import copyfile
import os,time
software_patn = r"\\192.168.208.1\Python\factory_Software"
time.sleep(10)
s = "正在安装通用系统_请稍后!!!"
b = "10秒后开始执行"
user = "请先输入192.168.0.17 用户名 ： Guest"
passworld = "请先输入192.168.0.17 密码 ： Yscac2018"

print('{0:-^60}'.format(s))
print('{0:>40}'.format(b))
print('{0:>30}'.format(user))
print('{0:>30}'.format(passworld))

Yishion_sys_path = r'\\192.168.208.1\Python\factory_Sys'#软件查询目录

#判断X86文件在存在

x86 = r"C:\Program Files (x86)"
if os.access(x86,os.F_OK):
    autoupdate_path = r"C:\Program Files (x86)"
    print("发现Program Files (x86)")
else:
    autoupdate_path = r"C:\Program Files"

updatefile_name = 'autoupdate.exe'#系统更新更新文件名

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

forsn = 0
for r in Yishion_sys_name:
    #获取CAC安装文件路径
    sys_intstall_path = sorted(Path(Yishion_sys_path).glob("**/*{0}.exe".format(Yishion_sys_name[forsn])))
    
    #执行安装
    os.popen(str(sys_intstall_path[0])+" /s")
    print("正在安装{0}".format(Yishion_sys_name[forsn]))
    forsn +=1

print("正在等待更新程序启动，请稍后！")
time.sleep(30)

updatelen = sorted(Path(autoupdate_path).glob("**/autoupdate.exe"))#搜索更新文件所在路径
# x86 = r"C:\Program Files (x86)"
try:
    if os.access(x86,os.F_OK):
        #复制板房更新文件到本地
        copyfile(banfangupdate_root,x86_banfang)
        #执行板房文件更新
        os.popen(x86_banfang)
        print("复制到32位文件夹成功")
    else:
        copyfile(banfangupdate_root,banfangpath_local)
        print("复制到64位文件夹成功")
except:
    print("板房更新文件复制失败，请手动复制更新")

#执行其他系统更新

forsn1 = 0
for x in updatelen:

    os.popen(str(x))
    print("正在更新{0}".format(Yishion_sys_name[forsn1]))
    forsn1 +=1

#执行常办公软件安装
software = sorted(Path(software_patn).glob('**/*.exe'))


print("序列号__Ofiice2007_Sn = DBXYD-TF477-46YM4-W74MH-6YDQ8 ")
print("序列号__VNC6.0_Sn = B7SLM-7MAX5-B4M74-UTDBE-K5WFA ")
for z in software:
    os.popen(str(z))
    print("正在安装{0}".format(z))

os.system(r"\\192.168.208.1\1.电脑部\03.【办公软件】\2007\MicrosoftOfficeProfessionalPlus2007\setup.exe")

print("程序执行完成")
