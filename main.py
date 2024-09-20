import pygame
import sys
import math
import time
import replaydecoder

printInfo = False

selectedReplay = 'paula.osr'

frames = replaydecoder.initiateReplayAnalysis(selectedReplay)

'''
pygame.init()
screen = pygame.display.set_mode((512, 385))
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
    clock.tick(60)
'''

#print(frames)

WIDTH, HEIGHT = 1280, 720
factorX, factorY = WIDTH/512, HEIGHT/384

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
pygame.display.set_caption('osu replay analyzer python (concept test)')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

totalTime = 0

for index, frame in enumerate(frames):

    if int(frame[0]) >= 0:
        textSurface = font.render(f"Frame {index} out of {len(frames)} | Time Elapsed (ms): {totalTime}", False, (0, 0, 0))

        screen.fill("white")
        cursorPos = pygame.Vector2(float(frame[1])*factorX, float(frame[2])*factorY)
        screen.blit(textSurface, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.draw.circle(screen, "red", cursorPos, 15)

        pygame.display.update()
        #time.sleep(abs(int(frame[0])/1000))
        #pygame.time.delay(int(frame[0]))
        #pygame.time.delay(1)
        #time.sleep(.25)

        totalTime += int(frame[0])
        clock.tick(60)