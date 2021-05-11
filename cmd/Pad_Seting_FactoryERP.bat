@echo off
%windir%\system32\cmd.exe /k %windir%\System32\reg.exe add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
@REM reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Parameters /v ntpserver /d 192.168.0.201,0x9 /t REG_SZ /f
@REM xcopy \\192.168.208.1\Python\FactoryERP C:\FactoryERP\ /e/h/d/y/r/v/k
@REM xcopy \\192.168.208.1\Python\shutdown.bat c:\
@REM xcopy \\192.168.208.1\Python\shutdown1.xml c:\
@REM mklink %userprofile%\desktop\FactoryERP "c:\FactoryERP\StartERP2.exe"
taskschd.msc
@REM C:\FactoryERP\StartERP2.exe
echo hello worl!
pause
