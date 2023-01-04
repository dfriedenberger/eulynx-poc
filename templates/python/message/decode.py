from Ping import Ping
from Pong import Pong
import struct

def decode(data):
    o = None
    if data[0] == 0x01: o = Ping()
    if data[0] == 0x02: o = Pong()

    o.telegramType = struct.unpack('B',data[0:1])
    o.messageLength = struct.unpack('!H',data[1:3])
    o.message = data[3:].decode('utf-8')

    return o