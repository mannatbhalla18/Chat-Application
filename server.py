import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
LISTENER_LIMIT = 5
active_clients = []

def listen_for_messages(client, username):
    while True:  
        message = client.recv(2048).decode('utf-8')
        if message.strip():  
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print("The message sent from client is empty.")

def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client):
    while True:  # Infinite loop for handling client username
        username = client.recv(2048).decode('utf-8')
        if username.strip():  # Check if username is not empty
            active_clients.append((username, client))
            prompt_message = f"SERVER~{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty!")
    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except:
        print(f"Unable to bind to host: {HOST} and port: {PORT}")
        return

    server.listen(LISTENER_LIMIT)
    print("Server is listening for incoming connections...")

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]}:{address[1]}")

        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
