import helper_networkMonitor as helper
import time

def get_user_config():
    """
    Get user input for server, param for service checn and interval.
    Users can input 'Done' to terminate the app.
    """
    pass


# TODO: modify the values. for now they are from classmate's post
# Predefined configuration
config = {
    'servers': [
        {
            'type': 'HTTPS',
            'url': 'https://www.google.com/',
            'interval': 60
        },
        {
            'type': 'HTTP',
            'url': 'http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html',
            'interval': 60
        },
        {
            'type': 'ICMP',
            'address': 'nasa.gov',
            'interval': 30
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
            'interval': 300  # Check every 5 minutes
        },
        {
            'type': 'TCP',
            'address': 'wikipedia.org',
            'port': 80,
            'interval': 150
        },
        {
            'type': 'UDP',
            'address': '1.1.1.1',
            'port': 53,
            'interval': 180
        },
        {
            'type': 'NTP',
            'address': 'pool.ntp.org',
            'interval': 360  # Check every 6 minutes
        }
    ]
}


def monitor_services(config):
    """
    """
    for server in config['servers']:
        match server['type']:
            case 'HTTP':
                helper.print_http(server)
            case 'HTTPS':
                helper.print_https(server)
                pass
            case 'ICMP':
                pass
            case 'DNS':
                helper.print_dns(server)
            case 'TCP':
                helper.print_tcp(server)
            case 'UDP':
                helper.print_udp(server)
            case 'NTP':
                helper.print_ntp(server)
            case _:
                print(f"Unknown service type: {server['type']}")
        # time.sleep(server['interval'])


monitor_services(config)
