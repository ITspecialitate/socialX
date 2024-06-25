import socket
import threading
import tkinter
from tkinter import scrolledtext, END
from datetime import datetime

# Klienta iestatījumi
HOST = '127.0.0.1'  # Lokālais hosts
PORT = 12345        # Ports

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_box.config(state=tkinter.NORMAL)
            chat_box.insert(END, message + '\n')
            chat_box.config(state=tkinter.DISABLED)
            chat_box.yview(END)
        except:
            print("An error occurred!")
            client.close()
            break

def send_message():
    message = message_box.get("1.0", END).strip()
    message_box.delete("1.0", END)
    if message:
        timestamp = datetime.now().strftime('%y:%d   %H:%M:%S')
        message_with_nickname = f"{nickname}: {message} ({timestamp})"
        client.send(message_with_nickname.encode('utf-8'))
        chat_box.config(state=tkinter.NORMAL)
        chat_box.insert(END, message_with_nickname + '\n')
        chat_box.config(state=tkinter.DISABLED)
        chat_box.yview(END)

def connect_to_server():
    global nickname
    nickname = nickname_entry.get()
    if nickname:
        client.send(nickname.encode('utf-8'))
        nickname_entry.config(state=tkinter.DISABLED)
        connect_button.config(state=tkinter.DISABLED)

# Izveido GUI
root = tkinter.Tk()
root.title("Chat Room")

nickname_label = tkinter.Label(root, text="Enter your nickname:")
nickname_label.pack(pady=5)

nickname_entry = tkinter.Entry(root)
nickname_entry.pack(padx=20, pady=5)

connect_button = tkinter.Button(root, text="Connect", command=connect_to_server)
connect_button.pack(pady=5)

chat_box = scrolledtext.ScrolledText(root, state=tkinter.DISABLED)
chat_box.pack(padx=20, pady=5)

message_box = tkinter.Text(root, height=3)
message_box.pack(padx=20, pady=5)

send_button = tkinter.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Uzsāk pavedienu ziņu saņemšanai
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()
