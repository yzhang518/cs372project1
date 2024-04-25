# Predefined configuration
config = {
    'servers': [
        {
            'type': 'HTTPS',
            'url': 'https://www.google.com/',
            'interval': 5
        },
        {
            'type': 'HTTP',
            'url': 'http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html',
            'interval': 5
        },
        {
            'type': 'ICMP',
            'server': '8.8.8.8',
            'interval': 5
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
            'interval': 10
        },
        {
            'type': 'TCP',
            'address': 'wikipedia.org',
            'port': 80,
            'interval': 10
        },
        {
            'type': 'UDP',
            'address': '1.1.1.1',
            'port': 53,
            'interval': 10
        },
        {
            'type': 'NTP',
            'address': 'pool.ntp.org',
            'interval': 15
        },
        {
        'type': 'ECHO',
        'address': '127.0.0.1',
        'port': 12345,
        'interval': 30,
        'message': "hello from YZ"
        }
    ]
}