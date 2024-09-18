import pygame
import struct
import replaydecoder

printInfo = False

selectedReplay = 'std.osr'

replayInfo = replaydecoder.readReplay(selectedReplay)

if printInfo:
    for detail in replayInfo:
        if detail != "replay":
            print(detail, ":", replayInfo.get(detail))

#print(replayInfo.get("replay"))

replayData = replayInfo.get("replay")
byteList = []
countDict = {}


for byte in replayData:

    byteList.append(byte)

    if str(byte) in countDict.keys():
        countDict[str(byte)] = int(countDict.get(str(byte))) + 1
    elif str(byte) not in countDict:
        countDict[str(byte)] = 1

compareList = []

for byte in byteList:
    print(byte)