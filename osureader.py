import struct
import decoders
import time

byteList = []
modes = ['standard', 'taiko', 'ctb', 'mania']

replayInfo = {
    "mode": "",
    "version": "",
    "bmhash": "",
    "player": "",
    "replayhash": "",
    "perfect": "",
    "meh": "",
    "bad": "",
    "perfectalt": "",
    "mehalt": "",
    "miss": "",
    "score": "",
    "combo": "",
    "fc": "",
    "mods": "",
    "lifebar": "",
    "timestamp": "",
    "length": "",
    "replay": "",
    "id": "",
    "mod+": ""
}

beatmapInfo = {
    "title":"",
    "artist":"",
    "creator":"",
    "diff":"",
    "cs":"",
    "od":"",
    "ar":"",
    "hitobjects":"",
}

mods = {
    "1073741824": "MR",
    "536870912": "SV2",
    "268435456": "Key2",
    "134217728": "Key3",
    "67108864": "Key1",
    "33554432": "Coop",
    "16777216": "Key9",
    "8388608": "TP",
    "4194304": "LastMod/Cinema",
    "2097152": "Random",
    "1048576": "FI",
    "1015808": "KeyMod",
    "524288": "Key8",
    "262144": "Key7",
    "131072": "Key6",
    "65536": "Key5",
    "32768": "Key4",
    "16384": "PF",
    "8192": "AP",
    "4096": "SO",
    "2048": "AT",
    "1024": "FL",
    "512": "NC",
    "256": "HT",
    "128": "RX",
    "64": "DT",
    "32": "SD",
    "16": "HR",
    "8": "HD",
    "4": "TD",
    "2": "EZ",
    "1": "NF",
    "0": "NM"
}

inputs = {
    "1":"M1",
    "2":"M2",
    "4":"K1",
    "8":"K2",
    "16":"Smoke"
}

def whatMods(modId):
    result = ''
    for key in mods.keys():
        if modId >= int(key) and modId > 0:
            modId = modId - int(key)
            result = result + mods.get(key)
    return result

def whatInputs(inputId):
    result = ''
    for key in inputs.keys():
        if inputId >= int(key) and inputId > 0:
            inputId = inputId - int(key)
            result = result + inputs.get(key)
    return result

def readReplay(replayName):

    replay = open(replayName, "rb")
    replayData = replay.read()

    offset = 0

    replayInfo["mode"] = modes[struct.unpack_from('<B', replayData, offset)[0]]
    offset += 1
    replayInfo["version"] = struct.unpack_from("<I", replayData, offset)[0]
    offset += 4
    replayInfo["bmhash"], offset = decoders.readString(replayData, offset)
    replayInfo["player"], offset = decoders.readString(replayData, offset)
    replayInfo["replayhash"], offset = decoders.readString(replayData, offset)
    replayInfo["perfect"] = struct.unpack_from("<H", replayData, offset)[0]
    offset += 2
    replayInfo["meh"] = struct.unpack_from("<H", replayData, offset)[0]
    offset += 2
    replayInfo["bad"] = struct.unpack_from("<H", replayData, offset)[0]
    offset += 2
    replayInfo["perfectalt"] = struct.unpack_from("<H", replayData, offset)[0]
    offset += 2
    replayInfo["mehalt"] = struct.unpack_from("<H", replayData, offset)[0]
    offset += 2
    replayInfo["miss"] = struct.unpack_from("<H", replayData, offset)[0]
    offset += 2
    replayInfo["score"] = struct.unpack_from("<I", replayData, offset)[0]
    offset += 4
    replayInfo["combo"] = struct.unpack_from("<H", replayData, offset)[0]
    offset += 2
    replayInfo["fc"] = struct.unpack_from("<B", replayData, offset)[0]
    offset += 1
    replayInfo["mods"] = whatMods(struct.unpack_from("<I", replayData, offset)[0])
    offset += 4
    replayInfo["lifebar"], offset = decoders.readString(replayData, offset)
    replayInfo["timestamp"] = struct.unpack_from("<L", replayData, offset)[0]
    offset += 8
    replayInfo["length"] = struct.unpack_from("<I", replayData, offset)[0]
    offset += 4
    replayInfo["replay"] = replayData[offset:(offset + replayInfo.get("length"))]
    offset += replayInfo.get("length")
    replayInfo["id"] = struct.unpack_from("<Q", replayData, offset)[0]
    offset += 8
    
    replay.close()

    return replayInfo

def readBeatmap(beatmapName):

    beatmap = open(beatmapName, "r")

    hitObjects = []
    separatorIndex = None

    for index, line in enumerate(beatmap):

        line = line.strip()

        if "Title:" in line:
            beatmapInfo["title"] = line.split(":")[1]
        if "Artist:" in line:
            beatmapInfo["artist"] = line.split(":")[1]
        if "Creator:" in line:
            beatmapInfo["creator"] = line.split(":")[1]
        if "Version:" in line:
            beatmapInfo["diff"] = line.split(":")[1]
        if "CircleSize:" in line:
            beatmapInfo["cs"] = line.split(":")[1]
        if "OverallDifficulty:" in line:
            beatmapInfo["od"] = line.split(":")[1]
        if "ApproachRate:" in line:
            beatmapInfo["ar"] = line.split(":")[1]

        if "[HitObjects]" in line:
            separatorIndex = index
        
        if separatorIndex is not None:
            if index > separatorIndex:
                hitObjects.append(line)

    beatmapInfo["hitobjects"] = hitObjects

    return beatmapInfo


def extractFrames(replayData):
    dataList = []
    frameList = []

    dataList = replayData.split(",")

    for item in dataList:
        frameList.append(tuple(item.split("|")))

    frameList = frameList[3:]
    frameList = frameList[:-1]

    return frameList

def extractHitObjects(hitObjects):
    parsedHitObjects = []

    for hitobject in hitObjects:
        parsedHitObjects.append(tuple(hitobject.split(",")))

    return parsedHitObjects

def initiateReplayAnalysis(replayName):
    replay = readReplay(replayName)
    compressedReplayData = replay["replay"]
    replayData = decoders.decodeLZMA(compressedReplayData)
    frames = extractFrames(replayData)

    del replayInfo["replay"]

    return replayInfo, frames

def initiateBeatmapAnalysis(beatmapName):
    #print(beatmapName)
    beatmap = readBeatmap(beatmapName)
    hitObjects = extractHitObjects(beatmap["hitobjects"])

    return beatmap, hitObjects

def compileFrames(replayName, beatmapName):
   
   frames = []
   indexedReplayFrames = {}
   indexedCircleFrames = {}

   replay, replayFrames = initiateReplayAnalysis(replayName)
   map, circles = initiateBeatmapAnalysis(beatmapName)

   maxFrames = int(circles[-1][2])
   
   offset = 0
   prevFrame = None

   for index, rFrame in enumerate(replayFrames):
      if int(rFrame[0]) > 0:
          offset += int(rFrame[0])
          #print(index, offset, rFrame)
          indexedReplayFrames[offset] = rFrame
      else:
          indexedReplayFrames[offset] = rFrame

   for index, circle in enumerate(circles):
      #print(index, circle[2], circle)
      #indexedCircleFrames[int(circle[2]) - (1200 - (750*(9.3 - 5)/5))] = circle
      indexedCircleFrames[int(circle[2])] = circle
      #time.sleep(.25)

   prevCursor = None

   for i in range(0, maxFrames + 1):
      frame = []
      if i in indexedReplayFrames.keys() and i in indexedCircleFrames.keys():
         frame.append((indexedReplayFrames[i],indexedCircleFrames[i]))
         prevCursor = (indexedReplayFrames[i],indexedCircleFrames[i])
      elif i in indexedReplayFrames.keys():
         frame.append((indexedReplayFrames[i],None))
         prevCursor = (indexedReplayFrames[i])
      elif i in indexedCircleFrames.keys():
         frame.append((None,indexedCircleFrames[i]))
      else:
          frame.append(prevCursor)
      frames.append(frame)
   
   return replay, frames
