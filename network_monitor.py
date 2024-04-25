import helper_networkMonitor as helper
from config import config
import time
import threading
import datetime


def monitor_services(server, stop_event):
    """
    """
    global echo_server

    while not stop_event.is_set():
        match server['type']:
            case 'HTTPS':
                helper.print_https(server)
            case 'HTTP':
                helper.print_http(server)
                pass
            case 'ICMP':
                helper.print_icmp(server)
            case 'DNS':
                helper.print_dns(server)
            case 'TCP':
                helper.print_tcp(server)
            case 'UDP':
                helper.print_udp(server)
            case 'NTP':
                helper.print_ntp(server)
            case 'ECHO':
                echo_server = server
                helper.print_echo(server)
            case _:
                print(f"Unknown service type: {server['type']}")
        time.sleep(server['interval'])


def main():
    stop_event = threading.Event()
    threads = []

    for server in config['servers']:
        thread = threading.Thread(target=monitor_services, args=(server, stop_event))
        threads.append(thread)
        thread.start()

    try:
        input("Press Enter to terminate the monitoring.\n")
        print("Terminating the monitoring... Please wait.")
    finally:
        stop_event.set()
        for thread in threads:
            thread.join()

        print(echo_server['address'])
        helper.send_goodbye(echo_server)
        print("Monitoring has been successfully terminated.")


if __name__ == "__main__":

    main()
