import starter


def get_user_config():
    """
    Get user input for server, param for service checn and interval.
    Users can input 'Done' to terminate the app.
    """
    pass

#TODO: modify the values. for now they are from classmate's post
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
            'interval': 30  # Check every 30 seconds
        },
        {
            'type': 'DNS',
            'address': '8.8.8.8',
            'query': 'ubuntu.com',
            'record_type': 'A',  
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
        }
    ]
}

def monitor_services(config):
    """
    """
    while True:
        for server in config['servers']:
            match server['type']:
                case 'HTTP':
                    pass
                case 'HTTPS':
                    pass
                case _:
                    print(f"Unknown service type: {server['type']}")
                


