import socket
import datetime


def echo_client(message, host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            # print("Connected to echo server.")

            if message:
                sock.sendall(message.encode())
                response = sock.recv(1024).decode()
                print(f"{datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} Received: {response}")
                return response == f"Echo: {message}"

            # print("Disconnecting from server.")

        except socket.error as e:
            # print(f"Socket error: {e}")
            return False
        except Exception as e:
            # print(f"An error occurred: {e}")
            return False
