import socket

def echo_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            print("Connected to echo server. Type 'goodbye' to exit.")

            while True:
                message = input("Enter your message: ")
                if not message:
                    continue

                sock.sendall(message.encode())
                response = sock.recv(1024).decode()
                print(f"Received: {response}")

                if message.lower() == "goodbye":
                    print("Disconnecting from server.")
                    break

        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    echo_client()
