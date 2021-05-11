from pathlib import Path
from shutil import copyfile
import os,time

def Time(bbc):
    def htime(*args):
        start = time.time()
        bbc(*args)
        stop = time.time()
        print(stop - start)
    return htime


class CFile:
    dst_Directory = r'\\192.168.208.1\Python\factory_Sys'#公司专用系统安装包_预保存目标
    factoy_root_Path = r'\\192.168.0.17\CACUpdate'#服务器上的目录
    #需要安装的软件名字
    factoy_root_Name = [    
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

    @Time
    def run_copy(self):
        self.run_del()#删除原有的安装包
        forsn1 = 0 #循环序列号
        
        for x in self.factoy_root_Name:
            #生成安装包文件名
            dst_pant = (x + '.exe')
            #目标路径生成
            dst_name = os.path.join(self.dst_Directory,dst_pant)
            #列出安装包所在目录
            factory_sys_name = sorted(Path(self.factoy_root_Path).glob('**/{0}.exe'.format(self.factoy_root_Name[forsn1])))
            #复制文件到目标目录
            copyfile(str(factory_sys_name[0]),dst_name)#复制到文件到目标目录

            forsn1 +=1
    
    @Time
    def run_del(self):
        forsn2 = 0
        for x in self.factoy_root_Name:

            dst_pant = (x + '.exe')
            #列出安装包所在目录
            dst_name = os.path.join(self.dst_Directory,dst_pant)
            #执行删除
            os.remove(str(dst_name))
            


c = CFile()

c.run_copy()


