from Ping import Ping
from Pong import Pong
from encode import encode
from decode import decode

def test_ping_request():
    p1 = Ping()
    p1.telegramType = 0x01
    p1.message = "Hello"
    p1.messageLength = len("Hello")
    data = encode(p1)
    assert data == b'\x01\x00\x05Hello'
    assert len(data) == 8
    p2 = decode(data)
    assert p1.telegramType == p2.telegramType
    assert p1.messageLength == p2.messageLength
    assert p1.message == p2.message
    
def test_pong_request():
    p1 = Pong()
    p1.telegramType = 0x02
    p1.message = "PongPong"
    p1.messageLength = len("PongPong")
    data = encode(p1)
    assert data[0] == 2
    assert data == b'\x02\x00\x08PongPong'
    assert len(data) == 11
    p2 = decode(data)
    assert p1.telegramType == p2.telegramType
    assert p1.messageLength == p2.messageLength
    assert p1.message == p2.message

