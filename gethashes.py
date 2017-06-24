#coding=utf-8
import os,sys,shutil,md5

from backupconfig import *
hashbox={}

def getHash(filePath):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        f = file(filePath)
        bytesfromfile = f.read(picked_size)
        f.close()
        length = os.path.getsize(filePath)
        if length<=0: return None
        m1 = md5.new()
        m1.update(bytesfromfile)
        m1.update("%s"%length)
        return m1.hexdigest()
    return None


for i in os.walk(destfolder):
    for j in i[2]:
        filepath = i[0] + os.sep + j
        hashcode = getHash(filepath)
        if hashcode != None:
            if hashbox.has_key(hashcode):
                command = "del /q /f \"%s\""%filepath
                debuginfo = "md5: %s, duplicate (%s) with (%s)"%(hashcode, filepath, hashbox[hashcode])
                print debuginfo
                print command
                os.system(command.encode(codec_name))
            else:
                hashbox[hashcode]=filepath

f=file(hashfile,"w")
for key in hashbox:
    f.write(("%s\t%s\n"%(hashbox[key], key)).encode(codec_name))
f.close()
