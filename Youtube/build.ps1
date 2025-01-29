$parentDir = "C:\Users\mukes\Documents\GitHub\Handy_Tools"
$currentDirName = (Get-Item (Get-Location).Path).Name
if ($currentDirName -ne 'Youtube') {Set-Location "$parentDir\Youtube"}
else {Write-Output "Inside Youtube directory"}
& pyinstaller.exe --onefile gui.py --noconsole
