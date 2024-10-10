import struct
import lzma

# Function to decode ULEB128 values into a readable format
def decodeULEB(data, off):
    result = 0
    shift = 0
    size = 0
    while True:
        byte = data[off + size]
        size += 1
        result |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return result, size

# Function to read the strings from the byte arrays provided by the .osr file (thnaks for making it a pain peppy)
def readString(data, off):
    marker, = struct.unpack_from("<B", data, off)
    off += 1
    if marker == 0x0b:
        length, bytes = decodeULEB(data, off)
        off += bytes
        string = data[off:off + length].decode('utf-8')
        off += length
        return string, off
    else:
        return "", off

# Function to decode LZMA values
def decodeLZMA(data):
    decompressor = lzma.LZMADecompressor()
    decodedData = decompressor.decompress(data).decode('utf-8')
    return decodedData
