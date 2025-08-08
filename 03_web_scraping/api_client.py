"""
REST API Client Example

This module demonstrates how to consume REST APIs using the requests library.
It includes examples for authentication, pagination, rate limiting, and error handling.

Features:
- GET, POST, PUT, DELETE operations
- Authentication (API keys, Bearer tokens)
- Pagination handling
- Rate limiting
- Response caching
- Error handling and retries

Requirements:
    pip install requests

Usage Examples:
    # Create an API client
    client = APIClient("https://api.example.com", api_key="your-key")
    
    # Fetch data
    users = client.get("users")
    
    # Create new resource
    new_user = client.post("users", {"name": "John", "email": "john@example.com"})
    
    # Update resource
    updated_user = client.put("users/123", {"name": "John Doe"})
    
    # Delete resource
    client.delete("users/123")

Author: Python Learning Examples  
Date: August 2025
"""

import requests
import json
import time
import hashlib
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException, Timeout, ConnectionError
from datetime import datetime, timedelta


class APIClient:
    """
    A comprehensive REST API client with authentication, caching, and rate limiting.
    
    This client provides a clean interface for interacting with REST APIs while
    handling common concerns like authentication, retries, and response caching.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, 
                 auth_token: Optional[str] = None, timeout: int = 30,
                 max_retries: int = 3, rate_limit_delay: float = 0.1):
        """
        Initialize the API client.
        
        Args:
            base_url (str): The base URL of the API
            api_key (Optional[str]): API key for authentication
            auth_token (Optional[str]): Bearer token for authentication
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retries for failed requests
            rate_limit_delay (float): Delay between requests to avoid rate limiting
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        self.cache = {}  # Simple in-memory cache
        self.cache_duration = 300  # 5 minutes default cache
        
        # Set up session for connection reuse
        self.session = requests.Session()
        
        # Configure authentication
        if api_key:
            self.session.headers.update({'X-API-Key': api_key})
        elif auth_token:
            self.session.headers.update({'Authorization': f'Bearer {auth_token}'})
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'Python-API-Client/1.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _wait_for_rate_limit(self):
        """Implement simple rate limiting by adding delay between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _get_cache_key(self, method: str, url: str, params: Optional[Dict] = None) -> str:
        """Generate a cache key for the request."""
        cache_data = f"{method}:{url}:{json.dumps(params, sort_keys=True) if params else ''}"
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if a cache entry is still valid."""
        return datetime.now() < cache_entry['expires']
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Make an HTTP request with retry logic and caching.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint (relative to base_url)
            data (Optional[Dict]): Request body data
            params (Optional[Dict]): Query parameters
            use_cache (bool): Whether to use caching for GET requests
        
        Returns:
            Optional[Dict[str, Any]]: Response data if successful, None otherwise
        """
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        # Check cache for GET requests
        if method == 'GET' and use_cache:
            cache_key = self._get_cache_key(method, url, params)
            if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
                print(f"✓ Cache hit for {method} {url}")
                return self.cache[cache_key]['data']
        
        # Rate limiting
        self._wait_for_rate_limit()
        
        # Retry logic
        for attempt in range(self.max_retries + 1):
            try:
                print(f"Making {method} request to {url} (attempt {attempt + 1})")
                
                if method == 'GET':
                    response = self.session.get(url, params=params, timeout=self.timeout)
                elif method == 'POST':
                    response = self.session.post(url, json=data, params=params, timeout=self.timeout)
                elif method == 'PUT':
                    response = self.session.put(url, json=data, params=params, timeout=self.timeout)
                elif method == 'DELETE':
                    response = self.session.delete(url, params=params, timeout=self.timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                
                # Parse response
                if response.status_code == 204:  # No content
                    result = {}
                else:
                    try:
                        result = response.json()
                    except json.JSONDecodeError:
                        result = {'raw_content': response.text}
                
                # Cache GET responses
                if method == 'GET' and use_cache:
                    cache_key = self._get_cache_key(method, url, params)
                    self.cache[cache_key] = {
                        'data': result,
                        'expires': datetime.now() + timedelta(seconds=self.cache_duration)
                    }
                
                print(f"✓ {method} {url} - Status: {response.status_code}")
                return result
                
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response else None
                print(f"✗ HTTP Error {status_code}: {e}")
                
                # Don't retry client errors (4xx)
                if status_code and 400 <= status_code < 500:
                    break
                    
            except (Timeout, ConnectionError) as e:
                print(f"✗ Network Error: {e}")
                
            except Exception as e:
                print(f"✗ Unexpected Error: {e}")
            
            # Wait before retry (exponential backoff)
            if attempt < self.max_retries:
                wait_time = 2 ** attempt
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        print(f"✗ Failed to complete {method} {url} after {self.max_retries + 1} attempts")
        return None
    
    def get(self, endpoint: str, params: Optional[Dict] = None, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Perform a GET request.
        
        Args:
            endpoint (str): API endpoint
            params (Optional[Dict]): Query parameters
            use_cache (bool): Whether to use response caching
        
        Returns:
            Optional[Dict[str, Any]]: Response data
        
        Example:
            >>> client = APIClient("https://jsonplaceholder.typicode.com")
            >>> users = client.get("users")
            >>> user = client.get("users/1")
            >>> posts = client.get("posts", {"userId": 1})
        """
        return self._make_request('GET', endpoint, params=params, use_cache=use_cache)
    
    def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Perform a POST request.
        
        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any]): Request body data
            params (Optional[Dict]): Query parameters
        
        Returns:
            Optional[Dict[str, Any]]: Response data
        
        Example:
            >>> client = APIClient("https://jsonplaceholder.typicode.com")
            >>> new_post = {
            ...     "title": "My New Post",
            ...     "body": "This is the content",
            ...     "userId": 1
            ... }
            >>> result = client.post("posts", new_post)
        """
        return self._make_request('POST', endpoint, data=data, params=params)
    
    def put(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Perform a PUT request.
        
        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any]): Request body data
            params (Optional[Dict]): Query parameters
        
        Returns:
            Optional[Dict[str, Any]]: Response data
        
        Example:
            >>> client = APIClient("https://jsonplaceholder.typicode.com")
            >>> updated_post = {
            ...     "id": 1,
            ...     "title": "Updated Title",
            ...     "body": "Updated content",
            ...     "userId": 1
            ... }
            >>> result = client.put("posts/1", updated_post)
        """
        return self._make_request('PUT', endpoint, data=data, params=params)
    
    def delete(self, endpoint: str, params: Optional[Dict] = None) -> bool:
        """
        Perform a DELETE request.
        
        Args:
            endpoint (str): API endpoint
            params (Optional[Dict]): Query parameters
        
        Returns:
            bool: True if deletion was successful, False otherwise
        
        Example:
            >>> client = APIClient("https://jsonplaceholder.typicode.com")
            >>> success = client.delete("posts/1")
            >>> if success:
            ...     print("Post deleted successfully")
        """
        result = self._make_request('DELETE', endpoint, params=params)
        return result is not None
    
    def get_paginated(self, endpoint: str, page_param: str = 'page',
                     per_page_param: str = 'per_page', per_page: int = 10,
                     max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch all pages of a paginated API endpoint.
        
        Args:
            endpoint (str): API endpoint
            page_param (str): Name of the page parameter
            per_page_param (str): Name of the per-page parameter
            per_page (int): Number of items per page
            max_pages (Optional[int]): Maximum number of pages to fetch
        
        Returns:
            List[Dict[str, Any]]: All items from all pages
        
        Example:
            >>> client = APIClient("https://api.github.com")
            >>> repos = client.get_paginated("user/repos", per_page=50, max_pages=5)
            >>> print(f"Fetched {len(repos)} repositories")
        """
        all_items = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
            
            params = {
                page_param: page,
                per_page_param: per_page
            }
            
            print(f"Fetching page {page}...")
            response = self.get(endpoint, params=params, use_cache=False)
            
            if not response:
                break
            
            # Handle different pagination response formats
            items = []
            if isinstance(response, list):
                items = response
            elif 'data' in response:
                items = response['data']
            elif 'items' in response:
                items = response['items']
            elif 'results' in response:
                items = response['results']
            else:
                # If response is a dict but not in expected format, treat as single item
                items = [response] if response else []
            
            if not items:
                print("No more items found")
                break
            
            all_items.extend(items)
            print(f"✓ Page {page}: {len(items)} items (total: {len(all_items)})")
            
            # Check if we've reached the end
            if len(items) < per_page:
                print("Last page reached")
                break
            
            page += 1
        
        print(f"✓ Pagination complete: {len(all_items)} total items from {page-1} pages")
        return all_items
    
    def clear_cache(self):
        """Clear the response cache."""
        self.cache.clear()
        print("✓ Cache cleared")


class GitHubAPIClient(APIClient):
    """
    Specialized GitHub API client with GitHub-specific methods.
    
    This demonstrates how to extend the base APIClient for specific APIs.
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub API client.
        
        Args:
            token (Optional[str]): GitHub personal access token
        """
        super().__init__("https://api.github.com", auth_token=token)
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json'
        })
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get information about a GitHub user."""
        return self.get(f"users/{username}")
    
    def get_user_repos(self, username: str, repo_type: str = 'all') -> List[Dict[str, Any]]:
        """Get all repositories for a user."""
        params = {'type': repo_type, 'sort': 'updated', 'direction': 'desc'}
        return self.get_paginated(f"users/{username}/repos", 
                                page_param='page', per_page_param='per_page',
                                per_page=100, max_pages=10) or []
    
    def get_repo(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific repository."""
        return self.get(f"repos/{owner}/{repo}")
    
    def get_repo_issues(self, owner: str, repo: str, state: str = 'open') -> List[Dict[str, Any]]:
        """Get issues for a repository."""
        params = {'state': state}
        return self.get_paginated(f"repos/{owner}/{repo}/issues",
                                per_page=100, max_pages=5) or []


def demo_jsonplaceholder_api():
    """
    Demonstrate API usage with JSONPlaceholder (fake REST API for testing).
    
    JSONPlaceholder provides a free fake REST API for testing and prototyping.
    """
    print("=== JSONPlaceholder API Demo ===\n")
    
    # Create API client
    client = APIClient("https://jsonplaceholder.typicode.com")
    
    # GET: Fetch all users
    print("1. Fetching all users:")
    users = client.get("users")
    if users:
        print(f"   ✓ Found {len(users)} users")
        for user in users[:3]:  # Show first 3 users
            print(f"   - {user['name']} ({user['email']})")
        print("   ...")
    print()
    
    # GET: Fetch specific user
    print("2. Fetching specific user:")
    user = client.get("users/1")
    if user:
        print(f"   ✓ User: {user['name']}")
        print(f"   ✓ Email: {user['email']}")
        print(f"   ✓ Website: {user.get('website', 'N/A')}")
    print()
    
    # GET: Fetch posts with parameters
    print("3. Fetching posts for user 1:")
    posts = client.get("posts", {"userId": 1})
    if posts:
        print(f"   ✓ Found {len(posts)} posts")
        for post in posts[:2]:  # Show first 2 posts
            print(f"   - \"{post['title'][:50]}...\"")
    print()
    
    # POST: Create new post
    print("4. Creating new post:")
    new_post = {
        "title": "My Test Post",
        "body": "This is a test post created via API",
        "userId": 1
    }
    created_post = client.post("posts", new_post)
    if created_post:
        print(f"   ✓ Created post with ID: {created_post.get('id')}")
        print(f"   ✓ Title: {created_post.get('title')}")
    print()
    
    # PUT: Update post
    print("5. Updating post:")
    updated_data = {
        "id": 1,
        "title": "Updated Post Title",
        "body": "This post has been updated",
        "userId": 1
    }
    updated_post = client.put("posts/1", updated_data)
    if updated_post:
        print(f"   ✓ Updated post title: {updated_post.get('title')}")
    print()
    
    # DELETE: Delete post
    print("6. Deleting post:")
    delete_success = client.delete("posts/1")
    if delete_success:
        print("   ✓ Post deleted successfully")
    print()
    
    # Demonstrate caching
    print("7. Demonstrating caching:")
    print("   First request (cache miss):")
    start_time = time.time()
    users1 = client.get("users")
    time1 = time.time() - start_time
    
    print("   Second request (cache hit):")
    start_time = time.time()
    users2 = client.get("users")
    time2 = time.time() - start_time
    
    print(f"   ✓ First request: {time1:.3f}s")
    print(f"   ✓ Second request: {time2:.3f}s (cached)")
    print()


def demo_github_api():
    """
    Demonstrate GitHub API usage.
    
    Note: Some endpoints may require authentication for higher rate limits.
    """
    print("=== GitHub API Demo ===\n")
    
    # Create GitHub API client (no token for public data)
    github = GitHubAPIClient()
    
    # Get user information
    print("1. Fetching user information:")
    user_info = github.get_user("octocat")
    if user_info:
        print(f"   ✓ Name: {user_info.get('name', 'N/A')}")
        print(f"   ✓ Public repos: {user_info.get('public_repos', 0)}")
        print(f"   ✓ Followers: {user_info.get('followers', 0)}")
        print(f"   ✓ Created: {user_info.get('created_at', 'N/A')}")
    print()
    
    # Get repository information
    print("2. Fetching repository information:")
    repo_info = github.get_repo("octocat", "Hello-World")
    if repo_info:
        print(f"   ✓ Description: {repo_info.get('description', 'N/A')}")
        print(f"   ✓ Language: {repo_info.get('language', 'N/A')}")
        print(f"   ✓ Stars: {repo_info.get('stargazers_count', 0)}")
        print(f"   ✓ Forks: {repo_info.get('forks_count', 0)}")
    print()
    
    # Get user repositories (limited to prevent rate limiting)
    print("3. Fetching user repositories (first 5):")
    repos = github.get_user_repos("octocat")
    if repos:
        print(f"   ✓ Found {len(repos)} repositories")
        for repo in repos[:5]:  # Show first 5 repos
            print(f"   - {repo['name']} ({repo.get('language', 'Unknown')})")
            print(f"     Stars: {repo.get('stargazers_count', 0)}, "
                  f"Updated: {repo.get('updated_at', 'N/A')[:10]}")
    print()


def main():
    """
    Main demonstration function showing various API client capabilities.
    """
    print("=== REST API Client Examples ===\n")
    
    try:
        # Demo with JSONPlaceholder API (always available)
        demo_jsonplaceholder_api()
        
        # Demo with GitHub API (may have rate limits)
        demo_github_api()
        
    except KeyboardInterrupt:
        print("\n✗ Demo interrupted by user")
    except Exception as e:
        print(f"\n✗ Demo error: {e}")
    
    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()