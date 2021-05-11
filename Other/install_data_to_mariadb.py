import sqlite3,time,os,sys
import mariadb
# sqlite3_install_tables_name = 'eventid','hostname','clock','error','message'

try:
    conn = mariadb.connect(
        user="pyuser",
        password="VMware1!",
        host="192.168.208.240",
        port=3306,
        database="DevOps"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute('select * from Dimission;')
data = cur.fetchone()
print(data)