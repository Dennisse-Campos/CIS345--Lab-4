import socket
import threading

def listen_for_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            print("Server closed connection.")
            break
        print("\n[Server] "+data.decode('utf-8'))


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))
    
    listener = threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True)
    listener.start()
    
    print("Commands: /count | Ctrl+c or exit to quit")
    print("This server broadcasts all messages")
    
    try:
        while True:
            message = input("> ")
            
            if message.lower() == "exit":
                print("Closing client...")
                client_socket.close()
                break
            
            client_socket.sendall(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Closing client...")
        client_socket.close()
        exit(0)


if __name__ == "__main__":
    main()

