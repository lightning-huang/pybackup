#coding=utf-8
import os,sys,shutil,md5,time,io,binascii
from backupconfig import *

print(sys.getdefaultencoding())
print (sys.stdout.encoding)
def getHash(filePath):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        f = file(filePath)
        bytesfromfile = f.read(picked_size)
        f.close()
        length = os.path.getsize(filePath)
        m1 = md5.new()
        m1.update(bytesfromfile)
        m1.update("%s"%length)
        return m1.hexdigest()

def indexFilePath(folder, dataList):
    for i in os.walk(folder):
        for j in i[2]:
            filepath = i[0] + os.sep + j
            relative2root = filepath[len(folder) + 1:]
            if not relative2root.endswith("baiduyun.downloading"):
                dataList.append(relative2root)


if len(sys.argv)>=3:
    srcfolder = sys.argv[1].decode(codec_name)
    destfolder = sys.argv[2].decode(codec_name)
    if len(sys.argv)==4:
        indexfile=sys.argv[3]
    
    

print "now running python backup.py %s %s"%(srcfolder, destfolder)
indexexists=os.path.exists(indexfile) and os.path.isfile(indexfile)
print "checking index file, exists? %s"%indexexists
if not indexexists:
    print "no indexfile, so we exit"
    sys.exit(-1)
    

print "building filelist to copy..."

srcList=[]
destList=[]

indexFilePath(srcfolder, srcList)
indexFilePath(destfolder, destList)

for item in destList:
    if item in srcList:
        srcList.remove(item)

print "missing file to copy is"
for item in srcList:
    print item
print "totally we have %s files may need to copy"%len(srcList)
print "now check digests"
digesttable={}
f=file(indexfile)
for line in f:
    line=line.strip()
    if line:
        tokens=line.split('\t')
        digesttable[tokens[1]]=1
f.close()

itemstoremove=[]
for item in srcList:
    file_to_check=srcfolder + os.sep + item
    hashvalue=getHash(file_to_check)
    if hash != None and digesttable.has_key(hashvalue):
        itemstoremove.append(item)

print "we have %s which can be removed"%len(itemstoremove)

for item in itemstoremove:
    srcList.remove(item)

if len(srcList) <= 0:
    print "0 files to deal with"
else:
    choice = raw_input("finally, we have %s to copy, let's copy file, copy or not? Y/N"%len(srcList))
    if choice != "Y" and choice != "y":
        sys.exit(0)

    total_count = len(srcList)
    processed = 0 
    for item in srcList:
        print "copy %s from %s to %s"%(item, srcfolder, destfolder)
        dest = destfolder + os.sep + item
        parentfolder = dest[:dest.rfind("\\")]
        parentexists = os.path.exists(parentfolder)
        print "check parent folder exists:%s"%parentexists
        if not parentexists:
            print "make dir: %s"%parentfolder
            os.makedirs(parentfolder)    
        command = "copy /y \"%s\" \"%s\""%(srcfolder + os.sep + item, dest)
        print command
        os.system(command.encode(codec_name))
        processed += 1
        print "finished %s/%s"%(processed, total_count)

    print "backup finished"

choice = raw_input("do you want to remove the files 2 months ago?")
if choice != "Y" and choice != "y":
    sys.exit(0)

for i in os.walk(srcfolder):
    for j in i[2]:
        filepath = i[0] + os.sep + j
        s = os.stat(filepath)
        if not filepath.endswith("baiduyun.downloading.cfg"):
            diff = time.time() - s.st_mtime
            if diff/3600/24 > maxdays:
                print filepath
                command = "del /q /f \"%s\""%filepath
                print command
                os.system(command.encode(codec_name))
print "all done."

        
    


