# -*- coding: utf-8 -*-

from socket import *

import os

import struct

ADDR = ('192.168.0.108',9876)

BUFSIZE = 1024

filename = 'wubi.exe'

FILEINFO_SIZE=struct.calcsize('128s32sI8s')

sendSock = socket(AF_INET,SOCK_STREAM)

sendSock.connect(ADDR)

fhead=struct.pack('128s11I',filename,0,0,0,0,0,0,0,0,os.stat(filename).st_size,0,0)

sendSock.send(fhead)

fp = open(filename,'rb')

while 1:

    filedata = fp.read(BUFSIZE)

    if not filedata: break

    sendSock.send(filedata)

print "文件传送完毕，正在断开连接..."

fp.close()

sendSock.close()

print "连接已关闭..."
