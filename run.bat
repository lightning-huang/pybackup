chcp 936
cd C:\Python27\src 
echo build index and clear the duplicates
..\python gethashes.py
echo build index complete
..\python backup.py
pause