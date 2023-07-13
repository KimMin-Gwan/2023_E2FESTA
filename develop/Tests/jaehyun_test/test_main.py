"""
* Project : 2023CDP Theadind Test of User Button
* Program Purpose and Features :
* - multi threading test user button input
* Author : JH KIM
* First Write Date : 2023.07.13
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.13		v1.00		First Write
"""
from modules.Button import *
import threading
import time

def print_a():
    while True:
        print("a")
        time.sleep(0.1)

def runButton():
    button = Button()
    while True:
        button.buttonInput()

if __name__ == "__main__":
     print_thread = threading.Thread(target=print_a)
     button_thread = threading.Thread(target=runButton)

     print_thread.start()
     button_thread.start()

     print_thread.join()
     button_thread.join()