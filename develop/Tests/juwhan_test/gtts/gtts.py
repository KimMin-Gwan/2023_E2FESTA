from gtts import gTTS

import pygame

tts=gTTS(text="안녕하세요",lang='ko')
tts.save('test2_ko.mp3')

pygame.init()

pygame.mixer.music.load('test2_ko.mp3')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)