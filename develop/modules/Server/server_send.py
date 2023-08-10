# server_send.py
"""
* Program Purpose and Features :
* - for Running Client 
* - This file will run in rasberryPI
* Author : JW KIM, SH PARK
* First WriJuwhante Date : 2023.07.17
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* SH PARK   		2023.07.17      v0.10	    make send system
* JW KIM	        2023.07.20      v0.20       change send method
* SH PARK           2023.07.20      v0.30       change IP of url
* 
"""

#url 을 전송하는 방법

import requests

def send():
    url = 'http://43.201.213.223:8080/rcv?id=ID&id=SUB&id=1'
    response = requests.get(url)
    
send()