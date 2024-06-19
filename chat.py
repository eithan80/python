import socket
import threading
import sqlite3

clients = []
def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def handle_client(client_socket, client_address):
    with sqlite3.connect("chat.db") as conn:
        cursor = conn.cursor()
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"{client_address}: {message}")
                    broadcast(message, client_socket)
                    cursor.execute("INSERT INTO messages (client, message) VALUES (?, ?)", (str(client_address), message))
                    conn.commit()
                else:
                    remove(client_socket)
                    break
            except:
                remove(client_socket)
                break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def setup_database():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Server started and listening on port 12345")
    setup_database()

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        print(f"Connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    start_server()
