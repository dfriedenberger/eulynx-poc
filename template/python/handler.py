import socket
import argparse

from Ping import Ping
from Pong import Pong
from encode import encode
from decode import decode

def handle_request(request : Ping) -> Pong:
    response = Pong()
    response.telegramType = 0x02
    response.messageLength = len(request.message)
    response.message = request.message
    return response


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for transform model to code.')
    parser.add_argument('-H', '--host',
                        help='host ip',
                        required='True',
                        default='localhost')
    parser.add_argument('-p', '--port',type=int,
                        help='port of socket',
                        default='5000')
    args = parser.parse_args()

    return args.host, args.port

host, port = parse_args()


server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
print("bind",host,port)
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(2)

while True:

    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    # receive data stream. it won't accept data packet greater than 1024 bytes
    request = conn.recv(1024)
    ping = decode(request)
    print("from connected user: " + ping.message)
    pong = handle_request(ping)
    print("to connected user: " + pong.message)

    conn.send(encode(pong))  # send data to the client
    conn.close()  # close the connection