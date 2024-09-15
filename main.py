import pygame
import replaydecoder

selectedReplay = 'std.osr'

replayInfo = replaydecoder.readReplay(selectedReplay)

for detail in replayInfo:
    if detail != "replay":
        print(detail, ":", replayInfo.get(detail))

print(replayInfo.get("replay"))