from gtts import gTTS
import os

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')  # 텍스트와 언어 설정
    tts.save(filename)
    os.system('mpg321 ' + filename)  # 음성 파일 재생

text = input("음성으로 변환할 텍스트를 입력하세요: ")
filename = 'output.mp3'
text_to_speech(text, filename)