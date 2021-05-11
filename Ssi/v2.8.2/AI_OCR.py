# -*- coding: UTF-8 -*-
import os
# os.system('pip install pyautogui')
# os.system('pip install psutil')
import pyautogui,time,psutil,socket
from pathlib import Path
class Install():
    run_sn = 0
    run_name = ''
    imagelist = []
    Ocr_Root_Image_file = r'Ocr_Root_Image'  # 需要识别的图片保存的目录
    PyAuto_image_Path_Root = r'\\192.168.208.1\Python\PyAutoGui'  # 所有PyAutoGui用图根目录
    Istall_root = r'\\192.168.208.1\Python'
    one_key_list = ['sougoupingying','WeChatSetup','WeCom','360zip_setup']#只用一键就能安装的软件名单
    Software_Name = []  # 保存所有等待识别的 安装软件文件夹文件名字
    Erection_Schedule = []
    factory_Software = 'factory_Software'
    Software_Name_list = sorted(Path(os.path.join(Istall_root,factory_Software)).glob('**/*.exe'),key=os.path.getctime,reverse=True)
    PPoint = [] # Point 坐标列表
    for name in Software_Name_list:
        Erection_Schedule.append(name.name)#安装包名称写到Software_Name列表 #进程名称
        Software_Name.append(name.stem)#安装包软件名称

    # 单个软件安装OCR临时列表
    def __Software_Key(self,Software_name=None):
        Point = ''
        rtx_key = [2,1,2,1,'pause20' ,0]#腾讯通安装快捷建
        sougouwubi_key = [2, 1, 2, 2, 1, 'pause10', 0, 'pause1.5', 2, 'tab_x2', 'down', 2, 2, 2, 0]#搜狗五笔安装快捷建
        vnc6_key = [2,'tab',5,2,'down','down','space','down','space',2,2,2,1,'pause20',0]#vnc快捷键
        vnc6_input_licese_key = [2,'tab','input_key',2,'enter']
        sougoupingying_key = ['ocr','ocr']
        Office2007_Excel_Work_Power_point = ['ocr']
        Adobe_Reader_key = [2,1,'pause40',0]
        WeCom = ['ocr','pause1.5','terminate']
        WeChatSetup = ['ocr']
        pdfprint = [6,5,'ocr','enter']
        zip_360_setup =['ocr','ocr','ocr']
        # Software_name = [sougouwubi_key,rtx_key,vnc6_key,sougoupingying_key,Adobe_Reader_key,Office2007_Excel_Work_Power_point]
        all_key = {'WeCom':WeCom,'WeChatSetup':WeChatSetup,'rtxcsetup':rtx_key,'realvncsetup':vnc6_key,'pdf3.52pro-chs':pdfprint,'AdbeRdr930_zh_CN':Adobe_Reader_key,\
                   '360zip_setup':zip_360_setup,'sougoupingying':sougoupingying_key,'sougouwubi':sougouwubi_key}

        return all_key.get(Software_name)# 返回对应的key

    def i(self):
        whilesn = 0
        Point = ''
        filesn = []#软件安装 首页截图
        Soft_Start = 'Soft_Start'
        all_start_root = sorted(Path(os.path.join(self.PyAuto_image_Path_Root,Soft_Start)).glob('**/*.png'))# 所以软件开始首页图片
        while True:
            if whilesn == 5:
                print('识别结束,程序正在退出!')
                break
            whilesn +=1
            print('第%s轮正在识别' % whilesn)
            for install_start_File in all_start_root:#遍历并列出有所文件
                filesn.append(install_start_File.name)#将文件名写到Filesn列表
                print('正在识别%s'%install_start_File.name)
                install_start_Files = str(install_start_File)
                Point = pyautogui.locateCenterOnScreen(install_start_Files)#取出一张图片对电脑桌面进行比对

                #匹配成功
                if Point != None:
                    if install_start_File.stem in self.one_key_list: #判断是否是只需为一键安装
                        self.run_name = install_start_File.stem #比对成功的图片文件名 非常重要 #赋值给全局u
                        self.run_sn = self.Software_Name.index(install_start_File.stem)#获取比对成功的文件名 在所有所需安装的列表的索引
                        pyautogui.click(Point)
                        pyautogui.click(0, 1)
                        self.__ocrnext(sft_name=install_start_File)
                    else:
                        whilesn = 0
                        pyautogui.click(Point)
                        self.Point = Point
                        file_index = filesn.index(install_start_File.name)#取得当前名字在列表的索引
                        print(install_start_File.name)
                        self.run_name = install_start_File.stem
                        self.run_sn = self.Software_Name.index(install_start_File.stem)
                        self.__action()
    def __action(self):
        alt = 'alt'
        key = ['f','i','n','p','c','a','y']
        inter = 0.1
        pyautogui.click(self.Point, interval=inter)
        for key_sn in self.__Software_Key(Software_name=self.run_name):
            print('{0}正在执行安装{1}'.format(self.Software_Name[self.run_sn],key_sn))
            if type(key_sn) == int:
                pyautogui.hotkey(alt, key[key_sn], interval=inter)
            elif key_sn == 'pause1.5':
                time.sleep(1.5)
            elif key_sn == 'pause10':
                time.sleep(10)
            elif key_sn == 'pause20':
                time.sleep(20)
            elif key_sn == 'pause15':
                time.sleep(15)
            elif key_sn == 'pause40':
                time.sleep(40)
            elif key_sn == 'pause1':
                time.sleep(1)
            elif key_sn == 'tab_x2':
                pyautogui.press('tab', presses=2)
            elif key_sn == 'down':
                pyautogui.press('down')
            elif key_sn == 'space':
                pyautogui.press('space')
            elif key_sn == 'ocr':
                Point = self.__ocrnext()
                pyautogui.click(Point)
                pyautogui.moveTo(0, 0)
            elif key_sn == 'terminate':
                if self.run_name == 'WeCom':
                    self.__psut(name='WXWork.exe')
        self.install_sfoware_name = '' #初始化正在安装名字的全局变量
        self.sn = 0

    def __ocrnext(self,sft_name = None):
        sft_list = sorted(Path(os.path.join(self.PyAuto_image_Path_Root, self.Ocr_Root_Image_file, \
                                            self.Software_Name[self.run_sn])).glob('**/*n.PNG'))  # 每个软件所有图片的扫描文件路径
        for ocrfile in sft_list:
            Point = self.__ocrAI(ocr_file_name=ocrfile)  # 识别当前屏幕新动态
            print(ocrfile)
            pyautogui.click(Point)
            pyautogui.moveTo(0, 1)
        print('%s安装结束，正等待完成安装' % ocrfile.stem)
        if sft_name == None:
            pass
        else:
            self.__psut(name=sft_name.stem + '.exe')  # 结束安装进程
            print('ok' * 10)
            self.sn = 0
            time.sleep(5)

    #截图保存
    def __coordinates(self):
        '''
        :param Ocr_root_Image_file: 截图保存的路径，需要有读写权限
        :return:
        '''
        Ocr_Root_Path = os.path.join(self.PyAuto_image_Path_Root,'Ocr_Image')#所有截图保存路径
        pchostname = socket.gethostname()
        localhost_image_path = os.path.join(Ocr_Root_Path,pchostname)
        if os.path.exists(localhost_image_path):#判断路径是否存在
            pass
        else:
            localhost_image_path = os.mkdir(localhost_image_path)#创建以本地计算机名的文件夹，用来保存后面截图的路径
        try:
            file_name = self.__localtime() + '.PNG'
            ocr_file = os.path.join(localhost_image_path,file_name)#生成以当前时间为名的文件图像
            time.sleep(5)
            pyautogui.screenshot(ocr_file)#识别生成的文件图像
            Point = self.__ocrAI()
            # return ocr_file #返回最新截图文件路径
            return Point
        except Exception as e:
                print(e)
    # 图像识别
    def __ocrAI(self,ocr_file_name=None):
        if ocr_file_name == None:
            return
        Point = pyautogui.locateCenterOnScreen(str(ocr_file_name))
        for _ in range(50):
            time.sleep(2)
            if Point == None:
                print('正在识别的图片为%s'%ocr_file_name)
                Point = pyautogui.locateCenterOnScreen(str(ocr_file_name))
            else:
                return Point
    #清理进程
    def __psut(self,name=None):
        if name == None:
            return
        else:
            try:
                for p in psutil.process_iter(attrs=['name', 'pid']):
                    if p.name() == name:
                        s = psutil.Process(p.pid)
                        s.terminate()#结束name进程
            except Exception as e:
                print(e)
    #返回时间
    def __localtime(self):
        localtime = time.localtime()
        localtime = time.strftime("%Y-%m-%d_%H-%M-%S", localtime)
        return localtime#返回当前时间

if __name__=="__main__":
    i = Install()
    i.i()
