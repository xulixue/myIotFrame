#! /usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys,time
import socket

def doConnect(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        sock.connect((host,port))
    except :
        pass
    return sock

def main():
#    host,port = "IP",14578
    host,port = "127.0.0.1",14578
    print host,port
    sockLocal = doConnect(host,port)

    while True :
        try :
            msg = "$~A01" + str(time.time())     # head cat data;
            sockLocal.send(msg)
            print "send msg ok : ",msg
            print "recv data :",sockLocal.recv(1024)
        except socket.error :
            print "\r\nsocket error,do reconnect "
            time.sleep(3)
            sockLocal = doConnect(host,port)
        except :
            print '\r\nother error occur '
            time.sleep(3)
        time.sleep(1)

if __name__ == "__main__" :
    main()
