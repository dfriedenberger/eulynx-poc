import socket
import argparse

def handle_request(request):
    response = "Pong"
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
    request = conn.recv(1024).decode()
    print("from connected user: " + str(request))
    response = handle_request(request)
    print("to connected user: " + str(response))

    conn.send(response.encode())  # send data to the client
    conn.close()  # close the connection