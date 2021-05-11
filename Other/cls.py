import os,time
from pathlib import Path
from pathlib import PurePath
class Mtime():
    filepath = ''
    def __init__(self,filepath=filepath):
        self.filepath = filepath
    def file_atime(self):
        FileNameDict = {}
        FileFullPath = sorted(Path(self.filepath).glob('**/*'))#列出filepath路径下所有文件的路径
        for x in FileFullPath:
            FileName = PurePath(x).name#获取文件名
            FileAttributes = os.stat(x)
            atime = time.gmtime(FileAttributes.st_atime)
            atime = time.strftime("%Y-%m-%d %H-%M-%S",atime)
            FileNameDict.setdefault(FileName,atime)
            # FileNameList.append(FileName)
        return FileNameDict
m1 = Mtime(filepath=r'\\192.168.208.1\Python')
m = m1.file_atime()
c = sorted(m.items(),key=lambda item:item[1],reverse=False)
print(c)
#a.st_atime 最后访问时间
#a.st_mtime 最后修改时间
#a.st_ctime 文件创建时间
