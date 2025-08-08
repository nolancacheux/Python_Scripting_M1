"""
File Writer Module - Comprehensive File Writing Examples

This module demonstrates various file writing operations including:
- Writing text files
- Appending to files
- Writing with different encodings
- Atomic file writing (safe overwrites)
- Backup creation before overwriting
- Error handling for write operations

Author: Python Learning Module
Date: 2025-08-08
"""

import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime


def write_text_file(file_path, content, encoding='utf-8', create_backup=False):
    """
    Write content to a text file, optionally creating a backup.
    
    Args:
        file_path (str): Path to the output file
        content (str): Content to write
        encoding (str): File encoding (default: utf-8)
        create_backup (bool): Whether to create a backup if file exists
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = write_text_file('output.txt', 'Hello, World!', create_backup=True)
        if success:
            print("File written successfully")
    """
    try:
        # Create backup if requested and file exists
        if create_backup and os.path.exists(file_path):
            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(file_path, backup_path)
            print(f"Backup created: {backup_path}")
        
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(content)
        
        print(f"Successfully wrote {len(content)} characters to '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to write to '{file_path}'.")
        return False
    except OSError as e:
        print(f"Error: Could not write to '{file_path}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing to '{file_path}': {e}")
        return False


def append_to_file(file_path, content, encoding='utf-8', add_newline=True):
    """
    Append content to a text file.
    
    Args:
        file_path (str): Path to the file
        content (str): Content to append
        encoding (str): File encoding (default: utf-8)
        add_newline (bool): Whether to add a newline before content
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = append_to_file('log.txt', 'New log entry', add_newline=True)
        if success:
            print("Content appended successfully")
    """
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'a', encoding=encoding) as file:
            if add_newline and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                file.write('\n')
            file.write(content)
        
        print(f"Successfully appended {len(content)} characters to '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to append to '{file_path}'.")
        return False
    except OSError as e:
        print(f"Error: Could not append to '{file_path}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error appending to '{file_path}': {e}")
        return False


def write_lines_to_file(file_path, lines, encoding='utf-8', line_ending='\n'):
    """
    Write a list of lines to a file.
    
    Args:
        file_path (str): Path to the output file
        lines (list): List of strings to write as lines
        encoding (str): File encoding (default: utf-8)
        line_ending (str): Line ending character(s) (default: \\n)
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        lines = ['First line', 'Second line', 'Third line']
        success = write_lines_to_file('output.txt', lines)
    """
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as file:
            for i, line in enumerate(lines):
                file.write(line)
                if i < len(lines) - 1:  # Don't add line ending after last line
                    file.write(line_ending)
        
        print(f"Successfully wrote {len(lines)} lines to '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to write to '{file_path}'.")
        return False
    except OSError as e:
        print(f"Error: Could not write to '{file_path}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing lines to '{file_path}': {e}")
        return False


def write_file_atomic(file_path, content, encoding='utf-8'):
    """
    Write to a file atomically using a temporary file and rename operation.
    This prevents corruption if the write operation is interrupted.
    
    Args:
        file_path (str): Path to the output file
        content (str): Content to write
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = write_file_atomic('important.txt', 'Critical data')
        if success:
            print("File written atomically")
    """
    try:
        # Create directory if it doesn't exist
        directory = Path(file_path).parent
        directory.mkdir(parents=True, exist_ok=True)
        
        # Create temporary file in the same directory
        with tempfile.NamedTemporaryFile(mode='w', encoding=encoding, 
                                       dir=directory, delete=False) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Atomically move the temporary file to the target location
        shutil.move(temp_path, file_path)
        
        print(f"Successfully wrote {len(content)} characters atomically to '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to write to '{file_path}'.")
        # Clean up temporary file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        return False
    except OSError as e:
        print(f"Error: Could not write atomically to '{file_path}': {e}")
        # Clean up temporary file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        return False
    except Exception as e:
        print(f"Unexpected error writing atomically to '{file_path}': {e}")
        # Clean up temporary file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        return False


def write_with_timestamp(file_path, content, encoding='utf-8'):
    """
    Write content to a file with timestamp prefix.
    
    Args:
        file_path (str): Path to the output file
        content (str): Content to write
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = write_with_timestamp('log.txt', 'Application started')
    """
    timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
    timestamped_content = timestamp + content
    
    return write_text_file(file_path, timestamped_content, encoding)


def append_with_timestamp(file_path, content, encoding='utf-8'):
    """
    Append content to a file with timestamp prefix.
    
    Args:
        file_path (str): Path to the file
        content (str): Content to append
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = append_with_timestamp('log.txt', 'User logged in')
    """
    timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
    timestamped_content = timestamp + content
    
    return append_to_file(file_path, timestamped_content, encoding)


def write_multiline_content(file_path, content_dict, encoding='utf-8'):
    """
    Write structured multiline content to a file.
    
    Args:
        file_path (str): Path to the output file
        content_dict (dict): Dictionary with sections and content
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        content = {
            'Header': 'Configuration File',
            'Database': 'host=localhost\nport=5432',
            'Cache': 'redis_host=127.0.0.1\nredis_port=6379'
        }
        success = write_multiline_content('config.txt', content)
    """
    try:
        lines = []
        for section, content in content_dict.items():
            lines.append(f"[{section}]")
            lines.append(content)
            lines.append("")  # Empty line between sections
        
        # Remove the last empty line
        if lines and lines[-1] == "":
            lines.pop()
        
        content_text = '\n'.join(lines)
        return write_text_file(file_path, content_text, encoding)
    
    except Exception as e:
        print(f"Error creating multiline content: {e}")
        return False


def safe_overwrite(file_path, content, encoding='utf-8', confirm=True):
    """
    Safely overwrite a file with user confirmation and backup.
    
    Args:
        file_path (str): Path to the file
        content (str): New content
        encoding (str): File encoding (default: utf-8)
        confirm (bool): Whether to ask for confirmation if file exists
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = safe_overwrite('important.txt', 'New content', confirm=True)
    """
    try:
        if os.path.exists(file_path):
            if confirm:
                response = input(f"File '{file_path}' exists. Overwrite? (y/N): ").lower()
                if response != 'y' and response != 'yes':
                    print("Operation cancelled.")
                    return False
            
            # Create backup
            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(file_path, backup_path)
            print(f"Backup created: {backup_path}")
        
        return write_file_atomic(file_path, content, encoding)
    
    except Exception as e:
        print(f"Error in safe overwrite: {e}")
        return False


def write_binary_file(file_path, data):
    """
    Write binary data to a file.
    
    Args:
        file_path (str): Path to the output file
        data (bytes): Binary data to write
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        binary_data = b'\\x00\\x01\\x02\\x03'
        success = write_binary_file('data.bin', binary_data)
    """
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'wb') as file:
            file.write(data)
        
        print(f"Successfully wrote {len(data)} bytes to '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to write to '{file_path}'.")
        return False
    except OSError as e:
        print(f"Error: Could not write to '{file_path}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing binary data to '{file_path}': {e}")
        return False


def create_log_entry(log_file, level, message, encoding='utf-8'):
    """
    Create a formatted log entry and append it to a log file.
    
    Args:
        log_file (str): Path to the log file
        level (str): Log level (INFO, WARNING, ERROR, etc.)
        message (str): Log message
        encoding (str): File encoding (default: utf-8)
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = create_log_entry('app.log', 'INFO', 'Application started')
        success = create_log_entry('app.log', 'ERROR', 'Database connection failed')
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {level.upper()}: {message}"
    
    return append_to_file(log_file, log_entry, encoding, add_newline=True)


def main():
    """
    Demonstration of file writing functions.
    Run this script to see examples of all file writing operations.
    """
    print("=== File Writer Module Demonstration ===\n")
    
    # Create a demo directory
    demo_dir = "file_writer_demo"
    os.makedirs(demo_dir, exist_ok=True)
    
    # 1. Basic text file writing
    print("1. Writing basic text file:")
    content = "Hello, World!\nThis is a demonstration of file writing in Python."
    success = write_text_file(f"{demo_dir}/basic.txt", content)
    print(f"   Success: {success}\n")
    
    # 2. Appending to file
    print("2. Appending to file:")
    append_content = "This line was appended to the file."
    success = append_to_file(f"{demo_dir}/basic.txt", append_content)
    print(f"   Success: {success}\n")
    
    # 3. Writing lines
    print("3. Writing lines to file:")
    lines = ["Line 1: Introduction", "Line 2: Main content", "Line 3: Conclusion"]
    success = write_lines_to_file(f"{demo_dir}/lines.txt", lines)
    print(f"   Success: {success}\n")
    
    # 4. Atomic writing
    print("4. Atomic file writing:")
    critical_data = "This is critical data that must not be corrupted during writing."
    success = write_file_atomic(f"{demo_dir}/atomic.txt", critical_data)
    print(f"   Success: {success}\n")
    
    # 5. Timestamped writing
    print("5. Writing with timestamp:")
    success = write_with_timestamp(f"{demo_dir}/timestamped.txt", "Application started")
    print(f"   Success: {success}\n")
    
    # 6. Structured content
    print("6. Writing structured content:")
    config_content = {
        "Database": "host=localhost\nport=5432\nname=myapp",
        "Cache": "redis_host=127.0.0.1\nredis_port=6379",
        "Logging": "level=INFO\nfile=app.log"
    }
    success = write_multiline_content(f"{demo_dir}/config.txt", config_content)
    print(f"   Success: {success}\n")
    
    # 7. Log entries
    print("7. Creating log entries:")
    log_file = f"{demo_dir}/app.log"
    create_log_entry(log_file, "INFO", "Application started")
    create_log_entry(log_file, "WARNING", "Low memory detected")
    create_log_entry(log_file, "ERROR", "Database connection failed")
    print("   Log entries created\n")
    
    # 8. Binary file writing
    print("8. Writing binary data:")
    binary_data = bytes([0, 1, 2, 3, 255, 254, 253, 252])
    success = write_binary_file(f"{demo_dir}/binary.dat", binary_data)
    print(f"   Success: {success}\n")
    
    # Display created files
    print("Created files:")
    for file_path in Path(demo_dir).glob("*"):
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"   {file_path.name}: {size} bytes")
    
    print(f"\nAll demo files created in '{demo_dir}' directory.")
    print("You can examine these files to see the results of different writing operations.")


if __name__ == "__main__":
    main()