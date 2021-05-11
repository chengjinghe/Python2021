import pymysql

try:
    conn = pymysql.Connect(
                user = 'pyuser',
                password='VMware1!',
                host = "192.168.208.240",
                port = 3306,
                database = 'DevOps'
    )
except Exception as e:
    print(e)

cur = conn.cursor()

cur.execute('''select * from Ssilog''')
data = cur.fetchall()
print(data)

print('hello,python'*99)