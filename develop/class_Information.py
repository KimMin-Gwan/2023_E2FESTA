"""
* Project : 2023CDP main information class
* Program Purpose and Features :
* - information class
* Author : JH KIM
* First Write Date : 2023.07.17
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.17		v1.00		First Write
"""
import threading
class information:
    def __init__(self):
        self.__buttonState = -1
        self.cs = threading.Lock()

    def setButtonState(self, state):
        self.cs.acquire()
        self.__buttonState = state
        self.cs.release()

    def getButtonState(self):
        return self.__buttonState