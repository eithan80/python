import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break

def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))


def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    return client_socket

def start_client():
    client_socket = connect_to_server()

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

def close_connection(client_socket):
    client_socket.close()

