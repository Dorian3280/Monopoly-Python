import socket
import threading

from monopoly import Monopoly

HEADER = 8
PORT = 5050
SERVER = '127.0.0.1'
# SERVER = '192.168.1.16'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "QUIT"
CONNECT_MSG = "CONN"
START_MSG = "GO"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(conn, address):
    print(f"[NEW CONNECTION] {address} connected")

    connected = True
    while connected:
        response = conn.recv(HEADER).decode(FORMAT)
        if response != '':
            print('response : ', response)
            if response == CONNECT_MSG:
                conn.send("200".encode(FORMAT))

            if response == DISCONNECT_MSG:
                break

    conn.close()

def start():
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")

    while True:
        print(threading.activeCount() - 1)
        server.listen()
        conn, address = server.accept()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()

        if (threading.activeCount() - 1) == 2:
            monopoly.start_game()

if __name__ == "__main__":
    monopoly = Monopoly()
    monopoly.start_game()
    print("[Starting] server is starting...")
