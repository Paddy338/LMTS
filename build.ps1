# 在项目根目录运行
# 绝对路径均为本人电脑上的路径，需要修改
chcp 65001
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Clear-Host

# 虚拟环境
cd D:\Develop\LMTS\ 
.\.venv\Scripts\Activate.ps1

# 清理
rmdir -path ".\build\" -recurse
rmdir -path ".\dist\" -recurse
del .\send.spec
del .\receive.spec

# 打包
PyInstaller -F -w  --icon .\icons\sendicon.ico `
--strip --exclude-module test `
--exclude-module unittest `
--exclude-module tkinter.dnd `
--exclude-module tkinter.tix `
--hidden-import ttkbootstrap `
--upx-dir=.
.\send.pyw

PyInstaller -F -w  --icon .\icons\receiveicon.ico `
--strip --exclude-module=test `
--exclude-module unittest `
--exclude-module tkinter.dnd `
--exclude-module tkinter.tix `
--hidden-import ttkbootstrap `
--upx-dir=.
.\receive.pyw

# 签名
$ExeFiles=@(
    "D:\Develop\LMTS\dist\send.exe",
    "D:\Develop\LMTS\dist\receive.exe"
)
$SpcPath = "D:\Develop\LMTS\cert\Paddy338.spc"
$PvkPath = "D:\Develop\Paddy338.pvk" # 不在仓库里，仓库里只有公钥


foreach($exe in $ExeFiles){
    if (Test-Path $exe){
        Write-Host "Signing $exe ... / 正在为 $exe 添加数字签名...`n"
        & "D:\Green_Software\cert\signcode.exe" -spc $Spcpath -v $Pvkpath -a sha1 -t http://timestamp.digicert.com $exe
        if($LASTEXITCODE -eq 0){
            Write-Host "√ Successfully signed / 签名成功"
        }
        else{
            Write-Error "Signing failed: $exe / 签名失败：$exe"
        }
    }
    else{
        Write-Warning "File not found: $exe / 找不到文件：$exe"
    }
}

pause