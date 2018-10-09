#! /usr/bin/python
# -*- coding: utf-8 -*- #
import os
import time;
from bluepy.btle import Scanner, DefaultDelegate

DEBUG_MI_BAND3 = True

search_times = 0;   #标记总数
lines = 0;

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if not DEBUG_MI_BAND3:
            if isNewDev:
                print ("Discovered device", dev.addr)
            elif isNewData:
                print ("Received new data from", dev.addr)
while(True):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(0.2) # set the timeout 
    for dev in devices:
        if DEBUG_MI_BAND3:
            #search_times = search_times + 1;
            if dev.addr == 'd2:31:83:d4:3c:fe':
                #print ("search times:", lines, ".all times:", search_times, lines = lines+1)
                print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                time.sleep(1)
        else:
            print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print ("  %s = %s" % (desc, value))

