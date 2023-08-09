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
from develop.constant import *
import threading
class information:
    def __init__(self):
        self.__buttonState = -1
        self.cs = threading.Lock()
        self.systemState = 0

    def getButtonState(self):
        return self.__buttonState

    def setButtonState(self, state):
        self.cs.acquire()
        print("SYSTEM ALARM::Button State Changed({} -> {})".format(self.getButtonState(), state))
        self.__buttonState = state
        self.cs.release()

    def getSystemState(self):
        return self.systemState

    def setSystemState(self, newSysState):
        print("SYSTEM ALARM::System State Changed({} -> {})".format(self.getSystemState(), newSysState))
        self.systemState = newSysState

