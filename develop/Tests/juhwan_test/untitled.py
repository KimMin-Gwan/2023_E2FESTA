#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2023  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
    def __init__(self,iface=0):
        self.__scan_data__={}
        if(DefaultDelegate!=None):
            DefaultDelegate.__init__(self)
    def handleDiscovery(self,dev,isNewDev,isNewData):
        raw=dev.getScanData()
        mac=dev.addr.upper()
        rssi=dev.rssi
        data={}
        data['raw']=raw
        data['mac']=mac
        data['rssi']=rssi
        self.__scan_data__=data

def main():
    scanner=Scanner().withDelegate(ScanDelegate())
    
    devices=scanner.scan(10.0)

    lit=[]
    str_data=''
    for dev in devices:
        print('Devices %s(%s) ,RSSI = %d db' % (dev.addr,dev.addrType,dev.rssi))
        for (adtype,desc,value) in dev.getScanData():
            print(' %s   %s' %(desc,value))
        print()
if __name__ == '__main__':
    main()
