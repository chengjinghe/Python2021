import psutil
class IP_Psutil():
    P = psutil.net_if_addrs()
    pids = psutil.pids()
    @property
    def IPV4(self):
        for x,r in self.P.items():
            if len(r) == 2 and x == '以太网':
                return r[1]
            elif len(r) == 2 and x == '本地连接':
                return r[1]

    def pid(self,PidName=[]):
        '''
        PidName = [] 进程列表
        '''
        r = []
        r1 = []
        if PidName == None or PidName == []:
            print('请输入文件名称') 
            return
        else:
            for x in self.pids:
                if x == 0 : continue
                proc = psutil.Process(x)
                for c in PidName:
                    if proc.name() == c :
                        a = proc.cwd()
                        r.append(a)
                        a1 = proc.pid
                        r1.append(a1)
        return (r,r1)
if __name__ == '__main__':                                                     
    I = IP_Psutil()
    I.pid()