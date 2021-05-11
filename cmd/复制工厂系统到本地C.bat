xcopy \\192.168.208.1\Python\FactoryERP C:\FactoryERP /e/h/d/y/r/v/k
xcopy \\192.168.208.1\Python\shutdown.bat c:\
mklink %userprofile%\desktop\工厂扫描系统 "c:\FactoryERP\StartERP2.exe"
taskschd.msc