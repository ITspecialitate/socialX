import socket
import threading

# Servera iestatījumi
HOST = '127.0.0.1'  # Lokālais hosts
PORT = 12345        # Ports

# Savienojumu saraksts
clients = []
nicknames = {}

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            nickname = nicknames[client]
            broadcast(f"{nickname} has left the chat.".encode('utf-8'), client)
            clients.remove(client)
            del nicknames[client]
            client.close()
            break

def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames[client] = nickname

        clients.append(client)
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} has joined the chat.".encode('utf-8'), client)
        client.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive()
