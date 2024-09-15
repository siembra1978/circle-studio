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

def whatMods(modId):
    result = ''
    for key in mods.keys():
        #print(key, modId)
        if modId >= int(key) and modId > 0:
            modId = modId - int(key)
            result = result + mods.get(key)
            #print(result)
        #time.sleep(.25)
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

    return replayInfo
