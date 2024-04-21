import helper_networkMonitor as helper
import time
import threading


def get_user_config():
    """
    Get user input for server, param for service checn and interval.
    Users can input 'Done' to terminate the app.
    """
    pass


# Predefined configuration
config = {
    'servers': [
        {
            'type': 'HTTPS',
            'url': 'https://www.google.com/',
            'interval': 1
        },
        {
            'type': 'HTTP',
            'url': 'http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html',
            'interval': 1
        },
        {
            'type': 'ICMP',
            'server': '8.8.8.8',
            'interval': 1
        },
        {
            'type': 'DNS',
            'server': '8.8.8.8',  # Google's public DNS server
            'queries': [
                ('google.com', 'A'),
                ('google.com', 'MX'),
                ('google.com', 'AAAA'),
                ('google.com', 'CNAME'),
                ('yahoo.com', 'A'),
            ],
            'interval': 2
        },
        {
            'type': 'TCP',
            'address': 'wikipedia.org',
            'port': 80,
            'interval': 2
        },
        {
            'type': 'UDP',
            'address': '1.1.1.1',
            'port': 53,
            'interval': 2
        },
        {
            'type': 'NTP',
            'address': 'pool.ntp.org',
            'interval': 3
        },
        {
        'type': 'ECHO',
        'address': '127.0.0.1',
        'port': 65432,
        'interval': 1  # Interval in minutes
        }
    ]
}


def monitor_services(server, stop_event):
    """
    """
    while not stop_event.is_set():
        match server['type']:
            case 'HTTPS':
                helper.print_http(server)
            case 'HTTP':
                helper.print_https(server)
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
                pass
            case _:
                print(f"Unknown service type: {server['type']}")
        time.sleep(server['interval'])


def main():
    stop_event = threading.Event()
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
        print("Monitoring has been successfully terminated.")


if __name__ == "__main__":
    main()
