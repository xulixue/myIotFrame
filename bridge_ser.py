#! /usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import threading
import time;

'''
注意：这里数据的帧头设置为5位字符，需要改进。

判断是移动端设备访问的时候，
    将数据记录到中间变量，所有的Iot设备可以收到，相当于广播。
    第一步：是要筛选一下数据，将那些超时的id数据包删除，下线。   
    第二步：将所有的转发数据包下载了。                       //这里执行之后是否要删除所有的数据包呢？ 这样确定可以看设备是否在线？ 还是不得了，还有其他设备访问呢，每次操作之后再刷新读取一次目标状态就可以了。
判断是Iot设备数据的时候：
    第一步判断是否有这个ID，有更新，没有的话添加。
    
要做的，每天的0点执行一次数据的筛选，超时的id要删除，id下线，目的是如果移动端总是不访问，而设备总是添加就会太大了。
'''
class DistriData:
    timestamp=0.
    data=""
    head=""
    def __init__(self,x,y,z):
        self.timestamp=x
        self.data=y
        self.head = z
devices =[]
m=DistriData(1.0,"x0","head1")
devices.append(m)
m=DistriData(1.0,"x1","head2")
devices.append(m)
#devices.remove()

print devices[0].data
print len(devices)

str_redit = ' ';
str_A = ''
strRemoteDeviBroadcast = ' ';

def ManageDivice(strRev):
    isNewData = True;                       #先假设是新的数据
    if len(strRev) >= 5:
        head = strRev[0:5]
        # print head
        for i in range(len(devices)):
            if devices[i].head == head:         #已经有了更新时间戳，并且更新数据赋值。
                devices[i].timestamp = time.time();
                devices[i].data = strRev[5:];
                isNewData = False;          #不是新的数据
                break;

        if isNewData:                       #如果是新的数据则添加数据。
            m = DistriData(time.time(), strRev[5:], head)
            devices.append(m)

timeOutCleanThreash = 5.0;              # Units is seconds
def CleanOutDatas():
    for i in range(len(devices)):
        if time.time() - devices[i].timestamp > timeOutCleanThreash:
            del devices[i];

# ManageDivice("head2xxxx")
# for i in range(len(devices)):
#     print devices[i].head, devices[i].data, devices[i].timestamp;

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
        global str_redit, str_A, strRemoteDeviBroadcast;
        size = 1024
        while True:
            try:
                data = client.recv(size)
                print "secndLen: ", len(data)
                if len(data) > 5:
                    isIot = False;
                    for i in range(5):
                        if(data[i] != chr(65+i)):
                            # print data[i],' is not equal', chr(65+i), ' , so this is from A'
                            isIot = True;

                    if isIot:
                        print 'is Iot devices.'
                        ManageDivice(data)          #更新或者添加
                        # str_A = data;
                        # print str_A
                        str_redit = strRemoteDeviBroadcast;         #Iot设备都可以接收到移动端设备发送的广播指令。
                    else:
                        print 'is like a phone.'
                        CleanOutDatas();
                        strRemoteDeviBroadcast = data;
                        print strRemoteDeviBroadcast
                        for i in range(len(devices)):               #移动设备一次读取所有Iot设备数据。
                            str_redit += devices[i].head + devices[i].data + "\n";
                            print devices[i].head, devices[i].data, devices[i].timestamp;
                    if len(str_redit) > 0:
                        client.send(str_redit)
                        str_redit = ''          #这里清除下。
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
