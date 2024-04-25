import socket

def echo_server(host='127.0.0.1', port=12345):
    # Create a Socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the Socket:
    server_address = host
    server_port = port
    server_sock.bind((server_address, server_port))

    # Listen for Incoming Connections:
    server_sock.listen(5)
    print("Server is listening for incoming connections...")

    try:
        # Loop to handle multiple connections
        while True:
            client_sock, client_address = server_sock.accept()
            print(f"Connection from {client_address}")

            try:
                while True:
                    # Receive Data:
                    message = client_sock.recv(1024).decode()
                    if not message:
                        # No message means the client has disconnected
                        break

                    print(f"Received message: {message}")

                    # Check if the message is 'goodbye'
                    if message.lower() == 'goodbye':
                        response = "Goodbye acknowledged"
                        client_sock.sendall(response.encode())
                        break

                    # Echo the received message back to the client
                    response = f"Echo: {message}"
                    client_sock.sendall(response.encode())

            except socket.error as e:
                print(f"Socket error: {e}")
            except Exception as e:
                print(f"Other error: {e}")
            finally:
                # Close Client Connection:
                client_sock.close()
                print(f"Connection with {client_address} closed")

            # Check if the received message was 'goodbye' to decide to close the server
            if message.lower() == 'goodbye':
                break

    except KeyboardInterrupt:
        print("Server is shutting down")

    finally:
        # Close Server Socket:
        server_sock.close()
        print("Server socket closed")

if __name__ == "__main__":
    echo_server()
