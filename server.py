import socket
import threading

HEADER = 8
PORT = 5050
SERVER = '127.0.0.1'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "QUIT"
        
server.bind(ADDRESS)

def handle_client(conn, address):
    print(f"[NEW CONNECTION] {address} connected")
    
    connected = True
    while connected:
        response = conn.recv(HEADER).decode(FORMAT)
        if response != '':
            print('response : ', response)
            if response == DISCONNECT_MSG:
                break
            conn.send("200".encode(FORMAT))
    
    conn.close()

        
def start():
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    
    while True:
        server.listen()
        conn, address = server.accept()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()

print("[Starting] server is starting...")
start()
server.stop()