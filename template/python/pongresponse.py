

class PongResponse:

    def __init__(self):
        pass

    def set_message(self,msg : str):
        self.msg = msg 

    def encode(self) -> bytearray:
        data = bytearray()
        data.append(2) #Type Pong

        message = self.msg.encode('utf-8')
        data.append(len(message)) #0-255
        data += message
        return data

    def __str__(self):
        return f"PongResponse({self.msg})"

    @staticmethod
    def decode(data):
        if data[0] != 2:
            raise ValueError(f"Not a PongRequest {data[0]}")
        l = data[1]
        message = str(data[2:2+l], 'UTF-8')
        p = PongResponse()
        p.set_message(message)
        return p
