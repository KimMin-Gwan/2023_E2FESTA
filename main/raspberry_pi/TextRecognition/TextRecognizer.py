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
import requests
from runpy import run_module
from TextRecognition.constant import *
from TextRecognition import *
#from TextRecognition.Easy_ocr import *
from TextRecognition.detector import *
import time
from threading import Thread
# from Easy_ocr
# from EASY_OCR.Easy_ocr import easy_ocr

# from Camera.camera_master import *
# from Speaker.speaker_master import *
# import Camera
# import Speaker

class TxtRecognizer():
   def __init__(self, camera, speaker = None, info = None):
      self.info = info  # inforamation with button state
      self.camera = camera
      self.speaker = speaker
      self.detector = Detector()  # 검출기 (Text-recognition 결과로 나온 단어)
      #self.e_ocr = Easy_ocr()  # 인식기 (사진 내의 여러 줄의 텍스트를 인식하고 list로 반환)
      self.url = "http://" + self.info.get_IP() + ":" + self.info.get_PORT() +"/easy_ocr"
      
   def __call__(self):
        pass
   
   # Run Recognition
   def runRecognition(self):
      self.info.add_system("textRecognizer")
      self.info.add_thread("textRecognizer")
      thread = Thread(target=self.__textRecognition)
      thread.start()
      return
   
   def _terminate(self):
      self.info.remove_system("textRecognizer")
      self.info.terminate_thread("textRecognizer")
      return

      
   # text recognition syste
   def __textRecognition(self):
      # inport camera module 
       #    <- handcam&webcam 관련 함수 제작했다고 가정
       # 함수 안에서 웹캠을 돌리다가 핸드카메라 전환. while문하면 안걸린다? if-while문
      
      self.camera.swap_camera()
      time.sleep(0.5)
      #count = 0
      while True:
         cam_button = self.info.getButtonState()
      
         if cam_button == SYS_STATE_HANDCAM:
            photo_frame = self.camera.get_frame()               # hand cam 버튼이 눌렸을 때 사진 찍어 변수에 저장
            break

         if self.info.get_terminate_flag():
            self._terminate()
            return
         """
         time.sleep(1)
         count += 1
         print('pick count :',count)
         if count == 5:
            photo_frame = self.camera.get_frame()               # hand cam 버튼이 눌렸을 때 사진 찍어 변수에 저장
            print("check")
            break
         """

      #print('type : ', type(photo_frame))
      print("SYSTEM ALARM::SNAP SHOT BUTTON ACTIVATE")
      data = {'frame':photo_frame.tolist()}
      try:
         return_data = requests.post(self.url, json = data)
         #photo_texts = self.e_ocr.run_easyocr_module(photo_frame)  # 사진을 넘겨 사진 속 글자 list 내에 넣어 반환
         photo_texts = return_data.json()['frame']
         for i in range(len(photo_texts)):
             photo_texts[i]=Image.fromarray(np.uint8(photo_texts[i]))
             photo_texts[i]=photo_texts[i].convert("RGBA")   
         if self.info.get_terminate_flag():
            self._terminate()
            return
      except Exception as e:
         print("ERROR : Server Error")
         print("ERROR CODE : ", e)
         self.info.terminate_thread("TextRecognizer")
         assert("SYSTEM CALL::Stop Text Recognition")
      for i in range(len(photo_texts)):
          photo_texts[i]=photo_texts[i].convert('L')

      text_result = self.detector.run_module(photo_texts)       # 리스트 내의 글자 인식하여 string 결과로 반환
      for i in range(len(text_result)):
         if self.info.get_terminate_flag():
            self._terminate()
            return
      #   photo_texts[i] = Image.fromarray(np.uint8(photo_texts[i])).convert('L')
      print("=========================================")
      #print(type(photo_texts[0]))

      if self.info.get_terminate_flag():
         self._terminate()
         return

      for arg in text_result:
         self.speaker.tts_read(arg)                             # string 형태로 받아온 글자 speaker로 읽어주기
      print("SYSTEM ALARM:: text recognition is operating completly ")
      self.camera.swap_camera()
      self.info.remove_system("textRecognizer")
      self.info.terminate_thread("textRecognizer")
