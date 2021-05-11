import pymysql
import sys
class MarDB():
    '''
    安装日志定入数据库
    '''
    try:
        conn = pymysql.connect(
            user = 'pyuser',
            password='VMware1!',
            host = "192.168.208.240",
            port = 3306,
            database = 'DevOps'
        )
    except pymysql.Error as r:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cur = conn.cursor()

    def ssiinsert(self,id=None,host=None,ip=None,message=None,error=None,remark=None,time=None):
        '''
        id = 记录ID
        host = 计算机名
        IP = IP地址
        message = 安装日志
        remark = 备注
        error = 错误提示
        time = 时间
        '''
        try:
            self.cur.execute('''INSERT INTO Ssilog (id,host,ip,message,remark,error,time) VALUES \
                ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')'''.format(id,host,ip,message,remark,error,time))

        except (pymysql.OperationalError,pymysql.IntegrityError) as e:
            print(e,'请输入ID')
        finally:
            self.conn.commit()
            # self.conn.close()
    def ssiselect(self,id=False,host=False,ip=False,message=False,error=False,remark=False):
        '''
        
        查询全部数据
        '''
        a = []
        al = dict(id=id,host=host,ip=ip,message=message,error=error,remark=remark)
        for key,val in al.items():
            if val == True:
                a.append(key)
        keys = tuple(a)
        try:
            if len(keys) == 0:
                self.cur.execute('''select * from Ssilog''')
            elif len(keys) == 1:
                self.cur.execute('''select {0} from Ssilog'''.format(*keys)) 
            elif len(keys) == 2:                            
                self.cur.execute('''select {0},{1} from Ssilog'''.format(*keys))  
            elif len(keys) == 3:                            
                self.cur.execute('''select {0},{1},{2} from Ssilog'''.format(*keys))  
            elif len(keys) == 4:                            
                self.cur.execute('''select {0},{1},{2},{3} from Ssilog'''.format(*keys))  
            elif len(keys) == 5:                            
                self.cur.execute('''select {0},{1},{2},{3},{4} from Ssilog'''.format(*keys))  
        except (pymysql.OperationalError,pymysql.InterfaceError,pymysql.ProgrammingError) as e:
            print(e)
        finally:
            data = self.cur.fetchall()
            return data
            # self.conn.close()
        
    def Ssidelete(self,value):
        '''
        删除记录 values ID 或
        '''
        if type(value) == int:
            try:
                key = input('确认%s删除输入Y,放弃删除输入n:'%value)
                if key == 'y' or 'Y':                                   
                    self.cur.execute('''DELETE FROM Ssilog WHERE id = {0}'''.format(value))
                    print('%s已删除'%value)
                else:
                    pass
            finally:
                self.conn.commit()
                self.conn.close()           
        elif type(value) == str:
            try:
                key1 = input('确认%s删除输入Y,放弃删除输入n:'%value)
                if key1 == 'y' or 'Y':
                    self.cur.execute('''DELETE FROM Ssilog WHERE host = "{0}"'''.format(value))
                    print('%s已删除'%value)
                else:
                    pass
            except pymysql.OperationalError as e:
                print('删除错误，请重新输入',e)
            finally:
                self.conn.commit()
                # self.conn.close() 
if __name__=='__main__':        
    m = MarDB()
    s = m.ssiselect(ip=True,host=True,message=True)
    print(s)
