import pygame
from pygame import gfxdraw
import sys
import math
import time
import osureader

class HitCircle:
    def __init__(self, screen, x, y, ms, ar, factorX, factorY, canvasX, canvasY):
        #print("circle",x,y,ar)
        self.screen = screen
        self.x = float(x) * factorX + canvasX
        self.y = float(y) * factorY + canvasY

        self.createdMS = ms
        self.currentMS = 0
        self.ar = 1200 - (750*(ar - 5)/5)

        self.factorX = factorX
        self.factorY = factorY
        self.canvasX = canvasX
        self.canvasY = canvasY

        #print(self.ar)
        
    def update(self, ms):
       #print("updating circle")
       self.currentMS = ms
       diff = self.createdMS - self.currentMS
       if diff < self.ar and self.createdMS >= self.currentMS:
            self.draw()

    def draw(self):
        #print("h")
        diff = self.createdMS - self.currentMS
        R,G,B = 255*((self.ar-diff)/self.ar),255*((self.ar-diff)/self.ar),255*((self.ar-diff)/self.ar)
        circlePos = pygame.Vector2(self.x, self.y)
        arSize = 300-(((self.ar-diff)/self.ar)*300)
        pygame.draw.circle(self.screen,(255,255,255),circlePos, arSize, 5)
        pygame.draw.circle(self.screen,(R,G,B),circlePos,60)

class Cursor:
    def __init__(self, screen, factorX, factorY, canvasX,canvasY):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.factorX = factorX
        self.factorY = factorY
        self.canvasX = canvasX
        self.canvasY = canvasY

    def update(self, x, y):
        self.x = float(x) * self.factorX + self.canvasX
        self.y = float(y) * self.factorY + self.canvasY
        self.draw()

    def draw(self):
        cursorPos = pygame.Vector2(self.x, self.y)
        pygame.draw.circle(self.screen,"yellow",cursorPos,15)

def display(sentReplay,sentBeatmap):

    osuX, osuY = 512, 384
    WIDTH, HEIGHT = 1280, 720

    canvasHeight = HEIGHT * .8
    canvasWidth = canvasHeight * (4/3)
    canvasX = (WIDTH-canvasWidth)/2
    canvasY = (HEIGHT-canvasHeight)/2
    factorX, factorY = canvasWidth/512, canvasHeight/384

    selectedReplay = sentReplay
    selectedBeatmap = sentBeatmap
    replay, frames = osureader.compileFrames(selectedReplay, selectedBeatmap)

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
    cursor = Cursor(screen, factorX, factorY, canvasX, canvasY)

    for i, frame in enumerate(frames):
        if frame[0] is not None and len(frame[0]) == 2:
            if frame[0][1] is not None:
                cx,cy = frame[0][1][0],frame[0][1][1]
                if cx != 0 and cy != 0:
                    circle = HitCircle(screen,cx,cy,i,10,factorX,factorY,canvasX,canvasY)
                    objectList.append(circle)
    
    #center = pygame.Vector2(WIDTH/2, HEIGHT/2)

    x,y = 0,0
    cx,cy = 0,0

    while True:
        circle = False
        cx,cy = 0,0
        screen.fill("black")

        canvas = pygame.Rect(canvasX, canvasY, canvasWidth, canvasHeight)
        pygame.draw.rect(screen, (105,105,105), canvas, 5)
        
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
            
            #if frame[0][1] is not None:
                #cx,cy = frame[0][1][0],frame[0][1][1]

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

        '''
        if cx != 0 and cy != 0:
            #print("new circle")
            currentCircle = HitCircle(screen,cx,cy,ms,10,factorX,factorY,canvasX,canvasY)
            objectList.append(currentCircle)
        '''

        for object in objectList:
            object.update(ms)
        
        cursor.update(x,y)

        #pygame.gfxdraw.aacircle(screen, x, y, 15, (255,0,0))
        #pygame.gfxdraw.filled_circle(screen, x, y, 15, (255,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
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
                for object in objectList:
                    canvasHeight = HEIGHT * .8
                    canvasWidth = canvasHeight * (4/3)
                    canvasX = (WIDTH-canvasWidth)/2
                    canvasY = (HEIGHT-canvasHeight)/2
                    factorX, factorY = canvasWidth/512, canvasHeight/384
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