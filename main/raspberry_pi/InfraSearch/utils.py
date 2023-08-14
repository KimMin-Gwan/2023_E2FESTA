#utils.py
"""
* Program Purpose and Features :
* - utility function and global variable
* Author : JH KIM, JH SUN, MG KIM
* First Write Date : 2023.07.11
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* MG KIM			2023.07.11      v0.10	    make from /juwhan_test/split_class.py 
"""

import threading

from queue import PriorityQueue
from bluepy.btle import Scanner
from modules.InfraSearch.scannrecive import ScanDelegate

lock=threading.Lock()
que=PriorityQueue()




duration=2
scan_delegate=ScanDelegate()
scanner=Scanner().withDelegate(scan_delegate)

