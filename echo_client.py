import socket


def echo_client():
    # Create a Socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Specify Server Address and Port:
    server_address = '127.0.0.1'
    server_port = 65432

    try:
        # Establish a Connection:
        sock.connect((server_address, server_port))

        while True:
            # Send and Receive Data:
            # Get user input
            message = input("Enter your message (type 'goodbye' to disconnect): ")
            print(f"Sending: {message}")
            sock.sendall(message.encode())

            # Receive the echo from the server
            response = sock.recv(1024)
            print(f"Received: {response.decode()}")

            # If the user sends 'goodbye', break the loop
            if message.lower() == 'goodbye':
                break

    finally:
        # Close the Connection:
        sock.close()


if __name__ == "__main__":
    echo_client()
