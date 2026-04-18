# 在项目根目录运行
python -m PyInstaller -F -w .\send.pyw --icon .\icons\sendicon.ico
python -m PyInstaller -F -w .\receive.pyw --icon .\icons\receiveicon.ico


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