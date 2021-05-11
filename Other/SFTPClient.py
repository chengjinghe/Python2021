import paramiko

username = "root"
passworld = "**************"
hostname = "TH.Test.com"
port = 22
try:
    t = paramiko.Transport((hostname,port))
    t.connect(username=username,password=passworld)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put("/home/user/info.db","/data/user/info.db")
    sftp.get("/data/user/info.db","/home/user/info.db")
    sftp.mkdir("/user/Test1",0755)
    sftp.rmdir("/user/Test1")
    sftp.rename("home/userfile.py","home/userfile1.py")
    print sftp.stat("home/userfile1.py")
    print sftp.stat("home")
    t.close
except Exception,e:
    print str(e)
            SystemError
            