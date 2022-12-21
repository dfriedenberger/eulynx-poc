import time
import socket 
import argparse

from pingrequest import PingRequest
from pongresponse import PongResponse

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


def call():
    try:
        ping = PingRequest()
        ping.set_message("Hello")
        print("Send to server:",ping)
       
        client_socket = socket.socket()  # instantiate
        print('Connect to',host,port)  # show in terminal

        client_socket.connect((host, port))  # connect to the server

        client_socket.send(ping.encode())  # send message
        data = client_socket.recv(1024)  # receive response
        pong = PongResponse.decode(data)
        print('Received from server: ' + str(pong))  # show in terminal

        client_socket.close()  # close the connection
    except ConnectionRefusedError as e:
        print(e)
    except ConnectionResetError as e:
        print(e)


while True:
    call()
    time.sleep(10)
