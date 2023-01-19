$appPath = (Get-Item $PSScriptRoot\main.exe).FullName
Start-Process -WindowStyle hidden -FilePath $apppath