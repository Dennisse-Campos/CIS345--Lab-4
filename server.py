import socket
import threading
import sys

client_count = 0
client_count_lock = threading.Lock()

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients:
            if client != sender_socket:  
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    pass 


def handle_client(client_socket, address):
    global client_count

    thread_name = threading.current_thread().name
    print(f"[{thread_name}] Handling client {address}")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"[{thread_name}] message: {message}")

            if message == "/count":
                with client_count_lock:
                    response = f"Active clients: {client_count}"
                client_socket.sendall(response.encode('utf-8'))

            else:
                broadcast_msg = f"[Broadcast] {message}"
                broadcast(broadcast_msg, client_socket)

                response = f"You said: {message}"
                client_socket.sendall(response.encode('utf-8'))

        except ConnectionResetError:
            print(f"[{thread_name}] Client disconnected abruptly")
            break

    with client_count_lock:
        client_count -= 1

    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

    client_socket.close()
    print(f"[{thread_name}] Connection closed for {address}")


def main():
    global client_count

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345

    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}. Type 'exit' to stop.")

 
    def input_thread():
        while True:
            cmd = input()
            if cmd == "exit":
                print("Shutting down server...")
                server_socket.close()
                sys.exit(0)

    threading.Thread(target=input_thread, daemon=True).start()

    while True:
        try:
            client_socket, client_address = server_socket.accept()
        except OSError:
            break

        with client_count_lock:
            client_count += 1

        with clients_lock:
            clients.append(client_socket)

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

        print(f"[Main] Clients connected: {client_count}")


if __name__ == "__main__":
    main()

