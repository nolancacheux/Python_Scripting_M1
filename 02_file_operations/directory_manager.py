"""
Directory Manager Module - Comprehensive Directory Operations

This module demonstrates various directory operations including:
- Creating directories and nested structures
- Deleting directories safely
- Moving and copying directories
- Listing directory contents
- Managing directory permissions
- Directory tree operations
- Error handling for directory operations

Author: Python Learning Module
Date: 2025-08-08
"""

import os
import shutil
import stat
from pathlib import Path
from datetime import datetime
import tempfile


def create_directory(dir_path, exist_ok=True, parents=True):
    """
    Create a directory with optional parent directory creation.
    
    Args:
        dir_path (str): Path to the directory to create
        exist_ok (bool): If True, don't raise error if directory exists
        parents (bool): If True, create parent directories as needed
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = create_directory('data/processed/output', parents=True)
        if success:
            print("Directory structure created successfully")
    """
    try:
        Path(dir_path).mkdir(parents=parents, exist_ok=exist_ok)
        print(f"Successfully created directory: '{dir_path}'")
        return True
    
    except FileExistsError:
        print(f"Error: Directory '{dir_path}' already exists and exist_ok=False")
        return False
    except PermissionError:
        print(f"Error: Permission denied to create directory '{dir_path}'")
        return False
    except OSError as e:
        print(f"Error creating directory '{dir_path}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error creating directory '{dir_path}': {e}")
        return False


def delete_directory(dir_path, confirm=True):
    """
    Safely delete a directory and all its contents.
    
    Args:
        dir_path (str): Path to the directory to delete
        confirm (bool): Whether to ask for confirmation before deletion
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = delete_directory('temp_data', confirm=True)
        if success:
            print("Directory deleted successfully")
    """
    try:
        if not os.path.exists(dir_path):
            print(f"Directory '{dir_path}' does not exist.")
            return False
        
        if not os.path.isdir(dir_path):
            print(f"Error: '{dir_path}' is not a directory.")
            return False
        
        if confirm:
            response = input(f"Are you sure you want to delete '{dir_path}' and all its contents? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Deletion cancelled.")
                return False
        
        shutil.rmtree(dir_path)
        print(f"Successfully deleted directory: '{dir_path}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied to delete directory '{dir_path}'")
        return False
    except OSError as e:
        print(f"Error deleting directory '{dir_path}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error deleting directory '{dir_path}': {e}")
        return False


def copy_directory(source_dir, dest_dir, overwrite=False):
    """
    Copy a directory and all its contents to a new location.
    
    Args:
        source_dir (str): Path to the source directory
        dest_dir (str): Path to the destination directory
        overwrite (bool): Whether to overwrite existing destination
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = copy_directory('project_backup', 'project_backup_new')
        if success:
            print("Directory copied successfully")
    """
    try:
        if not os.path.exists(source_dir):
            print(f"Error: Source directory '{source_dir}' does not exist.")
            return False
        
        if not os.path.isdir(source_dir):
            print(f"Error: '{source_dir}' is not a directory.")
            return False
        
        if os.path.exists(dest_dir):
            if not overwrite:
                print(f"Error: Destination '{dest_dir}' already exists. Use overwrite=True to overwrite.")
                return False
            else:
                shutil.rmtree(dest_dir)
        
        shutil.copytree(source_dir, dest_dir)
        print(f"Successfully copied directory from '{source_dir}' to '{dest_dir}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied during directory copy operation")
        return False
    except OSError as e:
        print(f"Error copying directory: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error copying directory: {e}")
        return False


def move_directory(source_dir, dest_dir, overwrite=False):
    """
    Move a directory to a new location.
    
    Args:
        source_dir (str): Path to the source directory
        dest_dir (str): Path to the destination directory
        overwrite (bool): Whether to overwrite existing destination
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        success = move_directory('old_location/data', 'new_location/data')
        if success:
            print("Directory moved successfully")
    """
    try:
        if not os.path.exists(source_dir):
            print(f"Error: Source directory '{source_dir}' does not exist.")
            return False
        
        if not os.path.isdir(source_dir):
            print(f"Error: '{source_dir}' is not a directory.")
            return False
        
        if os.path.exists(dest_dir):
            if not overwrite:
                print(f"Error: Destination '{dest_dir}' already exists. Use overwrite=True to overwrite.")
                return False
            else:
                shutil.rmtree(dest_dir)
        
        # Create parent directories if they don't exist
        Path(dest_dir).parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(source_dir, dest_dir)
        print(f"Successfully moved directory from '{source_dir}' to '{dest_dir}'")
        return True
    
    except PermissionError:
        print(f"Error: Permission denied during directory move operation")
        return False
    except OSError as e:
        print(f"Error moving directory: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error moving directory: {e}")
        return False


def list_directory_contents(dir_path, recursive=False, show_hidden=False, show_details=False):
    """
    List the contents of a directory with various options.
    
    Args:
        dir_path (str): Path to the directory
        recursive (bool): Whether to list contents recursively
        show_hidden (bool): Whether to show hidden files/directories
        show_details (bool): Whether to show detailed information
    
    Returns:
        list: List of directory contents or None if error
    
    Example:
        contents = list_directory_contents('data', recursive=True, show_details=True)
        if contents:
            for item in contents:
                print(item)
    """
    try:
        if not os.path.exists(dir_path):
            print(f"Error: Directory '{dir_path}' does not exist.")
            return None
        
        if not os.path.isdir(dir_path):
            print(f"Error: '{dir_path}' is not a directory.")
            return None
        
        contents = []
        
        if recursive:
            for root, dirs, files in os.walk(dir_path):
                # Filter hidden directories and files if needed
                if not show_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                
                for name in dirs + files:
                    full_path = os.path.join(root, name)
                    relative_path = os.path.relpath(full_path, dir_path)
                    
                    if show_details:
                        stat_info = os.stat(full_path)
                        is_dir = os.path.isdir(full_path)
                        size = stat_info.st_size if not is_dir else 0
                        modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        item_type = 'DIR' if is_dir else 'FILE'
                        
                        contents.append(f"{item_type:4} {size:>10} {modified} {relative_path}")
                    else:
                        contents.append(relative_path)
        else:
            for item in os.listdir(dir_path):
                if not show_hidden and item.startswith('.'):
                    continue
                
                item_path = os.path.join(dir_path, item)
                
                if show_details:
                    stat_info = os.stat(item_path)
                    is_dir = os.path.isdir(item_path)
                    size = stat_info.st_size if not is_dir else 0
                    modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    item_type = 'DIR' if is_dir else 'FILE'
                    
                    contents.append(f"{item_type:4} {size:>10} {modified} {item}")
                else:
                    contents.append(item)
        
        contents.sort()
        print(f"Found {len(contents)} items in '{dir_path}'")
        return contents
    
    except PermissionError:
        print(f"Error: Permission denied to access directory '{dir_path}'")
        return None
    except OSError as e:
        print(f"Error listing directory contents: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error listing directory contents: {e}")
        return None


def get_directory_size(dir_path):
    """
    Calculate the total size of a directory and its contents.
    
    Args:
        dir_path (str): Path to the directory
    
    Returns:
        int: Total size in bytes, or None if error
    
    Example:
        size = get_directory_size('data')
        if size is not None:
            print(f"Directory size: {size / (1024*1024):.2f} MB")
    """
    try:
        if not os.path.exists(dir_path):
            print(f"Error: Directory '{dir_path}' does not exist.")
            return None
        
        if not os.path.isdir(dir_path):
            print(f"Error: '{dir_path}' is not a directory.")
            return None
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    # Skip files that can't be accessed
                    continue
        
        print(f"Directory '{dir_path}' total size: {total_size} bytes ({total_size / (1024*1024):.2f} MB)")
        return total_size
    
    except Exception as e:
        print(f"Error calculating directory size: {e}")
        return None


def create_directory_structure(structure_dict, base_path="."):
    """
    Create a nested directory structure from a dictionary.
    
    Args:
        structure_dict (dict): Dictionary representing directory structure
        base_path (str): Base path for the structure
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        structure = {
            'project': {
                'src': {
                    'main': {},
                    'tests': {}
                },
                'docs': {},
                'config': {}
            }
        }
        success = create_directory_structure(structure, 'new_project')
    """
    try:
        def create_nested_dirs(dirs_dict, current_path):
            for dir_name, subdirs in dirs_dict.items():
                dir_path = os.path.join(current_path, dir_name)
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {dir_path}")
                
                if isinstance(subdirs, dict) and subdirs:
                    create_nested_dirs(subdirs, dir_path)
        
        # Create base path if it doesn't exist
        Path(base_path).mkdir(parents=True, exist_ok=True)
        
        create_nested_dirs(structure_dict, base_path)
        print(f"Successfully created directory structure in '{base_path}'")
        return True
    
    except Exception as e:
        print(f"Error creating directory structure: {e}")
        return False


def find_empty_directories(dir_path):
    """
    Find all empty directories within a given directory.
    
    Args:
        dir_path (str): Path to search for empty directories
    
    Returns:
        list: List of empty directory paths or None if error
    
    Example:
        empty_dirs = find_empty_directories('project')
        if empty_dirs:
            print(f"Found {len(empty_dirs)} empty directories")
            for empty_dir in empty_dirs:
                print(f"  {empty_dir}")
    """
    try:
        if not os.path.exists(dir_path):
            print(f"Error: Directory '{dir_path}' does not exist.")
            return None
        
        if not os.path.isdir(dir_path):
            print(f"Error: '{dir_path}' is not a directory.")
            return None
        
        empty_dirs = []
        for root, dirs, files in os.walk(dir_path):
            # Check if current directory is empty (no files and no subdirectories)
            if not files and not dirs:
                empty_dirs.append(root)
            # Check subdirectories
            for dirname in dirs:
                dirpath = os.path.join(root, dirname)
                try:
                    if not os.listdir(dirpath):  # Directory is empty
                        empty_dirs.append(dirpath)
                except PermissionError:
                    # Skip directories we can't access
                    continue
        
        print(f"Found {len(empty_dirs)} empty directories in '{dir_path}'")
        return empty_dirs
    
    except Exception as e:
        print(f"Error finding empty directories: {e}")
        return None


def cleanup_empty_directories(dir_path, confirm=True):
    """
    Remove all empty directories within a given directory.
    
    Args:
        dir_path (str): Path to clean up empty directories
        confirm (bool): Whether to ask for confirmation before deletion
    
    Returns:
        int: Number of directories removed, or -1 if error
    
    Example:
        removed_count = cleanup_empty_directories('project', confirm=True)
        if removed_count > 0:
            print(f"Removed {removed_count} empty directories")
    """
    try:
        empty_dirs = find_empty_directories(dir_path)
        if not empty_dirs:
            print("No empty directories found.")
            return 0
        
        if confirm:
            print(f"Found {len(empty_dirs)} empty directories:")
            for empty_dir in empty_dirs:
                print(f"  {empty_dir}")
            
            response = input(f"Remove all {len(empty_dirs)} empty directories? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Cleanup cancelled.")
                return 0
        
        removed_count = 0
        for empty_dir in empty_dirs:
            try:
                os.rmdir(empty_dir)
                print(f"Removed empty directory: {empty_dir}")
                removed_count += 1
            except OSError:
                # Directory might not be empty anymore or permission denied
                print(f"Could not remove directory: {empty_dir}")
        
        print(f"Successfully removed {removed_count} empty directories")
        return removed_count
    
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return -1


def create_temporary_directory(prefix="temp_", suffix=""):
    """
    Create a temporary directory that will be automatically cleaned up.
    
    Args:
        prefix (str): Prefix for the temporary directory name
        suffix (str): Suffix for the temporary directory name
    
    Returns:
        str: Path to the temporary directory or None if error
    
    Example:
        temp_dir = create_temporary_directory(prefix="data_processing_")
        if temp_dir:
            print(f"Temporary directory created: {temp_dir}")
            # Use the temporary directory...
            # It will be cleaned up automatically
    """
    try:
        temp_dir = tempfile.mkdtemp(prefix=prefix, suffix=suffix)
        print(f"Created temporary directory: {temp_dir}")
        return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None


def main():
    """
    Demonstration of directory management functions.
    Run this script to see examples of all directory operations.
    """
    print("=== Directory Manager Module Demonstration ===\n")
    
    # Create a demo base directory
    demo_base = "directory_manager_demo"
    
    # 1. Create directory structure
    print("1. Creating directory structure:")
    structure = {
        demo_base: {
            'data': {
                'input': {},
                'output': {},
                'processed': {}
            },
            'logs': {},
            'config': {},
            'temp': {}
        }
    }
    create_directory_structure(structure)
    print()
    
    # 2. List directory contents
    print("2. Listing directory contents:")
    contents = list_directory_contents(demo_base, recursive=True, show_details=True)
    if contents:
        for item in contents[:10]:  # Show first 10 items
            print(f"   {item}")
    print()
    
    # 3. Create some test files to make directories non-empty
    print("3. Creating test files:")
    test_files = [
        f"{demo_base}/data/input/sample.txt",
        f"{demo_base}/logs/app.log",
        f"{demo_base}/config/settings.ini"
    ]
    for file_path in test_files:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).write_text(f"Test content for {Path(file_path).name}")
        print(f"   Created: {file_path}")
    print()
    
    # 4. Get directory size
    print("4. Calculating directory size:")
    size = get_directory_size(demo_base)
    if size is not None:
        print(f"   Total size: {size} bytes\n")
    
    # 5. Find empty directories
    print("5. Finding empty directories:")
    empty_dirs = find_empty_directories(demo_base)
    if empty_dirs:
        for empty_dir in empty_dirs:
            print(f"   Empty: {empty_dir}")
    print()
    
    # 6. Copy directory
    print("6. Copying directory:")
    copy_success = copy_directory(f"{demo_base}/data", f"{demo_base}/data_backup")
    print(f"   Copy success: {copy_success}\n")
    
    # 7. Create temporary directory
    print("7. Creating temporary directory:")
    temp_dir = create_temporary_directory(prefix="demo_temp_")
    if temp_dir:
        print(f"   Temporary directory: {temp_dir}")
        # Create a test file in temp directory
        test_file = os.path.join(temp_dir, "test.txt")
        Path(test_file).write_text("Temporary test content")
        print(f"   Created test file: {test_file}")
    print()
    
    # 8. Show final directory structure
    print("8. Final directory structure:")
    final_contents = list_directory_contents(demo_base, recursive=True, show_details=False)
    if final_contents:
        print("   Created structure:")
        for item in sorted(final_contents):
            print(f"     {item}")
    
    print(f"\nDemo completed. Check the '{demo_base}' directory to see the results.")
    print("Note: Temporary directories will be cleaned up automatically by the system.")


if __name__ == "__main__":
    main()