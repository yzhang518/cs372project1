import threading
import json
import uuid
import time
import signal
from queue import Queue, Empty
import socket

import threading
import json
import uuid
import time
import signal
from queue import Queue, Empty
import socket


# Global consolidation queue and shutdown event
consolidation_queue = Queue()
shutdown_event = threading.Event()

# Signal handler for graceful shutdown
def signal_handler(signum, frame):
    print("Shutdown signal received")
    shutdown_event.set()

# Define a class to hold task information
class Task:
    def __init__(self, id, service):
        self.id = id
        self.service = service

    def execute(self):
        # Simulate task execution based on service type
        return {"task_id": self.id, "service": self.service, "result": f"Executed {self.service['type']} task"}

def producer(monitor_name, tasks, task_queue):
    while not shutdown_event.is_set():
        for task in tasks:
            if shutdown_event.is_set():
                break
            task_id = f"{monitor_name}-{str(uuid.uuid4())}"
            task_obj = Task(task_id, task)
            result = task_obj.execute()
            task_queue.put(result)
            time.sleep(task['interval'])

def consumer(task_queue, consolidation_queue, client_socket):
    while not shutdown_event.is_set():
        try:
            task_result = task_queue.get(timeout=3)  # Adjust timeout as needed
            # Send task to the monitor server
            client_socket.sendall(json.dumps(task_result).encode())
            # Receive the acknowledgment from the monitor server
            ack = client_socket.recv(1024)
            if not ack:
                print("No acknowledgment received from monitor.")
                continue
            try:
                ack_message = json.loads(ack.decode())
                consolidation_queue.put(ack_message)
            except json.JSONDecodeError as e:
                print(f"Error decoding acknowledgment: {e}")
                print(f"Received data: {ack.decode()}")
        except Empty:
            continue
        except Exception as e:
            print(f"Error in consumer: {e}")
            break

def message_writer():
    while not shutdown_event.is_set():
        try:
            message = consolidation_queue.get(timeout=3)  # Adjust timeout as needed
            if 'task_id' in message and 'service' in message:
                if 'msg' in message:
                    print(f"Task ID: {message['task_id']}, Service: {message['service']}, Result: {message['msg']}")
                elif 'message' in message:
                    print(f"Task ID: {message['task_id']}, Service: {message['service']}, Error: {message['message']}")
                else:
                    print(f"Invalid message format received: {message}")
            else:
                print(f"Invalid message format received: {message}")
        except Empty:
            continue

def start_monitor_client(monitor_config, tasks):
    monitor_name = monitor_config['monitor_name']
    server_ip = monitor_config['ip']
    server_port = monitor_config['port']
    
    # Establish connection to the monitor server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to {monitor_name} at {server_ip}:{server_port}")
    
    task_queue = Queue()
    producer_thread = threading.Thread(target=producer, args=(monitor_name, tasks, task_queue))
    consumer_thread = threading.Thread(target=consumer, args=(task_queue, consolidation_queue, client_socket))
    
    producer_thread.start()
    consumer_thread.start()
    
    return producer_thread, consumer_thread, client_socket

def main():
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    tasks = [
        {'type': 'HTTPS', 'url': 'https://www.google.com/', 'interval': 5},
        {'type': 'HTTP', 'url': 'http://example.com', 'interval': 5}
    ]
    
    monitor_configs = [
        {'monitor_name': 'Monitor1', 'ip': '127.0.0.1', 'port': 65432},
        {'monitor_name': 'Monitor2', 'ip': '127.0.0.1', 'port': 65433}
    ]
    
    threads = []
    sockets = []
    for config in monitor_configs:
        producer_thread, consumer_thread, client_socket = start_monitor_client(config, tasks)
        threads.extend([producer_thread, consumer_thread])
        sockets.append(client_socket)
    
    writer_thread = threading.Thread(target=message_writer)
    writer_thread.start()
    threads.append(writer_thread)
    
    try:
        while not shutdown_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt, shutting down")
        shutdown_event.set()
    
    for thread in threads:
        thread.join(timeout=3)
        if thread.is_alive():
            print(f"Thread {thread.name} did not terminate")
    
    for s in sockets:
        s.close()

if __name__ == "__main__":
    main()

