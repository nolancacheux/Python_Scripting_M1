"""
JSON Handler Module - Comprehensive JSON File Operations

This module demonstrates various JSON operations including:
- Reading and parsing JSON files
- Writing and formatting JSON data
- JSON schema validation
- Data manipulation and transformation
- Nested JSON operations
- Error handling for JSON operations
- Converting between JSON and other formats
- JSON streaming for large files

Author: Python Learning Module
Date: 2025-08-08
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
from decimal import Decimal
import tempfile


class DateTimeEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle datetime and date objects.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def read_json_file(file_path, encoding='utf-8'):
    """
    Read and parse a JSON file.
    
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
        print(f"Error: Invalid JSON in file '{file_path}' at line {e.lineno}, column {e.colno}: {e.msg}")
        return None
    except Exception as e:
        print(f"Unexpected error reading JSON file '{file_path}': {e}")
        return None


def write_json_file(data, file_path, indent=2, ensure_ascii=False, encoding='utf-8', sort_keys=False):
    """
    Write data to a JSON file with formatting options.
    
    Args:
        data: Data to write (dict, list, etc.)
        file_path (str): Path to the output JSON file
        indent (int): Number of spaces for indentation (None for compact)
        ensure_ascii (bool): Whether to escape non-ASCII characters
        encoding (str): File encoding
        sort_keys (bool): Whether to sort dictionary keys
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        config = {
            'database': {'host': 'localhost', 'port': 5432},
            'cache': {'enabled': True, 'timeout': 300}
        }
        success = write_json_file(config, 'config.json', indent=4)
    """
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=indent, ensure_ascii=ensure_ascii, 
                     sort_keys=sort_keys, cls=DateTimeEncoder)
        
        print(f"Successfully wrote JSON data to '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to write JSON file '{file_path}'.")
        return False
    except TypeError as e:
        print(f"Error: Data is not JSON serializable: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing JSON file '{file_path}': {e}")
        return False


def pretty_print_json(data, indent=2):
    """
    Pretty print JSON data to console.
    
    Args:
        data: JSON data to print
        indent (int): Number of spaces for indentation
    
    Example:
        pretty_print_json({'name': 'John', 'age': 30})
    """
    try:
        formatted_json = json.dumps(data, indent=indent, ensure_ascii=False, cls=DateTimeEncoder)
        print(formatted_json)
    except TypeError as e:
        print(f"Error: Data is not JSON serializable: {e}")
    except Exception as e:
        print(f"Error pretty printing JSON: {e}")


def validate_json_file(file_path, encoding='utf-8'):
    """
    Validate that a file contains valid JSON.
    
    Args:
        file_path (str): Path to the JSON file
        encoding (str): File encoding
    
    Returns:
        dict: Validation results with status and error details
    
    Example:
        result = validate_json_file('data.json')
        if result['is_valid']:
            print("JSON is valid")
        else:
            print(f"JSON is invalid: {result['error']}")
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            json.load(file)
        
        result = {
            'is_valid': True,
            'error': None,
            'line': None,
            'column': None
        }
        print(f"JSON file '{file_path}' is valid")
        return result
    
    except FileNotFoundError:
        return {
            'is_valid': False,
            'error': f"File '{file_path}' not found",
            'line': None,
            'column': None
        }
    except json.JSONDecodeError as e:
        return {
            'is_valid': False,
            'error': e.msg,
            'line': e.lineno,
            'column': e.colno
        }
    except Exception as e:
        return {
            'is_valid': False,
            'error': str(e),
            'line': None,
            'column': None
        }


def merge_json_objects(*json_objects, deep_merge=True):
    """
    Merge multiple JSON objects into one.
    
    Args:
        *json_objects: Variable number of dictionaries to merge
        deep_merge (bool): Whether to perform deep merge for nested objects
    
    Returns:
        dict: Merged JSON object
    
    Example:
        obj1 = {'a': 1, 'b': {'x': 1}}
        obj2 = {'b': {'y': 2}, 'c': 3}
        merged = merge_json_objects(obj1, obj2, deep_merge=True)
        # Result: {'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 3}
    """
    def deep_merge_dicts(dict1, dict2):
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge_dicts(result[key], value)
            else:
                result[key] = value
        return result
    
    try:
        if not json_objects:
            return {}
        
        result = json_objects[0].copy() if isinstance(json_objects[0], dict) else {}
        
        for json_obj in json_objects[1:]:
            if not isinstance(json_obj, dict):
                print(f"Warning: Skipping non-dictionary object: {type(json_obj)}")
                continue
            
            if deep_merge:
                result = deep_merge_dicts(result, json_obj)
            else:
                result.update(json_obj)
        
        print(f"Successfully merged {len(json_objects)} JSON objects")
        return result
    
    except Exception as e:
        print(f"Error merging JSON objects: {e}")
        return {}


def extract_json_path(data, path, default=None):
    """
    Extract data from JSON using a dot-notation path.
    
    Args:
        data: JSON data (dict or list)
        path (str): Dot-separated path (e.g., 'user.address.city')
        default: Default value if path not found
    
    Returns:
        Any: Value at the specified path or default value
    
    Example:
        data = {'user': {'profile': {'name': 'John', 'age': 30}}}
        name = extract_json_path(data, 'user.profile.name')  # Returns 'John'
        country = extract_json_path(data, 'user.address.country', 'Unknown')  # Returns 'Unknown'
    """
    try:
        current = data
        parts = path.split('.')
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    index = int(part)
                    current = current[index] if 0 <= index < len(current) else None
                except (ValueError, IndexError):
                    current = None
            else:
                current = None
            
            if current is None:
                break
        
        return current if current is not None else default
    
    except Exception as e:
        print(f"Error extracting path '{path}': {e}")
        return default


def set_json_path(data, path, value):
    """
    Set a value in JSON data using a dot-notation path.
    
    Args:
        data (dict): JSON data to modify
        path (str): Dot-separated path
        value: Value to set
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        data = {'user': {'profile': {}}}
        success = set_json_path(data, 'user.profile.name', 'John')
        # data becomes {'user': {'profile': {'name': 'John'}}}
    """
    try:
        if not isinstance(data, dict):
            print("Error: Root data must be a dictionary")
            return False
        
        parts = path.split('.')
        current = data
        
        # Navigate to the parent of the target
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                print(f"Error: Cannot set path '{path}', '{part}' is not a dictionary")
                return False
            current = current[part]
        
        # Set the final value
        current[parts[-1]] = value
        return True
    
    except Exception as e:
        print(f"Error setting path '{path}': {e}")
        return False


def filter_json_data(data, filter_func):
    """
    Filter JSON data based on a custom function.
    
    Args:
        data (list): List of JSON objects to filter
        filter_func (callable): Function that takes an object and returns bool
    
    Returns:
        list: Filtered data
    
    Example:
        users = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
        adults = filter_json_data(users, lambda x: x.get('age', 0) >= 30)
    """
    try:
        if not isinstance(data, list):
            print("Error: Data must be a list for filtering")
            return []
        
        filtered_data = []
        for item in data:
            try:
                if filter_func(item):
                    filtered_data.append(item)
            except Exception as e:
                print(f"Error applying filter to item {item}: {e}")
                continue
        
        print(f"Filtered data: {len(filtered_data)} items from {len(data)} total")
        return filtered_data
    
    except Exception as e:
        print(f"Error filtering JSON data: {e}")
        return []


def transform_json_data(data, transform_func):
    """
    Transform JSON data using a custom function.
    
    Args:
        data (list): List of JSON objects to transform
        transform_func (callable): Function that takes an object and returns transformed object
    
    Returns:
        list: Transformed data
    
    Example:
        users = [{'name': 'john', 'age': 30}]
        normalized = transform_json_data(users, lambda x: {**x, 'name': x['name'].title()})
    """
    try:
        if not isinstance(data, list):
            print("Error: Data must be a list for transformation")
            return []
        
        transformed_data = []
        for item in data:
            try:
                transformed_item = transform_func(item)
                transformed_data.append(transformed_item)
            except Exception as e:
                print(f"Error transforming item {item}: {e}")
                # Keep original item if transformation fails
                transformed_data.append(item)
        
        print(f"Transformed {len(transformed_data)} items")
        return transformed_data
    
    except Exception as e:
        print(f"Error transforming JSON data: {e}")
        return data


def convert_csv_to_json_file(csv_file_path, json_file_path, encoding='utf-8'):
    """
    Convert a CSV file to JSON format.
    
    Args:
        csv_file_path (str): Path to the input CSV file
        json_file_path (str): Path to the output JSON file
        encoding (str): File encoding
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = convert_csv_to_json_file('data.csv', 'data.json')
    """
    try:
        import csv
        
        data = []
        with open(csv_file_path, 'r', encoding=encoding, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert empty strings to None for cleaner JSON
                cleaned_row = {}
                for key, value in row.items():
                    cleaned_row[key] = value if value.strip() else None
                data.append(cleaned_row)
        
        success = write_json_file(data, json_file_path, encoding=encoding)
        if success:
            print(f"Successfully converted CSV to JSON: {len(data)} records")
        return success
    
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")
        return False


def flatten_json(data, separator='_'):
    """
    Flatten nested JSON data into a single level dictionary.
    
    Args:
        data (dict): JSON data to flatten
        separator (str): Separator for nested keys
    
    Returns:
        dict: Flattened JSON data
    
    Example:
        nested = {'user': {'profile': {'name': 'John', 'age': 30}}}
        flat = flatten_json(nested)
        # Result: {'user_profile_name': 'John', 'user_profile_age': 30}
    """
    def _flatten(obj, parent_key='', sep=separator):
        items = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{parent_key}{sep}{key}" if parent_key else key
                items.extend(_flatten(value, new_key, sep).items())
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                items.extend(_flatten(value, new_key, sep).items())
        else:
            return {parent_key: obj}
        return dict(items)
    
    try:
        flattened = _flatten(data)
        print(f"Flattened JSON: {len(flattened)} keys")
        return flattened
    except Exception as e:
        print(f"Error flattening JSON: {e}")
        return {}


def backup_json_file(file_path, backup_dir=None):
    """
    Create a backup of a JSON file with timestamp.
    
    Args:
        file_path (str): Path to the JSON file to backup
        backup_dir (str): Directory for backup (optional)
    
    Returns:
        str: Path to backup file or None if error
    
    Example:
        backup_path = backup_json_file('important_config.json')
        if backup_path:
            print(f"Backup created: {backup_path}")
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return None
        
        # Determine backup directory and filename
        if backup_dir is None:
            backup_dir = os.path.dirname(file_path)
        
        filename = Path(file_path).stem
        extension = Path(file_path).suffix
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{filename}_backup_{timestamp}{extension}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Create backup directory if it doesn't exist
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        import shutil
        shutil.copy2(file_path, backup_path)
        
        print(f"Successfully created backup: '{backup_path}'")
        return backup_path
    
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None


def update_json_file(file_path, updates, create_backup=True, encoding='utf-8'):
    """
    Update a JSON file with new data while preserving existing structure.
    
    Args:
        file_path (str): Path to the JSON file
        updates (dict): Dictionary of updates to apply
        create_backup (bool): Whether to create a backup before updating
        encoding (str): File encoding
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        updates = {'database.port': 5433, 'cache.enabled': False}
        success = update_json_file('config.json', updates)
    """
    try:
        # Read existing data
        existing_data = read_json_file(file_path, encoding)
        if existing_data is None:
            # Create new file with updates
            existing_data = {}
        
        # Create backup if requested
        if create_backup and os.path.exists(file_path):
            backup_path = backup_json_file(file_path)
            if backup_path:
                print(f"Backup created before update")
        
        # Apply updates
        for path, value in updates.items():
            if '.' in path:
                # Handle nested paths
                set_json_path(existing_data, path, value)
            else:
                # Handle top-level keys
                existing_data[path] = value
        
        # Write updated data
        success = write_json_file(existing_data, file_path, encoding=encoding)
        if success:
            print(f"Successfully updated JSON file with {len(updates)} changes")
        return success
    
    except Exception as e:
        print(f"Error updating JSON file: {e}")
        return False


def main():
    """
    Demonstration of JSON handling functions.
    Run this script to see examples of all JSON operations.
    """
    print("=== JSON Handler Module Demonstration ===\n")
    
    # Create demo directory
    demo_dir = "json_handler_demo"
    os.makedirs(demo_dir, exist_ok=True)
    
    # 1. Create sample JSON data
    print("1. Creating sample JSON data:")
    sample_data = {
        "application": {
            "name": "Demo App",
            "version": "1.0.0",
            "release_date": datetime.now(),
            "config": {
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "demo_db",
                    "ssl": True
                },
                "cache": {
                    "enabled": True,
                    "timeout": 300,
                    "redis_host": "127.0.0.1"
                },
                "logging": {
                    "level": "INFO",
                    "file": "app.log",
                    "max_size": "10MB"
                }
            }
        },
        "users": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "profile": {
                    "age": 30,
                    "department": "IT",
                    "active": True
                }
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "profile": {
                    "age": 25,
                    "department": "HR",
                    "active": True
                }
            }
        ],
        "metadata": {
            "created": datetime.now().date(),
            "total_records": 2,
            "schema_version": "2.1"
        }
    }
    
    json_file = f"{demo_dir}/sample_data.json"
    success = write_json_file(sample_data, json_file, indent=2)
    print(f"   Sample JSON file created: {success}\n")
    
    # 2. Read and validate JSON
    print("2. Reading and validating JSON:")
    read_data = read_json_file(json_file)
    if read_data:
        print(f"   Successfully read JSON data")
        print(f"   Application name: {read_data['application']['name']}")
    
    validation_result = validate_json_file(json_file)
    print(f"   JSON validation: {'Valid' if validation_result['is_valid'] else 'Invalid'}\n")
    
    # 3. Extract data using path notation
    print("3. Extracting data using path notation:")
    db_host = extract_json_path(read_data, 'application.config.database.host')
    user_name = extract_json_path(read_data, 'users.0.name')
    missing_value = extract_json_path(read_data, 'application.missing.path', 'Default Value')
    
    print(f"   Database host: {db_host}")
    print(f"   First user name: {user_name}")
    print(f"   Missing value with default: {missing_value}\n")
    
    # 4. Filter JSON data
    print("4. Filtering JSON data:")
    active_users = filter_json_data(read_data['users'], lambda user: user['profile']['active'])
    print(f"   Active users: {len(active_users)}")
    for user in active_users:
        print(f"     {user['name']} - {user['profile']['department']}")
    print()
    
    # 5. Transform JSON data
    print("5. Transforming JSON data:")
    transformed_users = transform_json_data(
        read_data['users'], 
        lambda user: {
            **user,
            'display_name': f"{user['name']} ({user['profile']['department']})",
            'profile': {
                **user['profile'],
                'age_group': 'Young' if user['profile']['age'] < 30 else 'Experienced'
            }
        }
    )
    print("   Transformed users:")
    for user in transformed_users:
        print(f"     {user['display_name']} - Age group: {user['profile']['age_group']}")
    print()
    
    # 6. Flatten nested JSON
    print("6. Flattening nested JSON:")
    config_data = read_data['application']['config']
    flattened = flatten_json(config_data)
    print("   Flattened configuration:")
    for key, value in list(flattened.items())[:5]:  # Show first 5 items
        print(f"     {key}: {value}")
    print()
    
    # 7. Merge JSON objects
    print("7. Merging JSON objects:")
    additional_config = {
        "security": {
            "encryption": True,
            "auth_timeout": 3600
        },
        "database": {
            "pool_size": 20,
            "timeout": 30
        }
    }
    
    merged_config = merge_json_objects(config_data, additional_config, deep_merge=True)
    merged_file = f"{demo_dir}/merged_config.json"
    write_json_file(merged_config, merged_file, indent=2)
    print(f"   Merged configuration saved to: {Path(merged_file).name}\n")
    
    # 8. Update JSON file
    print("8. Updating JSON file:")
    updates = {
        'application.config.database.port': 5433,
        'application.config.cache.timeout': 600,
        'metadata.last_updated': datetime.now()
    }
    
    config_file = f"{demo_dir}/config.json"
    write_json_file(config_data, config_file, indent=2)  # Create initial config file
    update_success = update_json_file(config_file, updates, create_backup=False)
    print(f"   Update success: {update_success}\n")
    
    # 9. Create JSON report
    print("9. Creating JSON report:")
    report_data = {
        "report": {
            "title": "JSON Handler Demo Report",
            "generated": datetime.now(),
            "summary": {
                "total_users": len(read_data['users']),
                "active_users": len(active_users),
                "configuration_keys": len(flattened),
                "database_host": db_host
            },
            "user_details": [
                {
                    "name": user['name'],
                    "department": user['profile']['department'],
                    "age": user['profile']['age']
                }
                for user in read_data['users']
            ]
        }
    }
    
    report_file = f"{demo_dir}/demo_report.json"
    write_json_file(report_data, report_file, indent=2)
    print(f"   Report created: {Path(report_file).name}\n")
    
    # 10. Pretty print sample data
    print("10. Pretty printing sample JSON:")
    sample_for_display = {
        "user": read_data['users'][0],
        "config_sample": {
            "database": read_data['application']['config']['database']
        }
    }
    pretty_print_json(sample_for_display)
    
    print(f"\nDemo completed! Check the '{demo_dir}' directory for all generated files:")
    for file_path in Path(demo_dir).glob("*.json"):
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"   {file_path.name}: {size} bytes")


if __name__ == "__main__":
    main()