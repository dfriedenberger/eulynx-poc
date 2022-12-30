import time
import socket 
import argparse
import threading
import queue
import os
import uuid

from Ping import Ping
from encode import encode
from decode import decode

from statemachine.statemachine import StateMachine
from statemachine.state import State
from ClientStateMachine import ClientStateMachine

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



class Client(ClientStateMachine):

    def __init__(self,host,port):
        self.error = None
        self.host = host
        self.port = port
        self.socket = None
        self.send_data = queue.Queue()
        self.recv_data = queue.Queue()
        self.uuid = str(uuid.uuid4())

    def send_ping(self):
        ping = Ping()
        ping.telegramType = 0x01
        ping.message = f"Hello id={self.uuid}"
        ping.messageLength = len(ping.message)
        self.send_data.put(ping)

	# Conditions/Guards
    def is_error(self):
        return self.error != None

    def is_true(self):
        return True

    def is_no_error_and_no_send_data(self):
        return not self.is_error() and not self.is_send_data()

    def is_send_data(self):
        return self.send_data.qsize() > 0

    def is_timeout(self):
        return self.recv_data.empty()

    def is_recv_data(self):
        return self.recv_data.qsize() > 0

	# Transitions
    def close(self):
        self.socket.close()  # close the connection
        self.error = None

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
        except socket.timeout:
            self.error = "Connect timeout"
        except socket.error as e:
            print(e)
            self.error = str(e)
        except:
            raise

    def initialize(self):
        self.socket = socket.socket()
        self.socket.settimeout(0.2) 

    def recv(self):
        try:
            request = self.socket.recv(1024)
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
        self.socket.send(encode(pong))  # send data to the client

    def timeout(self):
        pass

    def wait(self):
        time.sleep(3)

    def handle_callback(self):
        ping = self.recv_data.get()
        print("recv response",ping)





client = Client(host,port)
threading.Thread(target=client.run).start()


# send cyclic ping
def ping():
    while True:
        client.send_ping()
        time.sleep(10)

threading.Thread(target=ping).start()



try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C called")
os._exit(1)