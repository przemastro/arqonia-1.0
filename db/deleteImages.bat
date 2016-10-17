@echo off
forfiles /p "C:\Users\Przemek\Desktop\arqonia\backend\rest\inputFits" /s /m *.* /d -1 /c "cmd /c echo @path @fdate"
forfiles /p "C:\Users\Przemek\Desktop\arqonia\backend\rest\inputFits" /s /m *.* /d -1 /c "cmd /c echo del @path"
forfiles /p "C:\Users\Przemek\Desktop\arqonia\backend\rest\outputFits" /s /m *.* /d -1 /c "cmd /c echo @path @fdate"
forfiles /p "C:\Users\Przemek\Desktop\arqonia\backend\rest\outputFits" /s /m *.* /d -1 /c "cmd /c echo del @path"
forfiles /p "C:\Users\Przemek\Desktop\arqonia\frontend\app\inputFits" /s /m *.* /d -1 /c "cmd /c echo @path @fdate"
forfiles /p "C:\Users\Przemek\Desktop\arqonia\frontend\app\inputFits" /s /m *.* /d -1 /c "cmd /c echo del @path"
sqlcmd -S DESKTOP-4UP85UJ\SQLEXPRESS -i C:\Users\Przemek\Desktop\arqonia\db\deleteImages.sql
pause