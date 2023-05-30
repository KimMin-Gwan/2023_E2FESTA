from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)
	
	def handleDiscovery(self,dev,isNewDev,isNewData):
		if isNewDev:
			print('Discovered device',dev.addr)
		elif isNewData:
			print('Recevied new data from',dev.addr)


scanner=Scanner().withDelegate(ScanDelegate())
devices=scanner.scan(10.0)


for dev in devices:
	print('Device %s (%s), RSSI= %d db' %(dev.addr,dev.addrType,dev.rssi))
	for (adtype,desc,value) in dev.getScanData():
		print('   %s = %s'%(desc,value))



	for dev in devices:
		print('Device %s (%s), RSSI= %d db' %(dev.addr,dev.addrType,dev.rssi))
		for adv_data in dev.getScanData():
			print('Recevied Data {}'.format(adv_data))
		print()
