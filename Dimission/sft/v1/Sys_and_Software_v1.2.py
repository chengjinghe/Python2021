from pathlib import Path
from shutil import copyfile
import os,time
print('''本程序最后更新版本时间 2021-1-29
        1,程序会自动跳过已经安装的系统，
        2,会自动打开SN文件,请手动关闭该文件
        ''')
software_patn = r"\\192.168.208.1\Python\factory_Software"
time.sleep(10)
s = "正在安装通用系统_请稍后!!!"
b = "10秒后开始执行"
user = "请先输入192.168.0.17 用户名 ： Guest"
passworld = "请先输入192.168.0.17 密码 ： Yscac2018"

print('{0:-^60}'.format(s))
print('{0:>40}'.format(b))
print("{0:=^10}".format(user))
print("{0:-^10}".format(passworld))

Yishion_sys_path = r'\\192.168.208.1\Python\factory_Sys'#软件查询目录

#判断X86文件在存在

x86 = r"C:\Program Files (x86)" #x86文件路径
NoX86 = r"C:\Program Files"#非X86文件路径
try:
    if os.access(x86,os.F_OK):
        autoupdate_path = r"C:\Program Files (x86)"
        print("发现Program Files (x86)")
    else:
        autoupdate_path = r"C:\Program Files"

    updatefile_name = 'autoupdate.exe'#系统更新更新文件名
except:
    print('系统安装错误，请手动安装')
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
            print("已经安装{0}，已经成功跳过".format(Yishion_sys_name[forsn])) 
            forsn +=1                              
        else:
            os.popen(str(sys_intstall_path[0])+" /s")
            print("!!正在安装{0}!!!".format(Yishion_sys_name[forsn]))
            forsn +=1                   
    except:
        print("通用系统安装出错，请手动执行安装")

print("正在等待更新程序启动，请稍后！")
os.popen(r"\\192.168.208.1\Python\factory_Software\sn.txt")#打开SN文件

time.sleep(30)

try:
    updatelen = sorted(Path(autoupdate_path).glob("**/autoupdate.exe"))#搜索更新文件所在路径
    #执行其他系统更新
    forsn1 = 0
    try:
        for x in updatelen:
            os.popen(str(x))
            print("正在更新{0}".format(Yishion_sys_name[forsn1]))
            forsn1 +=1
    except:
        print('系统更新失败，请手动检查更新')

     #复制板房更新文件到本地
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
except:
    print("更新文件路径查询错误")

print("正在启动软件安装，请稍后！")
time.sleep(30)
#执行常办公软件安装

print("序列号__Ofiice2007_Sn = DBXYD-TF477-46YM4-W74MH-6YDQ8 ")
print("序列号__VNC6.0_Sn = B7SLM-7MAX5-B4M74-UTDBE-K5WFA ")
try:
    software = sorted(Path(software_patn).glob('**/*.exe'))
    for z in software:
        os.popen(str(z))
        print("正在安装{0}".format(z))
except:
    print("软件安装错误，请手动安装")


#office安装 和 CAC注册表写入
try:
    os.system(r"\\192.168.208.1\1.电脑部\03.【办公软件】\2007\MicrosoftOfficeProfessionalPlus2007\setup.exe")
    os.system(r"\\192.168.208.1\Python\factory_Sys\所有CAC数据库注册表.reg")
except:
    print("office 安装错误 请手动执行！")
    print("CAC注册表未成功写入！，请手动执行")
print('请关闭SN文件')
print("程序执行完成")
