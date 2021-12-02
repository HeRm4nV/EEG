copy %~dp0DLPortIO.dll %SystemRoot%\SysWOW64
copy %~dp0DLPortIO.sys %SystemRoot%\system32\drivers
regedit.exe %~dp0DLPortIO_reg.reg
pause
