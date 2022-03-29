import socket

HEADER = 8
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "QUIT"
# SERVER = '192.168.1.16'
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print(client.recv(8).decode(FORMAT))
    
send('1')

send(DISCONNECT_MSG)