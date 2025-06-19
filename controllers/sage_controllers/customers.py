import json
import os
import socket
import requests
import urllib3  # Add this import
from dotenv import load_dotenv

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env
load_dotenv()

def is_internal_network():
    """
    Check if we're likely running on the internal network by testing if we can
    resolve the internal hostname quickly.
    """
    try:
        # Try to resolve the internal server hostname with a short timeout
        socket.getaddrinfo('server69.cw-direct.co.uk', 50027)
        return True
    except (socket.gaierror, socket.timeout):
        return False
    finally:
        # Reset socket timeout to default
        socket.setdefaulttimeout(None)


def get_api_url():
    """
    Function to get the API URL with fallback support.
    Detects whether we're on internal or external network to choose 
    the appropriate connection route.
    """
    # Get configured URLs from environment
    internal_url = os.getenv("SAGE_API_URL_INTERNAL") or os.environ.get("SAGE_API_URL_INTERNAL")
    external_url = os.getenv("SAGE_API_URL") or os.environ.get("SAGE_API_URL")
    
    # Define direct internal server connection as backup option
    # direct_internal = "https://10.0.0.69:50027"  # Direct IP to SERVER69
    
    # If we're likely on the internal network, prioritize internal connections
    if is_internal_network():
        print("Detected internal network, prioritizing direct internal connection")
        return internal_url
    else:
        print("Detected external network, prioritizing external connection")
        return external_url


def test_connection():
    url = get_api_url()
    print(f"\nFinal selected API URL: {url}")
    
    # Optional: Try making a basic API request with the selected URL
    # This helps verify the URL works beyond just being reachable
    try:
        test_endpoint = f"{url}/api/searchInvoice"  # Using an endpoint we know exists
        print(f"\nTesting API endpoint: {test_endpoint}")
        
        # Only send a HEAD request to avoid unnecessary data transfer
        headers = {
            'Content-Type': 'application/json',
            'AuthToken': os.getenv("SAGE_API_TOKEN") or os.environ.get("SAGE_API_TOKEN") or "test-token"
        }
        test_response = requests.head(test_endpoint, headers=headers, timeout=5, verify=False)
        
        print(f"API endpoint test status: {test_response.status_code}")
        if test_response.status_code < 400:
            print("✓ API endpoint is accessible")
        else:
            print("✗ API endpoint returned an error status")
    except requests.RequestException as e:
        print(f"✗ API endpoint test failed: {str(e)}")


API_URL = get_api_url()
API_TOKEN = os.getenv("SAGE_API_TOKEN")


if not API_TOKEN:
    API_TOKEN = os.environ.get("API_TOKEN")
