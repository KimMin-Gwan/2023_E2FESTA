# TextRecognizer.py
"""
* Program Purpose and Features :
* - TextRecognizer with OCR system(made from NAVER CLOVA)
* Author : HL YANG, SJ YANG, SH PARK, MG KIM
* First Write Date : 2023.08.06
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* HL YANG			2023.08.06      v0.10	    making TextRecognizer.py
* HL YANG			2023.08.07      v0.20	    OCR 파트 삽입
* SH PARK           2023.08.07      v0.21	    OCR 파트 삽입
* MG KIM			2023.08.08      v0.30	    시스템 개편 및 설계
* SJ YANG			2023.08.09      v0.40	    ocr 파트 개선 및 메서드로 설계
* HL YANG			2023.08.13      v0.50	    Making RunRecognition()
"""

from runpy import run_module
from TextRecognition.constant import *
from TextRecognition import Dectector
from Easy_ocr import Easy_ocr
# from Easy_ocr
# from EASY_OCR.Easy_ocr import easy_ocr

# from Camera.camera_master import *
# from Speaker.speaker_master import *
# import Camera
# import Speaker

class TxtRecognizer():
   def __init__(self, info, camera, speaker = None):
      self.info = info  # 버튼
      self.camera = camera
      self.speaker = speaker
      self.detector = Dectector()  # 검출기 (Text-recognition 결과로 나온 단어)
      self.e_ocr = Easy_ocr()  # 인식기 (사진 내의 여러 줄의 텍스트를 인식하고 list로 반환)

   def __call__(self):
        pass

   def RunRecognition(self):
      # inport camera module 
       #    <- handcam&webcam 관련 함수 제작했다고 가정
       # 함수 안에서 웹캠을 돌리다가 핸드카메라 전환. while문하면 안걸린다? if-while문
      
      self.camera.swap_camera()
      
      while True:
         
         cam_button = self.info.getButtonState()
      
         if cam_button == 4:
            photo_frame = self.camera.get_frame()               # hand cam 버튼이 눌렸을 때 사진 찍어 변수에 저장
            
            break
      
      photo_texts = self.e_ocr.run_easyocr_module(photo_frame)  # 사진을 넘겨 사진 속 글자 list 내에 넣어 반환
      text_result = self.detector.run_module(photo_texts)       # 리스트 내의 글자 인식하여 string 결과로 반환
      self.speaker.tts_read(text_result)                         # string 형태로 받아온 글자 speaker로 읽어주기
         
        
        
        """
        1. 카메라 바꾸기
           버튼을 누르면 카메라를 바꿔주는 함수
           ㄴ 만들기 어디에 만들지 camera_master.py에 만들어
           그롬 그 함수 실행해
           그러며 ㄴ camera_master.py 안에 있는 def starthandcam()
           안에서 if 버튼ㄴ 눌렀을 때 카메라 바꾸는 코드를 지우고 함수를 때려박어 어딘지 찾아서/.
        2. 카메라로 사진 찍기
        2.5 ; 사진 하나에 여러 문장이 있을 때 인식 불가능 > easy_ocr 사용하여 글자 프레임 인식 후 넘겨주기
        3. 프레임 배열 넘겨서 처리하기 > text string 형태의 결과로 나옴
        result = self.detector.demo(frame)
        4. 결과로 나온 string 전체를 스피커로 출력하기
           - 들려주다가 버튼을 누르면 끊기 / 다시 듣기
        """
    
#################################################################################################################################################

"""
0. 카메라를 실행하는 건 main 문에서 하는 건가? monitor_test_main.py의 camera.RunCamera()처럼?
   그럼 이 .py 안에다 안 만들어도 되는 거 아닌가?
   
(카메라를 실행하고 웹에서 전환 버튼을 눌렀을 때 카메라 전환되는 것까지 타 파일에서 완성되어있다고 했을 때)
1. 카메라 내에서 실행 중인 상태에서 촬영 버튼을 눌렀을 때 get_frame()으로 프레임 넘겨받기
2. 넘겨받은 프레임을 easy_ocr()을 통해 사진 내의 여러 문장을 각각의 텍스트로 읽어서 넘겨받기
3. 그 여러 개의 프레임들을 받아 OCR 텍스트 인식 진행하고, 진행한 결과를 받기
4. 받은 결과(string)를 스피커로 읽어줄 수 있게 read_tts()를 사용하여 결과 읽어주기
   ㄴ 들려주다가 버튼을 누르면 끊기 / 다시 듣기  << 기능은 여기서 구현? or 버튼에서 구현?

"""