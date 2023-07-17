"""
* Project : 2023CDP main
* Program Purpose and Features :
* - Recognize User Button input
* Author : JH KIM
* First Write Date : 2023.07.10
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.17		v1.00		First Write
"""
from develop.modules.button import *

class information:
    def __init__(self):
        self.__buttonState = -1

    def setButtonState(self, state):
        self.__buttonState = state

def main():
    info = information()
    button = Button(info)
    button.info.setButtonState(1)

if __name__ == "__main__":
    main()