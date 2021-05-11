Active code page:65001
netsh interface ip set address name="本地连接" source=static addr=192.168.211.75 mask=255.255.254.0 
netsh interface ip set address name="本地连接" gateway=192.168.210.254 gwmetric=0
netsh interface ip add dns name = "本地连接" addr = 8.8.8.8
netsh interface ip add dns name = "本地连接" addr = 202.96.128.86
