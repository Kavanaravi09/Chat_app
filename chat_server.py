print("Starting...")
import socket, threading
from datetime import datetime

clients = {}

def broadcast(msg, sender=None):
    for c in list(clients):
        if c != sender:
            try:
                c.send(msg.encode())
            except:
                pass

def handle(conn):
    name = "?"
    try:
        name = conn.recv(1024).decode()
        print("Connected:", name)
        clients[conn] = name
        broadcast(name + " joined the chat", conn)
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            t = datetime.now().strftime("%H:%M")
            broadcast("[" + t + "] " + name + ": " + data, conn)
    except Exception as e:
        print("Error:", e)
    clients.pop(conn, None)
    broadcast(name + " left the chat")
    conn.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 4444))
s.listen()
print("Server running...")
while True:
    conn, addr = s.accept()
    print("New connection from", addr)
    threading.Thread(target=handle, args=(conn,), daemon=True).start()