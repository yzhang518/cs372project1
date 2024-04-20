import os
import socket
import struct
import threading
import time
import zlib
import random
import string
import requests
import ntplib
import dns.resolver
import dns.exception
from socket import gaierror
from time import ctime
from typing import Tuple, Optional, Any


def check_server_http(url: str) -> Tuple[bool, Optional[int]]:
    """
    Check if an HTTP server is up by making a request to the provided URL.

    This function attempts to connect to a web server using the specified URL.
    It returns a tuple containing a boolean indicating whether the server is up,
    and the HTTP status code returned by the server.

    :param url: URL of the server (including http://)
    :return: Tuple (True/False, status code)
             True if server is up (status code < 400), False otherwise
    """
    try:
        # Making a GET request to the server
        response: requests.Response = requests.get(url)

        # The HTTP status code is a number that indicates the outcome of the request.
        # Here, we consider status codes less than 400 as successful,
        # meaning the server is up and reachable.
        # Common successful status codes are 200 (OK), 301 (Moved Permanently), etc.
        is_up: bool = response.status_code < 400

        # Returning a tuple: (True/False, status code)
        # True if the server is up, False if an exception occurs (see except block)
        return is_up, response.status_code

    except requests.RequestException:
        # This block catches any exception that might occur during the request.
        # This includes network problems, invalid URL, etc.
        # If an exception occurs, we assume the server is down.
        # Returning False for the status, and None for the status code,
        # as we couldn't successfully connect to the server to get a status code.
        return False, None


def print_http(url: str):
    """
    """
    http_url = url
    http_server_status, http_server_response_code = check_server_http(url)
    print(f"HTTP URL: {http_url}, Status Code: {http_server_response_code if http_server_response_code is not None else 'N/A'}")


def check_server_https(url: str, timeout: int = 5) -> Tuple[bool, Optional[int], str]:
    """
    Check if an HTTPS server is up by making a request to the provided URL.

    This function attempts to connect to a web server using the specified URL with HTTPS.
    It returns a tuple containing a boolean indicating whether the server is up,
    the HTTP status code returned by the server, and a descriptive message.

    :param url: URL of the server (including https://)
    :param timeout: Timeout for the request in seconds. Default is 5 seconds.
    :return: Tuple (True/False for server status, status code, description)
    """
    try:
        # Setting custom headers for the request. Here, 'User-Agent' is set to mimic a web browser.
        headers: dict = {'User-Agent': 'Mozilla/5.0'}

        # Making a GET request to the server with the specified URL and timeout.
        # The timeout ensures that the request does not hang indefinitely.
        response: requests.Response = requests.get(url, headers=headers, timeout=timeout)

        # Checking if the status code is less than 400. Status codes in the 200-399 range generally indicate success.
        is_up: bool = response.status_code < 400

        # Returning a tuple: (server status, status code, descriptive message)
        return is_up, response.status_code, "Server is up"

    except requests.ConnectionError:
        # This exception is raised for network-related errors, like DNS failure or refused connection.
        return False, None, "Connection error"

    except requests.Timeout:
        # This exception is raised if the server does not send any data in the allotted time (specified by timeout).
        return False, None, "Timeout occurred"

    except requests.RequestException as e:
        # A catch-all exception for any error not covered by the specific exceptions above.
        # 'e' contains the details of the exception.
        return False, None, f"Error during request: {e}"


def print_https(url: str):
    """
    """
    https_url = url
    https_server_status, https_server_response_code, description = check_server_https(https_url)
    print(f"HTTPS URL: {https_url}, Status Code: {https_server_response_code if https_server_response_code is not None else 'N/A'}, Description: {description}")
