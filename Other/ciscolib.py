import ciscolib,time,datetime
def main():
    password = "cisco"
    username = "he"
    enable_pwd = ""

    t = datetime.datetime.now()
    ot = t.strftime("%Y-%m-%d")

    for ip in open('sw3750.txt').readlines():
        ip = ip.strip()

        if username != "":
            switch = ciscolib.Device(ip ,password,username,enable_pwd)
        else:
            switch = ciscolib.Device(ip,password,enable_password=enable_pwd)

        try:
            swi    
