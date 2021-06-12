from datetime import date
import pandas as pd
from IPy import IP
import pprint,sys,os,datetime
sys.path.append(r'D:\DevOps\Python')
from yishionreg import Reg
reg = Reg()#注册表实例化
from Pandas.IP.Marsql import MarDB
msql = MarDB()
def leisure_IP(savefile=True):
    '''
    IP空闲查询工具，只能查询第三位的 如(220) 
    '''
    Trieslimit = 3 #次数限制
    while Trieslimit:
        try: 
            network_segment = input(str('请输入要查询的网段 如(220)：'))
            if len(network_segment) != 3:
                    Trieslimit -= 1
                    print('错误，请重新输入')
                    if Trieslimit == 0: #输入错误达3次，则退出程序
                        sys.exit()
            else:
                net_Mask = f'192.168.{network_segment}.'
                if net_Mask != None:
                    break
        except Exception as e:
            print('输入错误',e)
            sys.exit()
    #读取深信服导出的IP表文件       
    # data =  pd.read_excel(r"C:\Users\Administrator\Desktop\10-23\ip.xlsx",skiprows=11)#源数据文件保存路径，文件为0.248深信服防火墙导出，并且跳过前11行注释  
    data =  pd.read_excel(r"C:\Users\Administrator\Desktop\10-23\ip(5-20).xlsx",skiprows=11)#源数据文件保存路径，文件为0.248深信服防火墙导出，并且跳过前11行注释  
    Source_IP_column = data[data.columns[0]]#读取第0列的数据
    Assign_Full_IP = IP(f'{net_Mask}0/24')

    #使用中的IP地址列表
    Sic_ip = []
    for ip in Source_IP_column:
        if ip[1:13] == net_Mask:
            Sic_ip.append(str(ip[1:]))

    #指定网段的IP的所有IP地址
    Full_IP = []
    for ip1 in Assign_Full_IP:
        Full_IP.append(str(ip1))

    #转换为集合
    Sic_ip = set(Sic_ip)
    Full_IP = set(Full_IP)

    #计算集合差集（算出没有使用的IP）
    Free_IP = Full_IP.difference(Sic_ip)
    
    FL = pd.DataFrame(Free_IP)
    try:
        for ip1 in (list(Free_IP)):
            msql.IPinsert(ip=ip1,time=date.today())
    except Exception as e:
        print(e)
    if savefile == False:#是否需要保存文件到桌面 ；默认保存
        pass
    else:
        try:
            FL.to_excel(os.path.join(reg.get_desktop,f'{network_segment}.xlsx'),index=False)
        except IOError as err:
            pass
    return list(Free_IP)
     
Data = leisure_IP(savefile=False)
print(Data,len(Data))

