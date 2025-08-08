"""
Simple HTTP Requests Example

This module demonstrates basic HTTP request operations using the requests library.
It covers GET, POST requests, handling headers, parameters, and response processing.

Requirements:
    pip install requests

Usage Examples:
    # Basic GET request
    response = get_webpage("https://httpbin.org/get")
    
    # GET with parameters
    params = {"key": "value", "search": "python"}
    response = get_with_params("https://httpbin.org/get", params)
    
    # POST request with data
    data = {"username": "test", "password": "secret"}
    response = post_data("https://httpbin.org/post", data)

Author: Python Learning Examples
Date: August 2025
"""

import requests
import json
import time
from typing import Dict, Any, Optional, Union
from requests.exceptions import RequestException, Timeout, ConnectionError


def get_webpage(url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
    """
    Perform a simple GET request to fetch webpage content.
    
    Args:
        url (str): The URL to fetch
        timeout (int): Request timeout in seconds (default: 10)
        headers (Optional[Dict[str, str]]): Custom headers to include
    
    Returns:
        Optional[requests.Response]: Response object if successful, None otherwise
    
    Example:
        >>> response = get_webpage("https://httpbin.org/get")
        >>> if response:
        ...     print(f"Status: {response.status_code}")
        ...     print(f"Content: {response.text[:100]}...")
    """
    try:
        # Set default headers if none provided
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=timeout, headers=headers)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        print(f"✓ Success: Status {response.status_code}")
        print(f"✓ Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"✓ Content-Length: {len(response.content)} bytes")
        
        return response
        
    except Timeout:
        print(f"✗ Error: Request to {url} timed out after {timeout} seconds")
    except ConnectionError:
        print(f"✗ Error: Could not connect to {url}")
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
    except RequestException as e:
        print(f"✗ Request Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
    
    return None


def get_with_params(url: str, params: Dict[str, Any], timeout: int = 10) -> Optional[requests.Response]:
    """
    Perform a GET request with URL parameters.
    
    Args:
        url (str): The base URL
        params (Dict[str, Any]): Dictionary of parameters to include
        timeout (int): Request timeout in seconds
    
    Returns:
        Optional[requests.Response]: Response object if successful, None otherwise
    
    Example:
        >>> params = {"q": "python programming", "limit": 10}
        >>> response = get_with_params("https://httpbin.org/get", params)
        >>> if response:
        ...     data = response.json()
        ...     print(data.get('args'))  # Shows the parameters sent
    """
    try:
        print(f"Fetching: {url} with params: {params}")
        
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        
        print(f"✓ Success: Final URL: {response.url}")
        print(f"✓ Status: {response.status_code}")
        
        return response
        
    except RequestException as e:
        print(f"✗ Request Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
    
    return None


def post_data(url: str, data: Union[Dict[str, Any], str], 
              content_type: str = "form", timeout: int = 10) -> Optional[requests.Response]:
    """
    Perform a POST request with data.
    
    Args:
        url (str): The URL to post to
        data (Union[Dict[str, Any], str]): Data to send in the POST request
        content_type (str): Type of content - "form", "json", or "raw"
        timeout (int): Request timeout in seconds
    
    Returns:
        Optional[requests.Response]: Response object if successful, None otherwise
    
    Example:
        >>> data = {"username": "test", "email": "test@example.com"}
        >>> response = post_data("https://httpbin.org/post", data, "json")
        >>> if response:
        ...     result = response.json()
        ...     print(result.get('json'))  # Shows the JSON data sent
    """
    try:
        headers = {}
        
        if content_type.lower() == "json":
            headers['Content-Type'] = 'application/json'
            if isinstance(data, dict):
                data = json.dumps(data)
            response = requests.post(url, data=data, headers=headers, timeout=timeout)
        elif content_type.lower() == "form":
            response = requests.post(url, data=data, timeout=timeout)
        else:  # raw
            response = requests.post(url, data=data, timeout=timeout)
        
        response.raise_for_status()
        
        print(f"✓ POST Success: Status {response.status_code}")
        print(f"✓ Response received: {len(response.content)} bytes")
        
        return response
        
    except RequestException as e:
        print(f"✗ POST Request Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
    
    return None


def download_file(url: str, filename: str, chunk_size: int = 8192) -> bool:
    """
    Download a file from URL with progress indication.
    
    Args:
        url (str): URL of the file to download
        filename (str): Local filename to save as
        chunk_size (int): Size of chunks to download (default: 8192 bytes)
    
    Returns:
        bool: True if download successful, False otherwise
    
    Example:
        >>> success = download_file("https://httpbin.org/bytes/1024", "test_file.bin")
        >>> if success:
        ...     print("File downloaded successfully!")
    """
    try:
        print(f"Downloading {url} -> {filename}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
        
        print(f"\n✓ Download complete: {filename}")
        return True
        
    except RequestException as e:
        print(f"\n✗ Download Error: {e}")
    except IOError as e:
        print(f"\n✗ File Error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
    
    return False


def check_website_status(urls: list, timeout: int = 5) -> Dict[str, Dict[str, Any]]:
    """
    Check the status of multiple websites.
    
    Args:
        urls (list): List of URLs to check
        timeout (int): Request timeout in seconds
    
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary mapping URLs to their status info
    
    Example:
        >>> urls = ["https://google.com", "https://github.com", "https://nonexistent.site"]
        >>> results = check_website_status(urls)
        >>> for url, info in results.items():
        ...     print(f"{url}: {info['status']}")
    """
    results = {}
    
    for url in urls:
        print(f"Checking: {url}")
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=timeout)
            response_time = time.time() - start_time
            
            results[url] = {
                'status': 'online',
                'status_code': response.status_code,
                'response_time': round(response_time, 3),
                'headers': dict(response.headers),
                'error': None
            }
            
            print(f"  ✓ Status: {response.status_code} ({response_time:.3f}s)")
            
        except Exception as e:
            response_time = time.time() - start_time
            results[url] = {
                'status': 'offline',
                'status_code': None,
                'response_time': round(response_time, 3),
                'headers': {},
                'error': str(e)
            }
            
            print(f"  ✗ Error: {e}")
    
    return results


def main():
    """
    Demonstrate the usage of various HTTP request functions.
    
    This function shows practical examples of all the HTTP operations
    implemented in this module.
    """
    print("=== Simple HTTP Requests Demo ===\n")
    
    # Example 1: Basic GET request
    print("1. Basic GET Request:")
    response = get_webpage("https://httpbin.org/get")
    if response:
        try:
            data = response.json()
            print(f"   Your IP: {data.get('origin', 'Unknown')}")
            print(f"   User-Agent: {data.get('headers', {}).get('User-Agent', 'Unknown')[:50]}...")
        except json.JSONDecodeError:
            print("   Response is not JSON format")
    print()
    
    # Example 2: GET with parameters
    print("2. GET Request with Parameters:")
    params = {
        'search': 'python programming',
        'category': 'tutorials',
        'limit': 10
    }
    response = get_with_params("https://httpbin.org/get", params)
    if response:
        try:
            data = response.json()
            print(f"   Parameters sent: {data.get('args', {})}")
        except json.JSONDecodeError:
            print("   Response is not JSON format")
    print()
    
    # Example 3: POST request with JSON data
    print("3. POST Request with JSON Data:")
    post_data_example = {
        'username': 'demo_user',
        'email': 'demo@example.com',
        'age': 25,
        'interests': ['python', 'web scraping', 'automation']
    }
    response = post_data("https://httpbin.org/post", post_data_example, "json")
    if response:
        try:
            data = response.json()
            print(f"   Data sent: {data.get('json', {})}")
        except json.JSONDecodeError:
            print("   Response is not JSON format")
    print()
    
    # Example 4: Download a small file
    print("4. File Download:")
    download_success = download_file("https://httpbin.org/bytes/1024", "sample_download.bin")
    if download_success:
        import os
        size = os.path.getsize("sample_download.bin")
        print(f"   Downloaded file size: {size} bytes")
        # Clean up
        try:
            os.remove("sample_download.bin")
            print("   Temporary file cleaned up")
        except:
            pass
    print()
    
    # Example 5: Check website status
    print("5. Website Status Check:")
    test_urls = [
        "https://httpbin.org",
        "https://google.com",
        "https://github.com"
    ]
    status_results = check_website_status(test_urls)
    
    print("\n   Summary:")
    for url, info in status_results.items():
        status = info['status']
        code = info['status_code']
        time_taken = info['response_time']
        
        if status == 'online':
            print(f"   ✓ {url}: {status.upper()} (HTTP {code}) - {time_taken}s")
        else:
            print(f"   ✗ {url}: {status.upper()} - {info['error']}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()