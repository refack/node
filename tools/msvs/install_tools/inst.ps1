$wc = New-Object System.Net.WebClient;
Invoke-Expression $wc.DownloadString('https://chocolatey.org/install.ps1');
choco upgrade -y python2 visualstudio2017-workload-vctools;
Read-Host 'Type ENTER to exit'