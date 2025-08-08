"""
HTML Parser Example

This module demonstrates HTML parsing and web scraping techniques using BeautifulSoup.
It covers extracting text, links, images, tables, forms, and structured data from HTML.

Features:
- Parse HTML from strings, files, or URLs
- Extract text content and metadata
- Find and extract links and images
- Parse tables into structured data
- Extract form information
- Handle different HTML encodings
- Clean and normalize extracted data

Requirements:
    pip install beautifulsoup4 requests lxml

Usage Examples:
    # Parse HTML from URL
    parser = HTMLParser()
    soup = parser.fetch_and_parse("https://example.com")
    
    # Extract all links
    links = parser.extract_links(soup)
    
    # Parse table data
    tables = parser.extract_tables(soup)
    
    # Extract structured data
    articles = parser.extract_articles(soup)

Author: Python Learning Examples
Date: August 2025
"""

import requests
import re
import csv
import json
from bs4 import BeautifulSoup, Comment
from typing import Dict, List, Any, Optional, Union, Tuple
from urllib.parse import urljoin, urlparse, parse_qs
from requests.exceptions import RequestException
from datetime import datetime


class HTMLParser:
    """
    A comprehensive HTML parser for web scraping and content extraction.
    
    This class provides methods to parse HTML content and extract various
    types of information including text, links, images, tables, and metadata.
    """
    
    def __init__(self, parser: str = 'lxml', user_agent: Optional[str] = None):
        """
        Initialize the HTML parser.
        
        Args:
            parser (str): Parser to use ('lxml', 'html.parser', 'html5lib')
            user_agent (Optional[str]): Custom user agent string
        """
        self.parser = parser
        self.session = requests.Session()
        
        if user_agent:
            self.session.headers.update({'User-Agent': user_agent})
        else:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
    
    def fetch_and_parse(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        Fetch HTML content from URL and parse it.
        
        Args:
            url (str): URL to fetch and parse
            timeout (int): Request timeout in seconds
        
        Returns:
            Optional[BeautifulSoup]: Parsed HTML soup object, None if failed
        
        Example:
            >>> parser = HTMLParser()
            >>> soup = parser.fetch_and_parse("https://example.com")
            >>> if soup:
            ...     print(soup.title.text)
        """
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Detect encoding
            encoding = response.encoding or 'utf-8'
            print(f"✓ Fetched {len(response.content)} bytes (encoding: {encoding})")
            
            # Parse HTML
            soup = BeautifulSoup(response.content, self.parser)
            print(f"✓ Parsed HTML successfully")
            
            return soup
            
        except RequestException as e:
            print(f"✗ Request Error: {e}")
        except Exception as e:
            print(f"✗ Parsing Error: {e}")
        
        return None
    
    def parse_html_string(self, html_content: str) -> BeautifulSoup:
        """
        Parse HTML content from string.
        
        Args:
            html_content (str): HTML content to parse
        
        Returns:
            BeautifulSoup: Parsed HTML soup object
        
        Example:
            >>> parser = HTMLParser()
            >>> html = "<html><head><title>Test</title></head><body><h1>Hello</h1></body></html>"
            >>> soup = parser.parse_html_string(html)
            >>> print(soup.h1.text)
            Hello
        """
        return BeautifulSoup(html_content, self.parser)
    
    def extract_text(self, soup: BeautifulSoup, clean: bool = True) -> str:
        """
        Extract all text content from HTML.
        
        Args:
            soup (BeautifulSoup): Parsed HTML soup object
            clean (bool): Whether to clean and normalize the text
        
        Returns:
            str: Extracted text content
        
        Example:
            >>> soup = parser.fetch_and_parse("https://example.com")
            >>> text = parser.extract_text(soup)
            >>> print(text[:100])
        """
        # Remove script and style elements
        for script in soup(["script", "style", "noscript"]):
            script.decompose()
        
        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        # Get text
        text = soup.get_text()
        
        if clean:
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_links(self, soup: BeautifulSoup, base_url: Optional[str] = None,
                     internal_only: bool = False) -> List[Dict[str, str]]:
        """
        Extract all links from HTML.
        
        Args:
            soup (BeautifulSoup): Parsed HTML soup object
            base_url (Optional[str]): Base URL for resolving relative links
            internal_only (bool): Only return internal links (same domain)
        
        Returns:
            List[Dict[str, str]]: List of link dictionaries with 'url', 'text', 'title'
        
        Example:
            >>> soup = parser.fetch_and_parse("https://example.com")
            >>> links = parser.extract_links(soup, "https://example.com", internal_only=True)
            >>> for link in links[:5]:
            ...     print(f"{link['text']}: {link['url']}")
        """
        links = []
        base_domain = urlparse(base_url).netloc if base_url else None
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].strip()
            
            # Skip empty links and anchors
            if not href or href.startswith('#'):
                continue
            
            # Resolve relative URLs
            if base_url:
                href = urljoin(base_url, href)
            
            # Filter internal links if requested
            if internal_only and base_domain:
                link_domain = urlparse(href).netloc
                if link_domain != base_domain:
                    continue
            
            link_info = {
                'url': href,
                'text': a_tag.get_text(strip=True),
                'title': a_tag.get('title', ''),
                'target': a_tag.get('target', ''),
                'rel': a_tag.get('rel', [])
            }
            
            links.append(link_info)
        
        print(f"✓ Extracted {len(links)} links")
        return links
    
    def extract_images(self, soup: BeautifulSoup, base_url: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Extract all images from HTML.
        
        Args:
            soup (BeautifulSoup): Parsed HTML soup object
            base_url (Optional[str]): Base URL for resolving relative URLs
        
        Returns:
            List[Dict[str, str]]: List of image dictionaries with src, alt, title, etc.
        
        Example:
            >>> soup = parser.fetch_and_parse("https://example.com")
            >>> images = parser.extract_images(soup, "https://example.com")
            >>> for img in images:
            ...     print(f"{img['alt']}: {img['src']}")
        """
        images = []
        
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src', '').strip()
            
            if not src:
                continue
            
            # Resolve relative URLs
            if base_url:
                src = urljoin(base_url, src)
            
            img_info = {
                'src': src,
                'alt': img_tag.get('alt', ''),
                'title': img_tag.get('title', ''),
                'width': img_tag.get('width', ''),
                'height': img_tag.get('height', ''),
                'class': img_tag.get('class', [])
            }
            
            images.append(img_info)
        
        print(f"✓ Extracted {len(images)} images")
        return images
    
    def extract_tables(self, soup: BeautifulSoup) -> List[List[List[str]]]:
        """
        Extract table data from HTML.
        
        Args:
            soup (BeautifulSoup): Parsed HTML soup object
        
        Returns:
            List[List[List[str]]]: List of tables, each table is a list of rows,
                                   each row is a list of cell values
        
        Example:
            >>> soup = parser.fetch_and_parse("https://example.com")
            >>> tables = parser.extract_tables(soup)
            >>> for i, table in enumerate(tables):
            ...     print(f"Table {i+1}: {len(table)} rows, {len(table[0]) if table else 0} columns")
        """
        tables = []
        
        for table_tag in soup.find_all('table'):
            table_data = []
            
            # Extract rows
            for row in table_tag.find_all('tr'):
                row_data = []
                
                # Extract cells (both th and td)
                for cell in row.find_all(['th', 'td']):
                    cell_text = cell.get_text(strip=True)
                    row_data.append(cell_text)
                
                if row_data:  # Only add non-empty rows
                    table_data.append(row_data)
            
            if table_data:  # Only add non-empty tables
                tables.append(table_data)
        
        print(f"✓ Extracted {len(tables)} tables")
        return tables
    
    def extract_forms(self, soup: BeautifulSoup, base_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Extract form information from HTML.
        
        Args:
            soup (BeautifulSoup): Parsed HTML soup object
            base_url (Optional[str]): Base URL for resolving relative action URLs
        
        Returns:
            List[Dict[str, Any]]: List of form dictionaries with action, method, fields
        
        Example:
            >>> soup = parser.fetch_and_parse("https://example.com")
            >>> forms = parser.extract_forms(soup, "https://example.com")
            >>> for form in forms:
            ...     print(f"Form: {form['action']} ({form['method']})")
            ...     for field in form['fields']:
            ...         print(f"  - {field['name']}: {field['type']}")
        """
        forms = []
        
        for form_tag in soup.find_all('form'):
            action = form_tag.get('action', '').strip()
            method = form_tag.get('method', 'get').lower()
            
            # Resolve relative URLs
            if base_url and action:
                action = urljoin(base_url, action)
            
            # Extract form fields
            fields = []
            
            # Input fields
            for input_tag in form_tag.find_all('input'):
                field_info = {
                    'type': input_tag.get('type', 'text'),
                    'name': input_tag.get('name', ''),
                    'value': input_tag.get('value', ''),
                    'placeholder': input_tag.get('placeholder', ''),
                    'required': input_tag.has_attr('required')
                }
                fields.append(field_info)
            
            # Select fields
            for select_tag in form_tag.find_all('select'):
                options = [option.get('value', option.text) for option in select_tag.find_all('option')]
                field_info = {
                    'type': 'select',
                    'name': select_tag.get('name', ''),
                    'options': options,
                    'required': select_tag.has_attr('required')
                }
                fields.append(field_info)
            
            # Textarea fields
            for textarea_tag in form_tag.find_all('textarea'):
                field_info = {
                    'type': 'textarea',
                    'name': textarea_tag.get('name', ''),
                    'value': textarea_tag.text.strip(),
                    'placeholder': textarea_tag.get('placeholder', ''),
                    'required': textarea_tag.has_attr('required')
                }
                fields.append(field_info)
            
            form_info = {
                'action': action,
                'method': method,
                'fields': fields,
                'enctype': form_tag.get('enctype', 'application/x-www-form-urlencoded')
            }
            
            forms.append(form_info)
        
        print(f"✓ Extracted {len(forms)} forms")
        return forms
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract metadata from HTML head section.
        
        Args:
            soup (BeautifulSoup): Parsed HTML soup object
        
        Returns:
            Dict[str, Any]: Dictionary containing title, meta tags, and other metadata
        
        Example:
            >>> soup = parser.fetch_and_parse("https://example.com")
            >>> metadata = parser.extract_metadata(soup)
            >>> print(f"Title: {metadata.get('title', 'N/A')}")
            >>> print(f"Description: {metadata.get('description', 'N/A')}")
        """
        metadata = {}
        
        # Title
        title_tag = soup.find('title')
        metadata['title'] = title_tag.get_text(strip=True) if title_tag else ''
        
        # Meta tags
        meta_tags = {}
        for meta in soup.find_all('meta'):
            # Standard meta tags
            if meta.get('name'):
                meta_tags[meta['name']] = meta.get('content', '')
            # Property meta tags (Open Graph, etc.)
            elif meta.get('property'):
                meta_tags[meta['property']] = meta.get('content', '')
            # HTTP-equiv meta tags
            elif meta.get('http-equiv'):
                meta_tags[meta['http-equiv']] = meta.get('content', '')
        
        metadata['meta'] = meta_tags
        
        # Common metadata fields
        metadata['description'] = meta_tags.get('description', '')
        metadata['keywords'] = meta_tags.get('keywords', '')
        metadata['author'] = meta_tags.get('author', '')
        metadata['robots'] = meta_tags.get('robots', '')
        
        # Open Graph metadata
        og_data = {}
        for key, value in meta_tags.items():
            if key.startswith('og:'):
                og_data[key[3:]] = value
        metadata['open_graph'] = og_data
        
        # Twitter Card metadata
        twitter_data = {}
        for key, value in meta_tags.items():
            if key.startswith('twitter:'):
                twitter_data[key[8:]] = value
        metadata['twitter'] = twitter_data
        
        # Link tags
        links = {}
        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            href = link.get('href', '')
            
            if isinstance(rel, list):
                for r in rel:
                    links[r] = href
            else:
                links[rel] = href
        
        metadata['links'] = links
        
        print(f"✓ Extracted metadata with {len(meta_tags)} meta tags")
        return metadata
    
    def extract_articles(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract article-like content from HTML using common patterns.
        
        Args:
            soup (BeautifulSoup): Parsed HTML soup object
        
        Returns:
            List[Dict[str, Any]]: List of article dictionaries
        
        Example:
            >>> soup = parser.fetch_and_parse("https://news-site.com")
            >>> articles = parser.extract_articles(soup)
            >>> for article in articles:
            ...     print(f"{article['title']}: {article['summary'][:100]}...")
        """
        articles = []
        
        # Common article selectors
        article_selectors = [
            'article',
            '.article',
            '.post',
            '.entry',
            '.news-item',
            '.story',
            '[itemtype*="Article"]'
        ]
        
        for selector in article_selectors:
            for element in soup.select(selector):
                # Extract title
                title = ''
                title_selectors = ['h1', 'h2', 'h3', '.title', '.headline', '.entry-title']
                for title_sel in title_selectors:
                    title_elem = element.select_one(title_sel)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        break
                
                # Extract content/summary
                content = ''
                content_selectors = ['.content', '.entry-content', '.post-content', 'p']
                for content_sel in content_selectors:
                    content_elem = element.select_one(content_sel)
                    if content_elem:
                        content = content_elem.get_text(strip=True)
                        break
                
                # Extract date
                date = ''
                date_selectors = ['time', '.date', '.published', '.post-date']
                for date_sel in date_selectors:
                    date_elem = element.select_one(date_sel)
                    if date_elem:
                        date = date_elem.get('datetime', date_elem.get_text(strip=True))
                        break
                
                # Extract author
                author = ''
                author_selectors = ['.author', '.by', '.byline', '[rel="author"]']
                for author_sel in author_selectors:
                    author_elem = element.select_one(author_sel)
                    if author_elem:
                        author = author_elem.get_text(strip=True)
                        break
                
                # Extract link
                link = ''
                link_elem = element.select_one('a')
                if link_elem and link_elem.get('href'):
                    link = link_elem['href']
                
                if title or content:  # Only add if we found some content
                    article_info = {
                        'title': title,
                        'content': content,
                        'summary': content[:200] + '...' if len(content) > 200 else content,
                        'date': date,
                        'author': author,
                        'link': link
                    }
                    articles.append(article_info)
        
        print(f"✓ Extracted {len(articles)} articles")
        return articles
    
    def save_to_csv(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """
        Save extracted data to CSV file.
        
        Args:
            data (List[Dict[str, Any]]): List of dictionaries to save
            filename (str): Output CSV filename
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> links = parser.extract_links(soup)
            >>> parser.save_to_csv(links, "extracted_links.csv")
        """
        try:
            if not data:
                print("✗ No data to save")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for row in data:
                    # Handle lists in CSV (convert to string)
                    cleaned_row = {}
                    for key, value in row.items():
                        if isinstance(value, list):
                            cleaned_row[key] = ', '.join(str(v) for v in value)
                        else:
                            cleaned_row[key] = str(value)
                    writer.writerow(cleaned_row)
            
            print(f"✓ Saved {len(data)} records to {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving CSV: {e}")
            return False
    
    def save_to_json(self, data: Any, filename: str) -> bool:
        """
        Save extracted data to JSON file.
        
        Args:
            data (Any): Data to save (usually dict or list)
            filename (str): Output JSON filename
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> metadata = parser.extract_metadata(soup)
            >>> parser.save_to_json(metadata, "page_metadata.json")
        """
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False, default=str)
            
            print(f"✓ Saved data to {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving JSON: {e}")
            return False


def demo_basic_parsing():
    """Demonstrate basic HTML parsing capabilities."""
    print("=== Basic HTML Parsing Demo ===\n")
    
    parser = HTMLParser()
    
    # Example HTML content
    sample_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Page</title>
        <meta name="description" content="This is a sample page for demonstration">
        <meta name="author" content="Python Examples">
    </head>
    <body>
        <header>
            <h1>Welcome to Our Sample Site</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/contact">Contact</a>
            </nav>
        </header>
        
        <main>
            <article>
                <h2>First Article</h2>
                <p>This is the content of the first article. It contains some interesting information.</p>
                <img src="image1.jpg" alt="Sample image" width="300">
            </article>
            
            <article>
                <h2>Second Article</h2>
                <p>This is another article with different content and more details.</p>
            </article>
            
            <table>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>City</th>
                </tr>
                <tr>
                    <td>John</td>
                    <td>25</td>
                    <td>New York</td>
                </tr>
                <tr>
                    <td>Jane</td>
                    <td>30</td>
                    <td>London</td>
                </tr>
            </table>
            
            <form action="/submit" method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="email" name="email" placeholder="Email" required>
                <select name="country">
                    <option value="us">United States</option>
                    <option value="uk">United Kingdom</option>
                </select>
                <button type="submit">Submit</button>
            </form>
        </main>
    </body>
    </html>
    '''
    
    print("1. Parsing HTML content:")
    soup = parser.parse_html_string(sample_html)
    print(f"   ✓ Title: {soup.title.text}")
    print()
    
    print("2. Extracting text content:")
    text = parser.extract_text(soup)
    print(f"   ✓ Extracted {len(text)} characters")
    print(f"   ✓ First 100 chars: {text[:100]}...")
    print()
    
    print("3. Extracting links:")
    links = parser.extract_links(soup)
    for link in links:
        print(f"   - {link['text']}: {link['url']}")
    print()
    
    print("4. Extracting images:")
    images = parser.extract_images(soup)
    for img in images:
        print(f"   - {img['alt']}: {img['src']} ({img['width']}px)")
    print()
    
    print("5. Extracting tables:")
    tables = parser.extract_tables(soup)
    for i, table in enumerate(tables):
        print(f"   Table {i+1}: {len(table)} rows")
        for j, row in enumerate(table):
            print(f"     Row {j+1}: {row}")
    print()
    
    print("6. Extracting forms:")
    forms = parser.extract_forms(soup)
    for form in forms:
        print(f"   Form: {form['action']} ({form['method']})")
        for field in form['fields']:
            print(f"     - {field['name']}: {field['type']}")
    print()
    
    print("7. Extracting metadata:")
    metadata = parser.extract_metadata(soup)
    print(f"   ✓ Title: {metadata['title']}")
    print(f"   ✓ Description: {metadata['description']}")
    print(f"   ✓ Author: {metadata['author']}")
    print()


def demo_real_website():
    """Demonstrate parsing a real website."""
    print("=== Real Website Parsing Demo ===\n")
    
    parser = HTMLParser()
    
    # Parse a simple, reliable website
    print("1. Fetching and parsing example.com:")
    soup = parser.fetch_and_parse("https://example.com")
    
    if soup:
        print("\n2. Extracting metadata:")
        metadata = parser.extract_metadata(soup)
        print(f"   ✓ Title: {metadata['title']}")
        print(f"   ✓ Description: {metadata.get('description', 'N/A')}")
        
        print("\n3. Extracting text content:")
        text = parser.extract_text(soup)
        print(f"   ✓ Text length: {len(text)} characters")
        print(f"   ✓ Preview: {text[:200]}...")
        
        print("\n4. Extracting links:")
        links = parser.extract_links(soup, "https://example.com")
        if links:
            for link in links[:5]:  # Show first 5 links
                print(f"   - {link['text'][:30]}...: {link['url']}")
        else:
            print("   No links found")
        
        print("\n5. Saving extracted data:")
        # Save metadata to JSON
        parser.save_to_json(metadata, "example_metadata.json")
        
        # Save links to CSV if any exist
        if links:
            parser.save_to_csv(links, "example_links.csv")
    else:
        print("✗ Failed to fetch website")
    
    print()


def main():
    """
    Main demonstration function showing HTML parsing capabilities.
    """
    print("=== HTML Parser Examples ===\n")
    
    try:
        # Demo with sample HTML
        demo_basic_parsing()
        
        # Demo with real website (if network available)
        demo_real_website()
        
    except KeyboardInterrupt:
        print("\n✗ Demo interrupted by user")
    except Exception as e:
        print(f"\n✗ Demo error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()