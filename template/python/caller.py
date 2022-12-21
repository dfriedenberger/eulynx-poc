import time
import socket 
import argparse

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


def call(message):
    try:
        print("Send to server:",message)
       
        client_socket = socket.socket()  # instantiate
        print('Connect to',host,port)  # show in terminal

        client_socket.connect((host, port))  # connect to the server

        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        client_socket.close()  # close the connection
    except ConnectionRefusedError as e:
        print(e)
    except ConnectionResetError as e:
        print(e)


while True:
    call("Ping")
    time.sleep(10)
