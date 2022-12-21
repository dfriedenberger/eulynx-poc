from pingrequest import PingRequest
from pongresponse import PongResponse

def test_ping_request():
    p1 = PingRequest()
    p1.set_message("Ping")
    data = p1.encode()
    assert data[0] == 1
    assert data == b'\x01\x04Ping'
    assert len(data) == 6
    p2 = PingRequest.decode(data)
    assert p1.msg == p2.msg

def test_pong_request():
    p1 = PongResponse()
    p1.set_message("PongPong")
    data = p1.encode()
    assert data[0] == 2
    assert data == b'\x02\x08PongPong'
    assert len(data) == 10
    p2 = PongResponse.decode(data)
    assert p1.msg == p2.msg

