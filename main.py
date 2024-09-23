import pygame
from pygame import gfxdraw
import sys
import math
import time

import pygame.gfxdraw
import replaydecoder

class HitCircle:
    def __init__(self, x, y, ar):
        print("cursor",x,y,ar)
        
    def update(self):
       print("updating circle")

    def draw(self):
        print("drawing circle")

class Cursor:
    def __init__(self, x, y):
        print("init cursor",x,y)

    def update(self, x, y):
        print("updating cursor")
        self.draw()

    def draw(self, x, y):
        print("drawing cursor")
        pygame.Vector2(float(x)*factorX, float(y)*factorY)

def main():

    WIDTH, HEIGHT = 1280, 720
    factorX, factorY = WIDTH/512, HEIGHT/384

    selectedReplay = 'stdplus.osr'
    frames = replaydecoder.initiateReplayAnalysis(selectedReplay)

    frameIndex = 0
    frameTotal = len(frames) - 2

    autoPlay = False

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 20)
    pygame.display.set_caption('osu replay analyzer python (concept test)')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        screen.fill("black")

        frameData = frames[frameIndex]
        print(frameIndex, frameData)

        x = float(frameData[1])*factorX
        y = float(frameData[2])*factorY
        timeMS = int(frameData[0])

        cursorPos = pygame.Vector2(x,y)

        keys = pygame.key.get_pressed()

        textSurface = font.render(f"Frame {frameIndex} out of {frameTotal} | AutoPlay: {autoPlay}", False, (255, 255, 255))

        screen.blit(textSurface, (0,0))

        pygame.draw.circle(screen,"yellow",cursorPos,15)

        #pygame.gfxdraw.aacircle(screen, x, y, 15, (255,0,0))
        #pygame.gfxdraw.filled_circle(screen, x, y, 15, (255,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not autoPlay:
                    if event.key == pygame.K_a:
                        if frameIndex > 0:
                            frameIndex -= 1
                    if event.key == pygame.K_d:
                        if frameIndex < frameTotal:
                            frameIndex += 1
                if event.key == pygame.K_SPACE:
                    if not autoPlay:
                        autoPlay = True
                    elif autoPlay:
                        autoPlay = False

        if autoPlay:
            pygame.time.delay(timeMS)
            frameIndex+=1
        

        pygame.display.update()
        clock.tick(60)

main()

#print(frames)

'''
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
        pygame.time.delay(int(frame[0]))
        #pygame.time.delay(1)
        #time.sleep(.25)

        totalTime += int(frame[0])
        clock.tick(60)
'''