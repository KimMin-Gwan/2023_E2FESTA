"""
* Project : 2023CDP - information class constant
* Program Purpose and Features :
* - constant
* Author : JH KIM
* First Write Date : 2023.08.09
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* JH KIM			2023.08.09      v0.10	    first write
"""

SYS_STATE_DEFAULT = 0
SYS_STATE_INFRA = 1
SYS_STATE_HANDCAM = 3
# ocr을 위한 서버주소
#SERVER_IP = '43.201.213.223'
#SERVER_IP = '165.229.185.195'
#SERVER_IP = '192.168.50.51'
#SERVER_IP='192.168.50.47'
#SERVER_IP='172.20.10.7'  #혜림
SERVER_IP='192.168.234.157'  #easyocr 민관이꺼
#SERVER_IP='192.168.50.121'    #이 ip를 통해서 재현이 컴퓨터에서 서버를 열어야함 easy ocr과 비콘 데이터베이스 연결

SERVER_PORT = '8888'
UDP_PORT =8081 