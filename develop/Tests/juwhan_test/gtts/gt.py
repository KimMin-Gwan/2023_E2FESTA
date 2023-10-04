from gtts import gTTS

import pygame

tts=gTTS(text="경산우체국 방향 신호등입니다. 현재 빨간색이고 15초 남았습니다.", lang='ko')
tts.save('huhu.mp3')

pygame.init()

pygame.mixer.music.load('huhu.mp3')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)