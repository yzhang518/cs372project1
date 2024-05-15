import json
import socket
import threading
import sys
from queue import Queue
import helper_networkMonitor as helper


results_queue = Queue()


def handle_client_connection(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)  # Receive a larger chunk of data to accommodate multiple tasks
            if not data:
                print("No data received, closing connection.")
                break  # Exit the loop to close the connection

            task_info = json.loads(data.decode())
            print(f"Received task: {task_info}")

            # Ensure the received data is a dictionary and has the required keys
            if not isinstance(task_info, dict) or 'service' not in task_info or 'task_id' not in task_info:
                print("Invalid task data format received.")
                ack_message = json.dumps({'status': 'error', 'message': 'Invalid task data format'})
                client_socket.sendall(ack_message.encode())
                continue

            result = execute_task(task_info['service'])
            if result:
                ack_message = json.dumps({'status': 'received', 'task_id': task_info['task_id'], 'service': task_info['service'], 'msg': result})
            else:
                ack_message = json.dumps({'status': 'error', 'task_id': task_info['task_id'], 'service': task_info['service'], 'message': 'Config error, resend required'})

            results_queue.put(ack_message)  # Add the acknowledgment to the queue to be sent
            send_results(client_socket)  # Attempt to send results in the queue

    except Exception as e:
        print(f"Error handling client connection: {e}")
    finally:
        client_socket.close()
        print("Client connection closed")


def execute_task(service):
    try:
        if service['type'] == 'HTTPS':
            return helper.print_https(service)
        elif service['type'] == 'HTTP':
            return helper.print_http(service)
        elif service['type'] == 'ICMP':
            return helper.print_icmp(service)
        elif service['type'] == 'DNS':
            return helper.print_dns(service)
        elif service['type'] == 'TCP':
            return helper.print_tcp(service)
        elif service['type'] == 'UDP':
            return helper.print_udp(service)
        elif service['type'] == 'NTP':
            return helper.print_ntp(service)
        else:
            return "Unsupported service type"
    except Exception as e:
        print(f"Error executing task for {service['type']}: {e}")
        return None


def send_results(client_socket):
    while not results_queue.empty():
        try:
            result = results_queue.get_nowait()
            client_socket.sendall(result.encode())
        except socket.error as e:
            print(f"Error sending result: {e}")
            results_queue.put(result)  # Put the result back in the queue if send fails
            break


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable address reuse
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
            client_thread.start()
    finally:
        server_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python monitor.py <IP> <PORT>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])

    start_server(ip, port)
