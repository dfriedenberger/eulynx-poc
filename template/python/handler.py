import socket
import argparse
import threading
import queue
import os
import time

from Ping import Ping
from Pong import Pong
from encode import encode
from decode import decode

from statemachine.statemachine import StateMachine
from statemachine.state import State
from ServerStateMachine import ServerStateMachine
from ConnectionStateMachine import ConnectionStateMachine


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


class Connection(ConnectionStateMachine):


    def __init__(self,connection):
        self.error = None
        self.connection = connection
        self.send_data = queue.Queue()
        self.recv_data = queue.Queue()

	# Conditions/Guards
    def is_error(self):
        return self.error != None

    def is_recv_data(self):
        return self.recv_data.qsize() > 0

    def is_true(self):
        return True

    def is_no_error_and_no_send_data(self):
        return not self.is_error() and not self.is_send_data() 

    def is_send_data(self):
        return self.send_data.qsize() > 0

    def is_timeout(self):
        return self.recv_data.empty()

	# Transitions
    def close(self):
        self.connection.close()  # close the connection

    def handle_callback(self):
        ping = self.recv_data.get()
        pong = handle_request(ping)
        self.send_data.put(pong)

    def initialize(self):
        self.connection.settimeout(0.2) 

    def recv(self):
        try:
            request = self.connection.recv(1024)
        except socket.timeout:
            pass
        except:
            raise
        else:
            print("Receive",request)
            if len(request) == 0: #NoData
                self.error = "Zero Data Received"
                return
            ping = decode(request)
            print("from connected user: " + ping.message)
            self.recv_data.put(ping)

    def send(self):
        pong = self.send_data.get()
        print("to connected user: " + pong.message)
        self.connection.send(encode(pong))  # send data to the client

    def timeout(self):
        pass
        
class Server(ServerStateMachine):

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.connection_queue = queue.Queue()

	# Conditions/Guards
    def is_true(self):
        return True

    def is_timeout(self):
        return self.connection_queue.empty()

    def is_new_connection(self):
        return self.connection_queue.qsize() > 0

	# Transitions
    def accept(self):
        try:
            conn, address = self.server_socket.accept()  # accept new connection
        except socket.timeout:
            pass
        except:
            raise
        else:
            print("Connection from: " + str(address))
            self.connection_queue.put(conn)

    def initialize(self):
        self.server_socket = socket.socket()  # get instance

        # look closely. The bind() function takes tuple as argument
        print("bind",self.host,self.port)
        self.server_socket.bind((self.host, self.port))  # bind host address and port together

        # configure timeout for listening
        self.server_socket.settimeout(0.2) 
    
        # configure how many client the server can listen simultaneously
        self.server_socket.listen(2)

    def timeout(self):
        pass

    def handle_connection(self):
        connection = self.connection_queue.get()
        client = Connection(connection)
        threading.Thread(target=client.run).start()


server = Server(host,port)
threading.Thread(target=server.run).start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C called")
os._exit(1)


