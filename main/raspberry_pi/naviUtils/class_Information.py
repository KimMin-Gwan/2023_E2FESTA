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
* MG KIM            2023.08.22		v1.10		Change Details
"""
import threading

# button state has four different state
# buttonState | -1   |  Default
# buttonState |  1   |  Infra Search Call
# buttonState |  2   |  Okay Call or Stop(No) Call
# buttonState |  3   |  Text Recognition Call
# buttonState |  4   |  Snap Shot(Hand Cam) Call

class Information:
    def __init__(self):
        self.__buttonState = -1  # Default Button State : -1
        self.cs = threading.Lock()
        self.__systemState = 0
        self.now_thread = []

    def getButtonState(self):  # Button state accessor
        return self.__buttonState

    def setButtonState(self, state):  # Button state mutator
        self.cs.acquire()
        print("SYSTEM ALARM::Button State Changed({} -> {})".format(self.getButtonState(), state))
        self.__buttonState = state
        self.cs.release()
        return

    # Get System state
    def getSystemState(self):  # System state accessor
        return self.__systemState

    # Set System state
    def setSystemState(self, newSysState):  # System state mutator
        print("SYSTEM ALARM::System State Changed({} -> {})".format(self.getSystemState(), newSysState))
        self.__systemState = newSysState
        return

    # Add Thread in thread list
    def add_thread(self, thread_purpose):
        print(f"SYSTEM ALARM::{thread_purpose} appended in thread list")
        self.now_thread.append(thread_purpose)
        return
    
    # Therminate Thread list
    def therminate_thread(self, thread_purpose):
        print(f"SYSTEM ALARM::{thread_purpose} thread terminated")
        if thread_purpose in self.now_thread:
            self.now_thread.remove(thread_purpose)
        else:
            print("Information System Error")
            assert("ERROR TYPE : Thread Could not Found")
        return






