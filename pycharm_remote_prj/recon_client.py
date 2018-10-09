#! /usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys,time
import socket

import ConfigParser

def doConnect(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        sock.connect((host,port))
    except :
        pass
    return sock

def main():
    cf = ConfigParser.ConfigParser()
    cf.read("./db_config.ini")
    host = cf.get("host_cfg", "host")
    port = cf.get("host_cfg", "port")
    print host,port
    sockLocal = doConnect(host,port)

    while True :
        try :
            msg = '''"$~A02"''' + str(time.time())     # head cat data;
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

