import time
class YishionTime(object):
    '''时间显示样式函数'''
    @property
    def currentTime(self):
        '''
        返回 Y-m-d H-M-S:时间样式
        '''
        localtime = time.localtime()
        Rtime = time.strftime("%Y-%m-%d %H-%M-%S:", localtime)
        return Rtime

    @property
    def marTime(self):
        '''
        返回 YmdHMS 时间样式
        '''
        localtime = time.localtime()
        rRtime = time.strftime("%Y%m%d%H%M%S", localtime)
        return rRtime