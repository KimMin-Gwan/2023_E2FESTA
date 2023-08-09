from TextRecognition.constant import *
from TextRecognition import Dectector


class TxtRecognizer():
    def __init__(self, camera, speaker = None):
        self.camera = camera
        self.speakr = speaker
        detector = Dectector()  # 검출기 (Text-recognition 결과로 나온 단어)

    def __call__(self):
        pass

    def RunRecognition(self):
        # inport camera module 
        #    <- handcam&webcam 관련 함수 제작했다고 가정
        # 함수 안에서 웹캠을 돌리다가 핸드카메라 전환. while문하면 안걸린다? if-while문
        
        """
        1. 카메라 바꾸기
           버튼을 누르면 카메라를 바꿔주는 함수
           ㄴ 만들기 어디에 만들지 camera_master.py에 만들어
           그롬 그 함수 실행해
           그러며 ㄴ camera_master.py 안에 있는 def starthandcam()
           안에서 if 버튼ㄴ 눌렀을 때 카메라 바꾸는 코드를 지우고 함수를 때려박어 어딘지 찾아서/.
        2. 카메라로 사진 찍기
        
        3. 프레임 배열 넘겨서 처리하기 > text string 형태의 결과로 나옴
        result = self.detector.demo(frame)
        4. 결과로 나온 string 전체를 스피커로 출력하기
           - 들려주다가 버튼을 누르면 끊기 / 다시 듣기
        """
    
#################################################################################################################################################