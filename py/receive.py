# -*- coding: utf-8 -*-

from socket import *

import struct

ADDR = ('192.168.0.108',9876)

BUFSIZE = 1024

FILEINFO_SIZE=struct.calcsize('128s32sI8s')

recvSock = socket(AF_INET,SOCK_STREAM)

recvSock.bind(ADDR)

recvSock.listen(True)

print "等待连接..."

conn,addr = recvSock.accept()

print "客户端已连接—> ",addr

fhead = conn.recv(FILEINFO_SIZE)

filename,temp1,filesize,temp2=struct.unpack('128s32sI8s',fhead)

#print filename,temp1,filesize,temp2

print filename,len(filename),type(filename)

print filesize

filename = 'new_'+filename.strip('\00') #...

fp = open(filename,'wb')

restsize = filesize

print "正在接收文件... ",

while 1:

    if restsize > BUFSIZE:

        filedata = conn.recv(BUFSIZE)

    else:

        filedata = conn.recv(restsize)

    if not filedata: break

    fp.write(filedata)

    restsize = restsize-len(filedata)

    if restsize == 0:

     break

print "接收文件完毕，正在断开连接..."

fp.close()

conn.close()

recvSock.close()

print "连接已关闭..."
