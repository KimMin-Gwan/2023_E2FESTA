"""
* Project : 2023CDP User Button constant
* Program Purpose and Features :
* - button package constant
* Author : JH KIM
* First Write Date : 2023.07.17
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.17		v1.00		First Write
* JH KIM            2023.08.14      v1.10       Button 4 Added
"""


# pin number
BEACONSCANBUTTON = 8
YESNOBUTTON = 10
HANDCAMBUTTON = 12
HCAMCAPTUREBUTTON = 16

# state
DEFAULT = -1        # Button Default State
SCAN = 1            # SCAN Start/Stop Button
YES = 2             # Yes Button
NO = -2             # No Button
HANDCAM = 3         # HANDCAM Start Button
HCAMCAPTURE = 4     # HANDCAM Capture Button
