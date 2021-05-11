import os,time
from pathlib import Path
#返回文件的最后修改时间
class F1():
    s = []
    def __mt(self,fpath=None):
        
        a = time.localtime(os.stat(fpath).st_atime)
        a = time.strftime("%Y-%m-%d %H:%M:%S ",a)
        acctime_fname = str(a) + str(fpath)#访问时间加文件名称
        self.s.append(acctime_fname)#获取到的时间和路径写入列表

    def fp(self,folder):
                
        x = sorted(Path(folder).glob('**/*'))#需要查询的目录和文件名
        fsn = 0 #循环序号
        for t in x:
            ftime = self.__mt(fpath=x[fsn])#获需要查询时间的文件__完整路径
            fsn +=1
        return self.s
m1 = F1()

m = m1.fp(folder=r"D:\Soft")#填入需要查询的路径

for e in m:
    print(e)