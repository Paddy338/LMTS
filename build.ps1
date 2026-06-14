# 在项目根目录运行
# 绝对路径均为本人电脑上的路径，需要修改
chcp 65001
Clear-Host

# 虚拟环境
cd D:\Develop\LMTS_second_dev\ 
.\.venv\Scripts\Activate.ps1

# 清理
rmdir -path ".\build\" -recurse
rmdir -path ".\dist\" -recurse
del /f .\*.spec

# 打包
PyInstaller -F -w  --icon .\icons\sendicon.ico `
--strip --exclude-module test `
--exclude-module unittest `
--exclude-module tkinter.dnd `
--exclude-module tkinter.tix `
--hidden-import ttkbootstrap `
.\send.pyw

PyInstaller -F -w  --icon .\icons\receiveicon.ico `
--strip --exclude-module=test `
--exclude-module unittest `
--exclude-module tkinter.dnd `
--exclude-module tkinter.tix `
--hidden-import ttkbootstrap `
.\receive.pyw

# 签名
$ExeFiles=@(
    "D:\Develop\LMTS_second_dev\dist\send.exe",
    "D:\Develop\LMTS_second_dev\dist\receive.exe"
)
$SpcPath = "D:\Develop\LMTS_second_dev\cert\root.spc"
$PvkPath = "D:\Develop\LMTS_second_dev\cert\root.pvk"


foreach($exe in $ExeFiles){
    if (Test-Path $exe){
        Write-Host "正在为 $exe 添加数字签名..."
        & "D:\Green_Software\cert\signcode.exe" -spc $Spcpath -v $Pvkpath -a sha1 -t http://timestamp.digicert.com $exe
        if($LASTEXITCODE -eq 0){
            Write-Host "√ 签名成功"
        }
        else{
            Write-Error "签名失败：$exe"
        }
    }
    else{
        Write-Warning "找不到文件：$exe"
    }
}

pause