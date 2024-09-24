import pygame
from pygame import gfxdraw
import sys
import math
import time
import replaydecoder

class HitCircle:
    def __init__(self, screen, x, y, offset, ar, factorX, factorY):
        print("circle",x,y,ar)
        self.screen = screen
        self.x = float(x) * factorX
        self.y = float(y) * factorY
        self.offset = offset
        self.ar = ar
        
    def update(self):
       print("updating circle")
       self.draw()

    def draw(self):
        print("drawing circle")
        circlePos = pygame.Vector2(self.x, self.y)
        pygame.draw.circle(self.screen,(105,105,105),circlePos,40)

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

    selectedReplay = 'siembra.osr'
    selectedBeatmap = 'saygoodbye.osu'
    replay, replayFrames = replaydecoder.initiateReplayAnalysis(selectedReplay)
    beatmap, hitobjects = replaydecoder.initiateBeatmapAnalysis(selectedBeatmap)

    frameIndex = 0
    frameTotal = len(replayFrames) - 2
    ms = 0

    autoPlay = False
    speedMultiplier = 1
    tickSpeed = 60

    if "DT" in replay["mods"]:
        print("is dt")
        speedMultiplier = 2/3
        tickSpeed = 60

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Courier New', 20)
    pygame.display.set_caption('osu replay analyzer python (concept test)')
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    objectList = []
    cursor = Cursor(screen, factorX, factorY)

    for object in hitobjects:
        objectList.append(HitCircle(screen, int(object[0]), int(object[1]), int(object[3]), float(beatmap["ar"]), factorX, factorY))

    while True:
        screen.fill("black")

        frameData = replayFrames[frameIndex]
        #print(frameIndex, frameData)
        x = frameData[1]
        y = frameData[2]

        keys = pygame.key.get_pressed()

        textSurface = font.render(f"Time (ms): {ms}| AutoPlay: {autoPlay} | Frame {frameIndex} out of {frameTotal} ", False, (255, 255, 255))
        textSurface2 = font.render(f"Frame Data: {frameIndex, frameData}", False, (255, 255, 255))

        screen.blit(textSurface, (0,0))
        screen.blit(textSurface2, (0,HEIGHT-30))

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
                ms+=1
            if keys[pygame.K_DOWN]:
                if ms > 0:
                    ms-=1

        if autoPlay:
            #pygame.time.delay(1)
            ms+=1
        

        pygame.display.update()
        clock.tick(60)

main()