#!/usr/bin/python
# -*- coding: utf-8 -*-
#cpio -icduv < xx.cpio
from socket import *

import struct,os

def get_local_ip(ifname): 
    import socket, fcntl, struct 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15])) 
    ret = socket.inet_ntoa(inet[20:24]) 
    return ret 

def main(port):
    ADDR = (get_local_ip("eth0"),23216)
    BUFSIZE = 1024
    INFO_FORMAT='128sL128s'
    FILEINFO_SIZE=struct.calcsize(INFO_FORMAT)
    recvSock = socket(AF_INET,SOCK_STREAM)
    recvSock.bind(ADDR)
    recvSock.listen(True)
    print "..."
    conn,addr = recvSock.accept()
    #print ">>>> ",addr
    fhead = conn.recv(FILEINFO_SIZE)

    filename,filesize,dstlocal=struct.unpack(INFO_FORMAT,fhead)
    filename=filename.strip('\00')
    dstlocal=dstlocal.strip('\00')
    #print filename,filesize,dstlocal
    filename = "%s" %os.path.join(dstlocal,filename)
    fp = open(filename,'wb')
    restsize = filesize
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

    fp.close()
    conn.close()
    recvSock.close()
    print "<<<"+filename+"... ",


if __name__=="__main__":
    main(23216)
    #print get_local_ip("eth0") 
