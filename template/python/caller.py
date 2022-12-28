import time
import socket 
import argparse
import threading
import queue
import os

from Ping import Ping
from encode import encode
from decode import decode

from statemachine.statemachine import StateMachine
from statemachine.state import State

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



class Client:

    state_init = State("Init")
    state_idle = State("Idle")
    state_connected = State("Connected")
    state_handle_recv_data = State("HandleRecvData")
    state_closed = State("Closed")

    def __init__(self,host,port):
        self.error = None
        self.host = host
        self.port = port
        self.socket = None
        self.send_data = queue.Queue()
        self.recv_data = queue.Queue()

    def send_ping(self):
        ping = Ping()
        ping.telegramType = 0x01
        ping.messageLength = len("Hello")
        ping.message = "Hello"
        self.send_data.put(ping)

    # Conditions
    def always_true(self):
        return True

    def has_send_data(self):
        return self.send_data.qsize() > 0

    def has_recv_data(self):
        return self.recv_data.qsize() > 0

    def has_error(self):
        return self.error != None

    #Transitions
    def nop(self):
        pass
        
    def wait(self):
        time.sleep(3)


    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
        except socket.timeout:
            self.error = "Connect timeout"
        except:
            raise
       

    def init(self):
        self.socket = socket.socket()
        self.socket.settimeout(0.2) 

    def send(self):
        pong = self.send_data.get()
        print("to connected user: " + pong.message)
        self.socket.send(encode(pong))  # send data to the client

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

    def handle_callback(self):
        ping = self.recv_data.get()
        print("recv response",ping)

    def close(self):
        self.socket.close()  # close the connection
        self.error = None

    def run(self):

        sm = StateMachine(self.state_init, {

            self.state_init      : [
                (self.always_true , self.init, self.state_idle)
            ],
            self.state_idle: [
                (self.always_true, self.connect , self.state_connected)
            ],
            self.state_connected : [
                (self.has_error , self.close, self.state_closed),
                (self.has_send_data , self.send, self.state_connected),
                (self.always_true , self.recv, self.state_handle_recv_data)
            ],
            self.state_handle_recv_data : [
                (self.has_recv_data , self.handle_callback, self.state_connected),
                (self.always_true , self.nop, self.state_connected)
            ],
            self.state_closed: [
                (self.always_true , self.wait, self.state_init)
            ]

        })

        while True:
            sm.nextState()


client = Client(host,port)
threading.Thread(target=client.run).start()


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