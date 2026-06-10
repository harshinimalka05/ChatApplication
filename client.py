import socket
import threading

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode()
            print(msg)  # show full message with username
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 6000))  # match your server port

username = input("Enter your username: ")
client.send(username.encode())  # send username to server

thread = threading.Thread(target=receive_messages)
thread.start()

while True:
    msg = input()
    client.send(f"{username}: {msg}".encode())
