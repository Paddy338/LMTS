# 在项目根目录运行
pyinstaller -F -w .\send.pyw --icon .\icons\sendicon.ico
pyinstaller -F -w .\receive.pyw --icon .\icons\receiveicon.ico


$ExeFiles=@(
    ".\dist\send.exe",
    ".\dist\receive.exe"
)
$SpcPath = "$workdir\cert\root.spc"
$PvkPath = "$workdir\cert\root.pvk"


foreach($exe in $ExeFiles){
    if (Test-Path $exe){
        Write-Host "正在为 $exe 添加数字签名..."
        & "D:\Green_Software\cert\signcode.exe" -spc $Spcpath -v $Pvkpath $exe
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
