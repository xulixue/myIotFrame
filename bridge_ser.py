#! /usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import threading

str_redit = ' ';
str_A = ' ';
str_B = ' ';

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        global str_redit, str_A, str_B;
        size = 1024
        while True:
            try:
                data = client.recv(size)
                print "secndLen: ", len(data)
                if len(data) > 5:
                    isA = False;
                    for i in range(5):
                        if(data[i] != chr(65+i)):
                            print data[i],' is not equal', chr(65+i), ' , so this is from A'
                            isA = True;

                    if isA:
                        str_A = data;
                        print str_A
                        str_redit = str_B;
                    else:
                        str_B = data;
                        print str_B
                        str_redit = str_A;
                    if len(str_redit) > 0:
                        client.send(str_redit)
                else:
                    raise error('Client disconnected or Reved short than 5 chars')
            except:
                client.close()
                return False

if __name__ == "__main__":
    while True:
        port_num = 14578
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('',port_num).listen()
