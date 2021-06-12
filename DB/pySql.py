import pymysql,pprint

class DB(object):
    def __init__(self,database,user,password,host):
        '''
        database 数据库名
        user 数据库帐号
        host 数据库IP地址和主机名
        password 数据密码
        '''
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        
    def connet(self,sql):
        ''''
        sql 执行的sql语句
        '''
        try:
            conn = pymysql.Connect(
                        user = self.user,
                        password=self.password,
                        host = self.host,
                        port = 3306,
                        database = self.database
            )
        except Exception as e:
            print(e)

        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data
if __name__ == "__main__":
    d = DB(database='DevOps',host='192.168.208.240',user='pyuser',password='VMware1!')
    ret = d.connet(sql='select * from Ssilog')
    pprint.pprint(ret)