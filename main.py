import pygame
import struct
import lzma
import replaydecoder

printInfo = False

decompressor = lzma.LZMADecompressor()

selectedReplay = 'stdold.osr'

stuff = replaydecoder.initiateReplayAnalysis(selectedReplay)

#print(stuff)
print(type(stuff))
