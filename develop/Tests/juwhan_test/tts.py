from gtts import gTTS
from playsound import playsound

comment="안녕하세요"

comment_to_voice=gTTS(text=comment,lang="ko")
comment_to_voice.save("test_ko.mp3")



playsound("test_ko.mp3")