from datetime import date
import pandas as pd
from IPy import IP
import sys,os
from yishionreg import Reg
reg = Reg()#注册表实例化
from he_ip_marsql import MarDB
msql = MarDB()

print(
    '''
    本程序源文件IP地信息由深信服防火墙导出
    如需计算最新的IP,请替换IP.xlsx文件
    '''
)

def auto_display():
    masklist = ['208','209','210','211','212','213','214','218','219','220','221','222','224','230','231','232']
    full_ip = dict()
    source_Full_IP = dict()
    # try:
    #     file = os.path.join(os.getcwd(),"ip.xlsx")
    # except OSError as er2:
    #     print('ip.xlsx 文件错误！')
    #     sys.exit()
    file = (r"D:\DevOps\Python\ipSys\ipSys2.2\ip.xlsx")        
    data =  pd.read_excel(file,skiprows=11)#源数据文件保存路径，文件为0.248深信服防火墙导出，并且跳过前11行注释  
    for net_Mask in masklist:
        Source_IP_column = data[data.columns[0]]#读取第0列的数据
        ipmank = (f'192.168.{net_Mask}.')
        source_ipmank = IP(f'192.168.{net_Mask}.0/24')
    
        Sic_ip = []#单个指定网段已经使用的所有IP
        for ip in Source_IP_column:
            if ip[1:13] == ipmank:#判断单个网段
                Sic_ip.append(str(ip[1:]))
        full_ip.update({f'{net_Mask}':Sic_ip})

        sou_ip_list = []
        for sip in source_ipmank[1:-1]:
            sou_ip_list.append(str(sip))    
        source_Full_IP.update({f'{net_Mask}':sou_ip_list})

    free_ip = dict()
    for mask_ip in masklist:
        # print(type(full_ip.get(mask_ip)[1]),type(source_Full_IP.get(mask_ip)[1]))
        free =  set(source_Full_IP.get(mask_ip)).difference(set(full_ip.get(mask_ip)))
        free_ip.update({f'{mask_ip}':free})
    return free_ip


def leisure_IP(savefile=True):
    '''
    IP空闲查询工具，只能查询第三位的 如(220) 
    '''
    Trieslimit = 3 #次数限制
    while Trieslimit:
        try: 
            network_segment = input(str('请输入要查询的网段,完成按Enter(回车) |如(220)：'))
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
    # try:
    #     file = os.path.join(os.getcwd(),"ip.xlsx")
    # except OSError as err1:
    #     print('ip.xlsx 文件错误',err1)
    #     sys.exit()   
    file = (r"D:\DevOps\Python\ipSys\ipSys2.2\ip.xlsx")    
    data =  pd.read_excel(file,skiprows=11)#源数据文件保存路径，文件为0.248深信服防火墙导出，并且跳过前11行注释  
    Source_IP_column = data[data.columns[0]]#读取第0列的数据
    Assign_Full_IP = IP(f'{net_Mask}0/24')


    #使用中的IP地址列表
    Sic_ip = []
    for ip in Source_IP_column:
        if ip[1:13] == net_Mask:
            Sic_ip.append(str(ip[1:]))

    #指定网段的IP的所有IP地址
    Full_IP = []
    for ip1 in Assign_Full_IP[1:-1]:
        Full_IP.append(str(ip1))

    #转换为集合
    Sic_ip = set(Sic_ip)
    Full_IP = set(Full_IP)

    #根据查询名字
    for data_index,datas in data.iterrows():
        if datas.iloc[0][1:13] == net_Mask:
            data_index,datas.iloc[0],datas.iloc[1]

    #计算集合差集（算出没有使用的IP）
    Free_IP = Full_IP.difference(Sic_ip)
    
    FL = pd.DataFrame(Free_IP)
    try:
        for ip1 in (list(Free_IP)):
            # msql.IPinsert(ip=ip1,time=date.today())
            pass
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

if __name__ == '__main__':
    ip = auto_display()

    for mask,address in ip.items():
        print('网段:',mask,": ",'剩余',len(address),'|   ','1个： ',list(address)[0])

    try:
        c = str(input('退出或请按(enter),继续请输入(C)!: '))
    except ValueError as e1:
        sys.exit()


    if c == 'c' or c== 'C':
        Data = leisure_IP(savefile=False)
        try:
            try:
                sn = int(input('需要显示的IP数量,完成按Enter(回车) | 默认(3), 全部显示请输入(0) :'))
            except ValueError:
                sn = 3
                print('可用IP：',Data[:sn],"IP剩余数量：",len(Data))
            
            if sn == 0 :
                print('可用IP数量',len(Data))
                for ipindex,ipdata in enumerate(Data):
                    if ipindex %5 ==0 :
                        print('\n')
                    print(ipindex+1,': ',ipdata,end='\t')
                print('\n')

            elif sn != 3:
                print('可用IP：',Data[:sn],"IP剩余数量：",len(Data))
            else:
                pass
        except ValueError as e:
            print('输入错误！')

        exit = input('按任意键退出...')
    else:
        pass