from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
	def __init__(self,iface=0):
		self.__scan_data__={}
		if(DefaultDelegate !=None):
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
	devices=scanner.scan(5.0)  #scan duration 5second
	lit=[]
	str_data=''
	for dev in devices:   #devices find one of dev
		print('Device %s (%s), RSSI= %d db' %(dev.addr,dev.addrType,dev.rssi))
		for (adtype,desc, value) in dev.getScanData():
			print(' %s = %s' %(desc,value)
                  
                  
                  
                  
if __name__ =='__main__':
    main()