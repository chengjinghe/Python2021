
import pymysql
import sys
class YishionSsiAutoSql():
    '''SsiAuto专用库'''
    def connet(self,database='SsiAutoWin7'):
        '''
        database 数据库名称
        '''
        try:
            conn = pymysql.connect(
                user = 'ssiauto',
                password='VMware1!',
                host = "192.168.208.240",
                port = 3306,
                database = database
            )
        except pymysql.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        return conn
    def ssiAutoQuery(self,procName=None):
        '''SsiAutoKey'''
        if procName == None:
            return 'ssiAutoQuery进程名为空'
        else:
            try:
                conn = self.connet()
                cur = conn.cursor()
                cur.execute(f'''select * from {procName}''')
                data = cur.fetchall()
                return data
            except:
                return 'ssiAutoQuery数据查询错误'

    def ssiAutoInsert(self,tableName=None,Autokeys=None):
        '''数据维护专用函数'''
        Autokeys = [('ocr001fn.PNG'),(610,530),(610,530),('ocr002fn.PNG'),(610,530)]
        for nameindex,name in enumerate(Autokeys):
            conn = self.connet()
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO {tableName} (id,data) VALUES ({nameindex},'{name}')''')
            conn.commit()




if __name__=='__main__':        
    m = YishionSsiAuto()
    # s = m.ssiAutoInsert(tableName='AdbeRdr930')
    # print(s)
    s1 = m.ssiAutoQuery(procName='AdbeRdr930')
    print(s1)
# 