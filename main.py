import pygame
from pygame import gfxdraw
import sys
import math
import time
import replaydecoder

class HitCircle:
    def __init__(self, screen, x, y, ms, ar, factorX, factorY):
        #print("circle",x,y,ar)
        self.screen = screen
        self.x = float(x) * factorX
        self.y = float(y) * factorY
        self.createdMS = ms
        self.currentMS = ms
        self.ar = 1200 - (750*(ar - 5)/5)
        print(self.ar)
        
    def update(self, ms):
       #print("updating circle")
       self.currentMS = ms
       if self.currentMS - self.createdMS < self.ar-1:
           self.draw()

    def draw(self):
        #print("drawing circle")
        circlePos = pygame.Vector2(self.x, self.y)
        pygame.draw.circle(self.screen,(105,105,105),circlePos,60)

class Cursor:
    def __init__(self, screen, factorX, factorY):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.factorX = factorX
        self.factorY = factorY

    def update(self, x, y):
        self.x = float(x) * self.factorX
        self.y = float(y) * self.factorY
        self.draw()

    def draw(self):
        cursorPos = pygame.Vector2(self.x, self.y)
        pygame.draw.circle(self.screen,"yellow",cursorPos,15)

def main():

    WIDTH, HEIGHT = 1280, 720
    factorX, factorY = WIDTH/512, HEIGHT/384

    selectedReplay = 'wifeline.osr'
    selectedBeatmap = 'saygoodbye.osu'
    replay, frames = replaydecoder.compileFrames(selectedReplay, selectedBeatmap)

    frameTotal = len(frames)
    ms = 0

    autoPlay = False
    speedMultiplier = 1
    tickSpeed = 1000

    if "DT" in replay["mods"]:
        print("is dt")
        speedMultiplier = 2/3
        tickSpeed = 1000

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Courier New', 20)
    pygame.display.set_caption('osu replay analyzer python (concept test)')
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    objectList = []
    cursor = Cursor(screen, factorX, factorY)
    newCircle = False

    x,y = 0,0
    cx,cy = 0,0

    while True:
        circle = False
        cx,cy = 0,0
        screen.fill("black")
        
        frame = frames[ms]
        #print(frame)
        #print(len(frame[0]))
        #print(frame[0][1][0])
        #print(frame[0][1][1])

        if frame[0] is not None and len(frame[0]) == 2:
            #print("1")
            if frame[0][0] is not None:
                x = frame[0][0][1]
                y = frame[0][0][2]
            
            if frame[0][1] is not None:
                newCircle = True
                cx,cy = frame[0][1][0],frame[0][1][1]
                #print(frame[0][1][0],frame[0][1][1])

        elif frame[0] is not None and len(frame[0]) == 4:
            #print("2")
            x = frame[0][1]
            y = frame[0][2]
            #print(x,y)
            
        keys = pygame.key.get_pressed()

        textSurface = font.render(f"Resolution: {WIDTH} x {HEIGHT}| AutoPlay: {autoPlay}", False, (255, 255, 255))
        textSurface2 = font.render(f"Frame: {frame}", False, (255, 255, 255))
        textSurface3 = font.render(f"Frame Data: {ms, frameTotal}", False, (255, 255, 255))

        screen.blit(textSurface, (0,0))
        screen.blit(textSurface2, (0,20))
        screen.blit(textSurface3, (0,HEIGHT-30))

        if cx != 0 and cy != 0:
            #print("new circle")
            currentCircle = HitCircle(screen,cx,cy,ms,9.3,factorX,factorY)
            objectList.append(currentCircle)

        for object in objectList:
            object.update(ms)

        cursor.update(x,y)

        #pygame.gfxdraw.aacircle(screen, x, y, 15, (255,0,0))
        #pygame.gfxdraw.filled_circle(screen, x, y, 15, (255,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not autoPlay:
                    if event.key == pygame.K_LEFT:
                        if ms > 0:
                            ms-=1
                    if event.key == pygame.K_RIGHT:
                        if ms < frameTotal-1:
                            ms+=1
                if event.key == pygame.K_SPACE:
                    autoPlay = not autoPlay
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                factorX, factorY = WIDTH/512, HEIGHT/384
                cursor.factorX = factorX
                cursor.factorY = factorY

        keys = pygame.key.get_pressed()
        if not autoPlay:
            if keys[pygame.K_UP]:
                if ms < frameTotal-1:
                    ms+=1
            if keys[pygame.K_DOWN]:
                if ms > 0:
                    ms-=1

        if autoPlay:
            #pygame.time.delay(1)
            if ms < frameTotal-1:
                ms+=1
            elif ms == frameTotal-1:
                autoPlay = not autoPlay
        

        pygame.display.update()
        clock.tick(tickSpeed)

main()