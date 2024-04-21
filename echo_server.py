import socket
import threading

def handle_client(connection, address):
    print(f"Connected with {address}")
    try:
        while True:
            data = connection.recv(1024)
            if data:
                message = data.decode()
                print(f"Received message: {message}")
                response = f"Echo: {message}"
                connection.sendall(response.encode())
                if message.lower() == 'goodbye':
                    print(f"Disconnecting {address}")
                    break
            else:
                break
    finally:
        connection.close()

def echo_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))
        server_sock.listen()
        print(f"Echo server is running at {host}:{port}")
        
        try:
            while True:
                client_sock, client_addr = server_sock.accept()
                thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
                thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down...")

if __name__ == "__main__":
    echo_server()
