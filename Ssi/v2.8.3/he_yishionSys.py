# -*- coding: utf-8 -*-
class YishionSys():
    def sysNetworkRoot(self):
        rootPath = r'\\192.168.208.1\Python\factory_Sys'
    def SyslocalRootPath(self):
        followDirectoryPathList = [
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

    def sysNameList(self):
        sysnamelist = [
        "集团总部CAC查询系统","板房系统安装向导","质量检测管理系统","生产总部通知系统","客户加单系统","固定资产管理系统","CAC销售管理系统安装",\
            "董事长通知系统","后勤采购管理系统","CAC工厂管理系统安装","生产总部人员管理系统安装程序","车辆管理系统","集团CAC物料系统"]
