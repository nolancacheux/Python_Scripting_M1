"""
CSV Processor Module - Comprehensive CSV File Operations

This module demonstrates various CSV operations including:
- Reading CSV files with different delimiters and formats
- Writing CSV files with proper formatting
- Data manipulation and filtering
- Handling headers and data types
- CSV validation and error handling
- Converting between CSV and other formats
- Statistical operations on CSV data

Author: Python Learning Module
Date: 2025-08-08
"""

import csv
import os
from datetime import datetime, date
from pathlib import Path
import json


def read_csv_to_dict_list(file_path, delimiter=',', encoding='utf-8', skip_empty_rows=True):
    """
    Read a CSV file and return data as a list of dictionaries.
    
    Args:
        file_path (str): Path to the CSV file
        delimiter (str): CSV delimiter character
        encoding (str): File encoding
        skip_empty_rows (bool): Whether to skip empty rows
    
    Returns:
        list: List of dictionaries representing CSV rows or None if error
    
    Example:
        data = read_csv_to_dict_list('employees.csv')
        if data:
            for employee in data:
                print(f"Name: {employee['name']}, Department: {employee['department']}")
    """
    try:
        data = []
        with open(file_path, 'r', encoding=encoding, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            for row_num, row in enumerate(reader, start=1):
                # Skip empty rows if requested
                if skip_empty_rows and all(value.strip() == '' for value in row.values()):
                    continue
                
                # Convert empty strings to None for cleaner data
                cleaned_row = {}
                for key, value in row.items():
                    cleaned_row[key] = value.strip() if value.strip() else None
                
                data.append(cleaned_row)
        
        print(f"Successfully read {len(data)} rows from CSV file '{file_path}'")
        return data
    
    except FileNotFoundError:
        print(f"Error: CSV file '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read CSV file '{file_path}'.")
        return None
    except csv.Error as e:
        print(f"CSV parsing error in file '{file_path}': {e}")
        return None
    except UnicodeDecodeError:
        print(f"Encoding error reading '{file_path}'. Try a different encoding like 'latin-1'.")
        return None
    except Exception as e:
        print(f"Unexpected error reading CSV file '{file_path}': {e}")
        return None


def write_dict_list_to_csv(data, file_path, fieldnames=None, delimiter=',', encoding='utf-8'):
    """
    Write a list of dictionaries to a CSV file.
    
    Args:
        data (list): List of dictionaries to write
        file_path (str): Path to the output CSV file
        fieldnames (list): List of field names for headers (optional)
        delimiter (str): CSV delimiter character
        encoding (str): File encoding
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        employees = [
            {'name': 'John Doe', 'age': 30, 'department': 'IT'},
            {'name': 'Jane Smith', 'age': 25, 'department': 'HR'}
        ]
        success = write_dict_list_to_csv(employees, 'output.csv')
    """
    try:
        if not data:
            print("Warning: No data to write to CSV file.")
            return False
        
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Determine fieldnames if not provided
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with open(file_path, 'w', encoding=encoding, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
            
            writer.writeheader()
            for row in data:
                # Handle None values by converting to empty string
                cleaned_row = {}
                for field in fieldnames:
                    value = row.get(field, '')
                    cleaned_row[field] = '' if value is None else str(value)
                writer.writerow(cleaned_row)
        
        print(f"Successfully wrote {len(data)} rows to CSV file '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to write to CSV file '{file_path}'.")
        return False
    except csv.Error as e:
        print(f"CSV writing error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing CSV file '{file_path}': {e}")
        return False


def append_to_csv(file_path, data, delimiter=',', encoding='utf-8'):
    """
    Append data to an existing CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        data (list): List of dictionaries to append
        delimiter (str): CSV delimiter character
        encoding (str): File encoding
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        new_employees = [{'name': 'Bob Wilson', 'age': 35, 'department': 'Finance'}]
        success = append_to_csv('employees.csv', new_employees)
    """
    try:
        if not data:
            print("Warning: No data to append to CSV file.")
            return False
        
        # Check if file exists and read header
        file_exists = os.path.exists(file_path)
        fieldnames = None
        
        if file_exists:
            # Read existing header
            with open(file_path, 'r', encoding=encoding, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=delimiter)
                fieldnames = next(reader, None)
        else:
            # Create new file with headers from first data row
            fieldnames = list(data[0].keys())
        
        # Append data
        with open(file_path, 'a', encoding=encoding, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
            
            # Write header if new file
            if not file_exists:
                writer.writeheader()
            
            for row in data:
                # Handle None values by converting to empty string
                cleaned_row = {}
                for field in fieldnames:
                    value = row.get(field, '')
                    cleaned_row[field] = '' if value is None else str(value)
                writer.writerow(cleaned_row)
        
        print(f"Successfully appended {len(data)} rows to CSV file '{file_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to append to CSV file '{file_path}'.")
        return False
    except csv.Error as e:
        print(f"CSV appending error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error appending to CSV file '{file_path}': {e}")
        return False


def filter_csv_data(data, filter_func):
    """
    Filter CSV data using a custom function.
    
    Args:
        data (list): List of dictionaries representing CSV data
        filter_func (callable): Function that takes a row dict and returns bool
    
    Returns:
        list: Filtered data
    
    Example:
        # Filter employees older than 25
        filtered = filter_csv_data(employees, lambda row: int(row['age']) > 25)
        
        # Filter by department
        it_employees = filter_csv_data(employees, lambda row: row['department'] == 'IT')
    """
    try:
        filtered_data = []
        for row in data:
            try:
                if filter_func(row):
                    filtered_data.append(row)
            except Exception as e:
                print(f"Error applying filter to row {row}: {e}")
                continue
        
        print(f"Filtered data: {len(filtered_data)} rows from {len(data)} total rows")
        return filtered_data
    
    except Exception as e:
        print(f"Error filtering CSV data: {e}")
        return []


def sort_csv_data(data, sort_key, reverse=False):
    """
    Sort CSV data by a specified key.
    
    Args:
        data (list): List of dictionaries representing CSV data
        sort_key (str): Key to sort by
        reverse (bool): Whether to sort in descending order
    
    Returns:
        list: Sorted data
    
    Example:
        # Sort by age (ascending)
        sorted_data = sort_csv_data(employees, 'age')
        
        # Sort by name (descending)
        sorted_data = sort_csv_data(employees, 'name', reverse=True)
    """
    try:
        def sort_func(row):
            value = row.get(sort_key, '')
            # Try to convert to number if possible
            try:
                return float(value) if value else 0
            except (ValueError, TypeError):
                return str(value).lower() if value else ''
        
        sorted_data = sorted(data, key=sort_func, reverse=reverse)
        print(f"Sorted {len(sorted_data)} rows by '{sort_key}' ({'descending' if reverse else 'ascending'})")
        return sorted_data
    
    except Exception as e:
        print(f"Error sorting CSV data: {e}")
        return data


def get_csv_statistics(data, numeric_fields=None):
    """
    Calculate basic statistics for numeric fields in CSV data.
    
    Args:
        data (list): List of dictionaries representing CSV data
        numeric_fields (list): List of field names to analyze (optional)
    
    Returns:
        dict: Statistics for each numeric field
    
    Example:
        stats = get_csv_statistics(employees, ['age', 'salary'])
        if stats:
            for field, field_stats in stats.items():
                print(f"{field}: avg={field_stats['avg']:.2f}, min={field_stats['min']}, max={field_stats['max']}")
    """
    try:
        if not data:
            print("No data available for statistics calculation.")
            return {}
        
        # Auto-detect numeric fields if not specified
        if numeric_fields is None:
            numeric_fields = []
            sample_row = data[0]
            for field, value in sample_row.items():
                if value is not None:
                    try:
                        float(value)
                        numeric_fields.append(field)
                    except (ValueError, TypeError):
                        pass
        
        statistics = {}
        
        for field in numeric_fields:
            values = []
            for row in data:
                value = row.get(field)
                if value is not None and str(value).strip():
                    try:
                        values.append(float(value))
                    except (ValueError, TypeError):
                        continue
            
            if values:
                statistics[field] = {
                    'count': len(values),
                    'sum': sum(values),
                    'avg': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'median': sorted(values)[len(values) // 2]
                }
        
        print(f"Calculated statistics for {len(statistics)} numeric fields")
        return statistics
    
    except Exception as e:
        print(f"Error calculating CSV statistics: {e}")
        return {}


def validate_csv_data(data, required_fields=None, field_validators=None):
    """
    Validate CSV data against specified rules.
    
    Args:
        data (list): List of dictionaries representing CSV data
        required_fields (list): List of required field names
        field_validators (dict): Dictionary of field_name: validator_function pairs
    
    Returns:
        dict: Validation results with errors and warnings
    
    Example:
        validators = {
            'age': lambda x: x.isdigit() and 0 <= int(x) <= 150,
            'email': lambda x: '@' in x and '.' in x
        }
        results = validate_csv_data(employees, ['name', 'age'], validators)
    """
    try:
        errors = []
        warnings = []
        
        required_fields = required_fields or []
        field_validators = field_validators or {}
        
        for row_num, row in enumerate(data, start=1):
            # Check required fields
            for field in required_fields:
                if field not in row or not row[field] or str(row[field]).strip() == '':
                    errors.append(f"Row {row_num}: Missing required field '{field}'")
            
            # Apply field validators
            for field, validator in field_validators.items():
                if field in row and row[field] is not None:
                    try:
                        if not validator(str(row[field])):
                            errors.append(f"Row {row_num}: Invalid value for field '{field}': {row[field]}")
                    except Exception as e:
                        errors.append(f"Row {row_num}: Validation error for field '{field}': {e}")
        
        validation_results = {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'total_rows': len(data),
            'error_count': len(errors)
        }
        
        print(f"Validation completed: {len(errors)} errors, {len(warnings)} warnings")
        return validation_results
    
    except Exception as e:
        print(f"Error validating CSV data: {e}")
        return {'is_valid': False, 'errors': [str(e)], 'warnings': [], 'total_rows': 0, 'error_count': 1}


def convert_csv_to_json(csv_file_path, json_file_path, encoding='utf-8'):
    """
    Convert a CSV file to JSON format.
    
    Args:
        csv_file_path (str): Path to the input CSV file
        json_file_path (str): Path to the output JSON file
        encoding (str): File encoding
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = convert_csv_to_json('data.csv', 'data.json')
        if success:
            print("CSV successfully converted to JSON")
    """
    try:
        # Read CSV data
        csv_data = read_csv_to_dict_list(csv_file_path, encoding=encoding)
        if csv_data is None:
            return False
        
        # Create directory for output file
        Path(json_file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON data
        with open(json_file_path, 'w', encoding=encoding) as json_file:
            json.dump(csv_data, json_file, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted CSV to JSON: {len(csv_data)} records written to '{json_file_path}'")
        return True
    
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")
        return False


def merge_csv_files(file_paths, output_path, delimiter=',', encoding='utf-8'):
    """
    Merge multiple CSV files into a single file.
    
    Args:
        file_paths (list): List of CSV file paths to merge
        output_path (str): Path to the output merged CSV file
        delimiter (str): CSV delimiter character
        encoding (str): File encoding
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        files_to_merge = ['employees_2023.csv', 'employees_2024.csv']
        success = merge_csv_files(files_to_merge, 'all_employees.csv')
    """
    try:
        all_data = []
        all_fieldnames = set()
        
        # Read all CSV files and collect data
        for file_path in file_paths:
            print(f"Reading file: {file_path}")
            data = read_csv_to_dict_list(file_path, delimiter=delimiter, encoding=encoding)
            if data is None:
                print(f"Skipping file due to read error: {file_path}")
                continue
            
            all_data.extend(data)
            # Collect all unique fieldnames
            for row in data:
                all_fieldnames.update(row.keys())
        
        if not all_data:
            print("No data found in any of the input files.")
            return False
        
        # Convert set to sorted list for consistent ordering
        fieldnames = sorted(all_fieldnames)
        
        # Write merged data
        success = write_dict_list_to_csv(all_data, output_path, fieldnames, delimiter, encoding)
        
        if success:
            print(f"Successfully merged {len(file_paths)} files into '{output_path}' with {len(all_data)} total records")
        
        return success
    
    except Exception as e:
        print(f"Error merging CSV files: {e}")
        return False


def create_csv_report(data, output_path, title="CSV Report"):
    """
    Create a formatted report from CSV data.
    
    Args:
        data (list): List of dictionaries representing CSV data
        output_path (str): Path to the output report file
        title (str): Report title
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = create_csv_report(employees, 'employee_report.txt', 'Employee Summary')
    """
    try:
        if not data:
            print("No data available for report generation.")
            return False
        
        # Create directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as report_file:
            # Write report header
            report_file.write(f"{title}\n")
            report_file.write("=" * len(title) + "\n\n")
            report_file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write(f"Total records: {len(data)}\n\n")
            
            # Write field summary
            if data:
                fields = list(data[0].keys())
                report_file.write("Fields:\n")
                for i, field in enumerate(fields, 1):
                    report_file.write(f"  {i}. {field}\n")
                report_file.write("\n")
                
                # Calculate and write statistics for numeric fields
                stats = get_csv_statistics(data)
                if stats:
                    report_file.write("Numeric Field Statistics:\n")
                    for field, field_stats in stats.items():
                        report_file.write(f"\n  {field}:\n")
                        report_file.write(f"    Count: {field_stats['count']}\n")
                        report_file.write(f"    Average: {field_stats['avg']:.2f}\n")
                        report_file.write(f"    Minimum: {field_stats['min']}\n")
                        report_file.write(f"    Maximum: {field_stats['max']}\n")
                        report_file.write(f"    Median: {field_stats['median']}\n")
                
                # Write sample data (first 5 records)
                report_file.write(f"\nSample Data (first 5 records):\n")
                report_file.write("-" * 50 + "\n")
                for i, row in enumerate(data[:5], 1):
                    report_file.write(f"Record {i}:\n")
                    for field, value in row.items():
                        report_file.write(f"  {field}: {value}\n")
                    report_file.write("\n")
        
        print(f"Successfully created report: '{output_path}'")
        return True
    
    except Exception as e:
        print(f"Error creating CSV report: {e}")
        return False


def main():
    """
    Demonstration of CSV processing functions.
    Run this script to see examples of all CSV operations.
    """
    print("=== CSV Processor Module Demonstration ===\n")
    
    # Create demo directory
    demo_dir = "csv_processor_demo"
    os.makedirs(demo_dir, exist_ok=True)
    
    # 1. Create sample CSV data
    print("1. Creating sample CSV data:")
    employees = [
        {'name': 'John Doe', 'age': 30, 'department': 'IT', 'salary': 75000, 'email': 'john@company.com'},
        {'name': 'Jane Smith', 'age': 25, 'department': 'HR', 'salary': 65000, 'email': 'jane@company.com'},
        {'name': 'Bob Wilson', 'age': 35, 'department': 'Finance', 'salary': 80000, 'email': 'bob@company.com'},
        {'name': 'Alice Brown', 'age': 28, 'department': 'IT', 'salary': 70000, 'email': 'alice@company.com'},
        {'name': 'Charlie Davis', 'age': 32, 'department': 'Marketing', 'salary': 68000, 'email': 'charlie@company.com'}
    ]
    
    csv_file = f"{demo_dir}/employees.csv"
    success = write_dict_list_to_csv(employees, csv_file)
    print(f"   Created sample CSV file: {success}\n")
    
    # 2. Read CSV data
    print("2. Reading CSV data:")
    read_data = read_csv_to_dict_list(csv_file)
    if read_data:
        print(f"   Successfully read {len(read_data)} records")
        print(f"   Sample record: {read_data[0]}")
    print()
    
    # 3. Filter data
    print("3. Filtering CSV data:")
    it_employees = filter_csv_data(read_data, lambda row: row['department'] == 'IT')
    print(f"   IT employees: {len(it_employees)}")
    for emp in it_employees:
        print(f"     {emp['name']} - {emp['department']}")
    print()
    
    # 4. Sort data
    print("4. Sorting CSV data:")
    sorted_by_salary = sort_csv_data(read_data, 'salary', reverse=True)
    print("   Top 3 by salary:")
    for emp in sorted_by_salary[:3]:
        print(f"     {emp['name']}: ${emp['salary']}")
    print()
    
    # 5. Calculate statistics
    print("5. Calculating statistics:")
    stats = get_csv_statistics(read_data, ['age', 'salary'])
    for field, field_stats in stats.items():
        print(f"   {field.upper()}:")
        print(f"     Average: {field_stats['avg']:.2f}")
        print(f"     Range: {field_stats['min']} - {field_stats['max']}")
    print()
    
    # 6. Validate data
    print("6. Validating CSV data:")
    validators = {
        'age': lambda x: x.isdigit() and 18 <= int(x) <= 70,
        'email': lambda x: '@' in x and '.' in x,
        'salary': lambda x: x.isdigit() and int(x) > 0
    }
    validation_results = validate_csv_data(read_data, ['name', 'department'], validators)
    print(f"   Validation passed: {validation_results['is_valid']}")
    print(f"   Errors: {len(validation_results['errors'])}")
    print()
    
    # 7. Append data
    print("7. Appending new data:")
    new_employees = [
        {'name': 'David Lee', 'age': 29, 'department': 'IT', 'salary': 72000, 'email': 'david@company.com'}
    ]
    append_success = append_to_csv(csv_file, new_employees)
    print(f"   Append success: {append_success}\n")
    
    # 8. Convert to JSON
    print("8. Converting CSV to JSON:")
    json_file = f"{demo_dir}/employees.json"
    convert_success = convert_csv_to_json(csv_file, json_file)
    print(f"   Conversion success: {convert_success}\n")
    
    # 9. Create report
    print("9. Creating CSV report:")
    report_file = f"{demo_dir}/employee_report.txt"
    updated_data = read_csv_to_dict_list(csv_file)  # Re-read to include appended data
    report_success = create_csv_report(updated_data, report_file, "Employee Data Report")
    print(f"   Report creation success: {report_success}\n")
    
    # 10. Create additional CSV for merge demo
    print("10. Creating additional CSV for merge demonstration:")
    contractors = [
        {'name': 'Mike Johnson', 'age': 40, 'department': 'Consulting', 'salary': 85000, 'email': 'mike@contractor.com'},
        {'name': 'Lisa Wang', 'age': 33, 'department': 'Design', 'salary': 72000, 'email': 'lisa@contractor.com'}
    ]
    contractors_file = f"{demo_dir}/contractors.csv"
    write_dict_list_to_csv(contractors, contractors_file)
    
    # Merge files
    merged_file = f"{demo_dir}/all_staff.csv"
    merge_success = merge_csv_files([csv_file, contractors_file], merged_file)
    print(f"   Merge success: {merge_success}")
    
    print(f"\nDemo completed! Check the '{demo_dir}' directory for all generated files:")
    for file_path in Path(demo_dir).glob("*"):
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"   {file_path.name}: {size} bytes")


if __name__ == "__main__":
    main()