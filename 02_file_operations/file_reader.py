"""
File Reader Module - Comprehensive File Reading Examples

This module demonstrates various file reading operations including:
- Reading text files
- Reading CSV files
- Reading JSON files
- Handling different encodings
- Error handling for file operations

Author: Python Learning Module
Date: 2025-08-08
"""

import os
import csv
import json
import sys
from pathlib import Path


def read_text_file(file_path, encoding='utf-8'):
    """
    Read a text file and return its contents as a string.
    
    Args:
        file_path (str): Path to the text file
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        str: File contents or None if error occurred
    
    Example:
        content = read_text_file('sample.txt')
        if content:
            print(content)
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
            print(f"Successfully read {len(content)} characters from {file_path}")
            return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
        return None
    except UnicodeDecodeError:
        print(f"Error: Could not decode file '{file_path}' with encoding '{encoding}'.")
        print("Try a different encoding like 'latin-1' or 'cp1252'.")
        return None
    except Exception as e:
        print(f"Unexpected error reading file '{file_path}': {e}")
        return None


def read_text_file_lines(file_path, encoding='utf-8', strip_whitespace=True):
    """
    Read a text file and return its contents as a list of lines.
    
    Args:
        file_path (str): Path to the text file
        encoding (str): File encoding (default: utf-8)
        strip_whitespace (bool): Whether to strip whitespace from lines
    
    Returns:
        list: List of lines or None if error occurred
    
    Example:
        lines = read_text_file_lines('data.txt')
        for i, line in enumerate(lines, 1):
            print(f"Line {i}: {line}")
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            if strip_whitespace:
                lines = [line.strip() for line in file.readlines()]
            else:
                lines = file.readlines()
            print(f"Successfully read {len(lines)} lines from {file_path}")
            return lines
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
        return None
    except UnicodeDecodeError:
        print(f"Error: Could not decode file '{file_path}' with encoding '{encoding}'.")
        return None
    except Exception as e:
        print(f"Unexpected error reading file '{file_path}': {e}")
        return None


def read_csv_file(file_path, delimiter=',', encoding='utf-8'):
    """
    Read a CSV file and return its contents as a list of dictionaries.
    
    Args:
        file_path (str): Path to the CSV file
        delimiter (str): CSV delimiter (default: comma)
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        list: List of dictionaries representing CSV rows or None if error
    
    Example:
        data = read_csv_file('employees.csv')
        if data:
            for row in data:
                print(f"Name: {row['name']}, Age: {row['age']}")
    """
    try:
        data = []
        with open(file_path, 'r', encoding=encoding, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                data.append(dict(row))
            print(f"Successfully read {len(data)} rows from CSV file '{file_path}'")
            return data
    except FileNotFoundError:
        print(f"Error: CSV file '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read CSV file '{file_path}'.")
        return None
    except csv.Error as e:
        print(f"Error reading CSV file '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading CSV file '{file_path}': {e}")
        return None


def read_csv_file_as_list(file_path, delimiter=',', encoding='utf-8', skip_header=True):
    """
    Read a CSV file and return its contents as a list of lists.
    
    Args:
        file_path (str): Path to the CSV file
        delimiter (str): CSV delimiter (default: comma)
        encoding (str): File encoding (default: utf-8)
        skip_header (bool): Whether to skip the header row
    
    Returns:
        list: List of lists representing CSV rows or None if error
    
    Example:
        data = read_csv_file_as_list('data.csv')
        if data:
            for row in data:
                print(row)
    """
    try:
        data = []
        with open(file_path, 'r', encoding=encoding, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            if skip_header:
                next(reader, None)  # Skip header row
            for row in reader:
                data.append(row)
            print(f"Successfully read {len(data)} rows from CSV file '{file_path}'")
            return data
    except FileNotFoundError:
        print(f"Error: CSV file '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read CSV file '{file_path}'.")
        return None
    except csv.Error as e:
        print(f"Error reading CSV file '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading CSV file '{file_path}': {e}")
        return None


def read_json_file(file_path, encoding='utf-8'):
    """
    Read a JSON file and return its contents as a Python object.
    
    Args:
        file_path (str): Path to the JSON file
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        dict/list: Parsed JSON data or None if error occurred
    
    Example:
        data = read_json_file('config.json')
        if data:
            print(f"Database host: {data['database']['host']}")
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            data = json.load(file)
            print(f"Successfully loaded JSON data from '{file_path}'")
            return data
    except FileNotFoundError:
        print(f"Error: JSON file '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read JSON file '{file_path}'.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading JSON file '{file_path}': {e}")
        return None


def get_file_info(file_path):
    """
    Get comprehensive information about a file.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        dict: File information or None if file doesn't exist
    
    Example:
        info = get_file_info('document.txt')
        if info:
            print(f"Size: {info['size']} bytes")
            print(f"Modified: {info['modified']}")
    """
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"Error: File '{file_path}' does not exist.")
            return None
        
        stat = path.stat()
        info = {
            'name': path.name,
            'path': str(path.absolute()),
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'created': stat.st_ctime,
            'is_file': path.is_file(),
            'is_directory': path.is_dir(),
            'suffix': path.suffix,
            'parent': str(path.parent)
        }
        
        print(f"File information retrieved for '{file_path}'")
        return info
    except Exception as e:
        print(f"Error getting file info for '{file_path}': {e}")
        return None


def read_file_safely(file_path, max_size_mb=100):
    """
    Safely read a file with size checking to prevent memory issues.
    
    Args:
        file_path (str): Path to the file
        max_size_mb (int): Maximum allowed file size in MB
    
    Returns:
        str: File content or None if file is too large or error occurred
    
    Example:
        content = read_file_safely('large_file.txt', max_size_mb=50)
        if content:
            print("File content loaded successfully")
    """
    try:
        file_size = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if file_size > max_size_bytes:
            print(f"Error: File '{file_path}' is too large ({file_size} bytes). "
                  f"Maximum allowed size is {max_size_mb} MB.")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Successfully read {len(content)} characters from {file_path}")
            return content
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
        return None
    except Exception as e:
        print(f"Unexpected error reading file '{file_path}': {e}")
        return None


def main():
    """
    Demonstration of file reading functions.
    Run this script to see examples of all file reading operations.
    """
    print("=== File Reader Module Demonstration ===\n")
    
    # Create sample files for demonstration
    sample_text = "Hello, World!\nThis is a sample text file.\nPython file operations are powerful!"
    sample_csv = "name,age,city\nJohn,25,New York\nJane,30,Los Angeles\nBob,35,Chicago"
    sample_json = '{"name": "Python Tutorial", "version": "1.0", "topics": ["files", "csv", "json"]}'
    
    # Create sample files
    try:
        with open('sample.txt', 'w') as f:
            f.write(sample_text)
        with open('sample.csv', 'w') as f:
            f.write(sample_csv)
        with open('sample.json', 'w') as f:
            f.write(sample_json)
        print("Sample files created successfully!\n")
    except Exception as e:
        print(f"Error creating sample files: {e}")
        return
    
    # Demonstrate text file reading
    print("1. Reading text file:")
    content = read_text_file('sample.txt')
    if content:
        print(f"Content preview: {content[:50]}...")
    print()
    
    # Demonstrate reading lines
    print("2. Reading text file lines:")
    lines = read_text_file_lines('sample.txt')
    if lines:
        for i, line in enumerate(lines, 1):
            print(f"   Line {i}: {line}")
    print()
    
    # Demonstrate CSV reading
    print("3. Reading CSV file:")
    csv_data = read_csv_file('sample.csv')
    if csv_data:
        for row in csv_data:
            print(f"   {row}")
    print()
    
    # Demonstrate JSON reading
    print("4. Reading JSON file:")
    json_data = read_json_file('sample.json')
    if json_data:
        print(f"   Name: {json_data['name']}")
        print(f"   Topics: {', '.join(json_data['topics'])}")
    print()
    
    # Demonstrate file info
    print("5. Getting file information:")
    info = get_file_info('sample.txt')
    if info:
        print(f"   Name: {info['name']}")
        print(f"   Size: {info['size']} bytes")
        print(f"   Type: {info['suffix']}")
    print()
    
    # Clean up sample files
    try:
        os.remove('sample.txt')
        os.remove('sample.csv')
        os.remove('sample.json')
        print("Sample files cleaned up successfully!")
    except Exception as e:
        print(f"Error cleaning up files: {e}")


if __name__ == "__main__":
    main()