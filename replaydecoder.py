import struct
import decoders

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
    replayInfo["mods"] = struct.unpack_from("<I", replayData, offset)[0]
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
