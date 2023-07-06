from gtts import gTTS
from playsound import playsound

comment="안녕 하세요 저는 선주환입니다."
comment_to_voice=gTTS(text=comment,lang="ko")
comment_to_voice.save("test_ko_mp3")

comment_to_voice=gTTS(text=comment,lang="en")
comment_to_voice.save("test_en_mp3")
