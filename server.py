import socket
import threading

clients = {}

def broadcast(message, sender_conn):
    for conn in clients:
        if conn != sender_conn:
            try:
                conn.send(message)
            except:
                conn.close()
                del clients[conn]

def handle_client(conn, addr):
    username = conn.recv(1024).decode()  # first message is username
    clients[conn] = username
    print(f"{username} connected from {addr}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode())  # log with username
            broadcast(data, conn)
        except:
            break

    conn.close()
    del clients[conn]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 6000))
server.listen()

print("Server started... waiting for connections")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
