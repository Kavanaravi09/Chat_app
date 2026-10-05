import socket, threading

s = socket.socket()
s.connect(("127.0.0.1",4444))
s.send(input("Your name: ").encode())

def receive():
    while True:
        data = s.recv(1024).decode()
        if not data: break
        print(data)
threading.Thread(target=receive, daemon=True).start()
while True:
    s.send(input().encode())