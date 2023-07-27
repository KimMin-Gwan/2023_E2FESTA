# server_send.py
"""
* Program Purpose and Features :
* - for Running Client 
* - This file will run in rasberryPI
* Author : Juwhan Kim
* First WriJuwhante Date : 2023.07.16
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* Juwhan KIM			2023.07.16      v0.10	    make file
* 
"""

#url 을 전송하는 방법

import requests

def send():
    url = 'http://43.201.213.223:8080/rcv?id=ID&id=SUB&id=1'
    response = requests.get(url)
    
send()