Set WshShell = CreateObject("WScript.Shell")

WshShell.Run """.\exe\control.exe""", 0, False

WScript.Sleep 1000

WshShell.Run """.\exe\monitor.exe""", 0, False