import socket


def echo_server():
    # Create a Socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the Socket:
    server_address = '127.0.0.1'
    server_port = 65432
    server_sock.bind((server_address, server_port))

    # Listen for Incoming Connections:
    server_sock.listen(5)
    print("Server is listening for incoming connections...")

    try:
        client_sock, client_address = server_sock.accept()
        print(f"Connection from {client_address}")

        try:
            while True:
                # Receive Data:
                try:
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
                    break
                except Exception as e:
                    print(f"Other error: {e}")
                    break

        finally:
            # Close Client Connection:
            client_sock.close()
            print(f"Connection with {client_address} closed")

    except KeyboardInterrupt:
        print("Server is shutting down")

    finally:
        # Close Server Socket:
        server_sock.close()
        print("Server socket closed")


if __name__ == "__main__":
    echo_server()
