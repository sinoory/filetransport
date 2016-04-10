# -*- coding: utf-8 -*-
from socket import *
import os,sys
import struct
from optparse import OptionParser
def send(filename,ip,dstlocal='~/',port=23216):
    ADDR = (ip,port)
    BUFSIZE = 1024
    INFO_FORMAT='128sL128s'
    FILEINFO_SIZE=struct.calcsize(INFO_FORMAT)
    sendSock = socket(AF_INET,SOCK_STREAM)
    sendSock.connect(ADDR)
    fhead=struct.pack(INFO_FORMAT,os.path.basename(filename),os.stat(filename).st_size,dstlocal)
    sendSock.send(fhead)
    fp = open(filename,'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        if not filedata: break
        sendSock.send(filedata)

    fp.close()
    sendSock.close()
    print "<<<<"


def main():                         
    USAGE="send -f <file> -t <ip:local>  "
    optP=OptionParser(USAGE)
    optP.add_option("-f","--file",action="store",type="string",dest="file",default="",\
                    help="point the file to send")
    optP.add_option("-t","--ipLocal",action="store",type="string",dest="ipLocal",default="",\
                    help="to : ip:local ,such as 192.168.0.108:/home/xxx/tmp/")
    options,ags=optP.parse_args(sys.argv[1:])
    if options.file!='' and options.ipLocal!='':
        send(filename=options.file,ip=options.ipLocal.split(":")[0],
             dstlocal=options.ipLocal.split(":")[1])
    else :
        print "Use addlog -h to show detail usage"


if __name__=="__main__":
    main()
