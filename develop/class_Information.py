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
        self.systemState = -1

    def getButtonState(self):
        return self.__buttonState

    def setButtonState(self, state):
        self.cs.acquire()
        self.__buttonState = state
        print("Button setting : {}".format(self.getButtonState()))
        self.cs.release()

    def getSystemState(self):
        return self.systemState

    def setSystemState(self, newSysState):
        self.systemState = newSysState
