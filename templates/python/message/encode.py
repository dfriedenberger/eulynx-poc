import struct

def encode(o):
    data = b''
    data += struct.pack('B',o.telegramType)
    data += struct.pack('!H',o.messageLength)
    data += bytes(o.message,'utf-8')
    return data
    


