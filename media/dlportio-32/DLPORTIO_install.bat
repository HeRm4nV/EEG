copy %~dp0dlportio.dll %SystemRoot%\system32
copy %~dp0dlportio.sys %SystemRoot%\system32\drivers
regedit.exe %~dp0dlportio_reg.reg
pause