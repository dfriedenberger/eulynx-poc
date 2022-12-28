import socket
import argparse
import threading
import queue
import os

from Ping import Ping
from Pong import Pong
from encode import encode
from decode import decode

from statemachine.statemachine import StateMachine
from statemachine.state import State

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



class Client:

    state_init = State("Init")
    state_idle = State("Idle")
    state_handle_recv_data = State("HandleRecvData")
    state_closed = State("Closed")

    def __init__(self,connection):
        self.error = None
        self.connection = connection
        self.send_data = queue.Queue()
        self.recv_data = queue.Queue()

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

    def init(self):
        self.connection.settimeout(0.2) 

    def send(self):
        pong = self.send_data.get()
        print("to connected user: " + pong.message)
        self.connection.send(encode(pong))  # send data to the client

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

    def handle_callback(self):
        ping = self.recv_data.get()
        pong = handle_request(ping)
        self.send_data.put(pong)

    def close(self):
        self.connection.close()  # close the connection

    def run(self):
        sm = StateMachine(self.state_init, {

            self.state_init : [
                (self.always_true , self.init, self.state_idle)
            ],
            self.state_idle      : [
                (self.has_error , self.close, self.state_closed),
                (self.has_send_data , self.send, self.state_idle),
                (self.always_true , self.recv, self.state_handle_recv_data)
            ],
            self.state_handle_recv_data : [
                (self.has_recv_data , self.handle_callback, self.state_idle),
                (self.always_true , self.nop, self.state_idle)
            ]

        })

        while sm.nextState() != self.state_closed:
            pass
        
class Server:

    state_init = State("Init")
    state_wait_conn = State("WaitforConnection")
    state_handle_conn = State("HandleConnection")
    
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.connection_queue = queue.Queue()


    # Conditions
    def always_true(self):
        return True

    def has_timeout(self):
        return self.connection_queue.empty()

    #Transitions
    def nop(self):
        pass

    def init(self):
        self.server_socket = socket.socket()  # get instance

        # look closely. The bind() function takes tuple as argument
        print("bind",self.host,self.port)
        self.server_socket.bind((self.host, self.port))  # bind host address and port together

        # configure timeout for listening
        self.server_socket.settimeout(0.2) 
    
        # configure how many client the server can listen simultaneously
        self.server_socket.listen(2)

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
            
    def start_client(self):
        connection = self.connection_queue.get()
        client = Client(connection)
        threading.Thread(target=client.run).start()
        
        

    def run(self):
        sm = StateMachine(self.state_init, {

            self.state_init      : [
                (self.always_true , self.init, self.state_wait_conn)
            ],
            self.state_wait_conn: [
                (self.always_true, self.accept , self.state_handle_conn)
            ],
            self.state_handle_conn : [
                (self.has_timeout , self.nop, self.state_wait_conn),
                (self.always_true , self.start_client, self.state_wait_conn)
            ]

        })

        while True:
            sm.nextState()


server = Server(host,port)
threading.Thread(target=server.run).start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C called")
os._exit(1)


