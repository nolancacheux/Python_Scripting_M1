#!/usr/bin/env python3
"""
File Organizer - Automated File Organization Script

This script helps organize files in a directory by extension and/or date.
It can sort files into folders based on their file type or creation date.

Author: Python Automation Examples
Date: 2025
"""

import os
import shutil
import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import logging


class FileOrganizer:
    """
    A class to organize files in directories by extension or date.
    
    Attributes:
        source_dir (Path): Source directory to organize
        target_dir (Path): Target directory for organized files
        file_types (Dict): Mapping of file extensions to folder names
    """
    
    def __init__(self, source_dir: str, target_dir: Optional[str] = None):
        """
        Initialize the FileOrganizer.
        
        Args:
            source_dir (str): Path to the source directory
            target_dir (str, optional): Path to target directory. Defaults to source_dir
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir) if target_dir else self.source_dir
        
        # Define file type categories
        self.file_types = {
            # Documents
            '.pdf': 'Documents/PDF',
            '.doc': 'Documents/Word', '.docx': 'Documents/Word',
            '.xls': 'Documents/Excel', '.xlsx': 'Documents/Excel',
            '.ppt': 'Documents/PowerPoint', '.pptx': 'Documents/PowerPoint',
            '.txt': 'Documents/Text',
            
            # Images
            '.jpg': 'Images/JPEG', '.jpeg': 'Images/JPEG',
            '.png': 'Images/PNG',
            '.gif': 'Images/GIF',
            '.bmp': 'Images/Bitmap',
            '.svg': 'Images/Vector',
            '.tiff': 'Images/TIFF',
            
            # Videos
            '.mp4': 'Videos/MP4',
            '.avi': 'Videos/AVI',
            '.mkv': 'Videos/MKV',
            '.mov': 'Videos/QuickTime',
            '.wmv': 'Videos/Windows',
            
            # Audio
            '.mp3': 'Audio/MP3',
            '.wav': 'Audio/WAV',
            '.flac': 'Audio/FLAC',
            '.aac': 'Audio/AAC',
            
            # Archives
            '.zip': 'Archives/ZIP',
            '.rar': 'Archives/RAR',
            '.7z': 'Archives/7Z',
            '.tar': 'Archives/TAR',
            '.gz': 'Archives/GZ',
            
            # Code
            '.py': 'Code/Python',
            '.js': 'Code/JavaScript',
            '.html': 'Code/HTML', '.htm': 'Code/HTML',
            '.css': 'Code/CSS',
            '.java': 'Code/Java',
            '.cpp': 'Code/CPP', '.c': 'Code/C',
            '.json': 'Code/JSON',
            '.xml': 'Code/XML',
            
            # Executables
            '.exe': 'Programs/Executables',
            '.msi': 'Programs/Installers',
            '.dmg': 'Programs/MacOS',
            '.deb': 'Programs/Linux',
            '.rpm': 'Programs/Linux',
        }
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('file_organizer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def organize_by_extension(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Organize files by their extensions.
        
        Args:
            dry_run (bool): If True, only show what would be moved without actually moving
            
        Returns:
            Dict[str, int]: Statistics of files organized by category
        """
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory {self.source_dir} does not exist")
        
        stats = {}
        files_moved = 0
        
        try:
            for file_path in self.source_dir.iterdir():
                if file_path.is_file():
                    extension = file_path.suffix.lower()
                    
                    # Determine target folder
                    if extension in self.file_types:
                        folder_name = self.file_types[extension]
                    else:
                        folder_name = 'Others/Unknown'
                    
                    target_folder = self.target_dir / folder_name
                    target_file = target_folder / file_path.name
                    
                    # Update statistics
                    category = folder_name.split('/')[0]
                    stats[category] = stats.get(category, 0) + 1
                    
                    if not dry_run:
                        # Create target directory if it doesn't exist
                        target_folder.mkdir(parents=True, exist_ok=True)
                        
                        # Handle file name conflicts
                        if target_file.exists():
                            base_name = file_path.stem
                            extension = file_path.suffix
                            counter = 1
                            while target_file.exists():
                                new_name = f"{base_name}_{counter}{extension}"
                                target_file = target_folder / new_name
                                counter += 1
                        
                        # Move the file
                        shutil.move(str(file_path), str(target_file))
                        self.logger.info(f"Moved: {file_path.name} -> {folder_name}")
                        files_moved += 1
                    else:
                        self.logger.info(f"Would move: {file_path.name} -> {folder_name}")
            
            if not dry_run:
                self.logger.info(f"Successfully organized {files_moved} files")
            else:
                self.logger.info(f"Dry run completed. {sum(stats.values())} files would be moved")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error during organization: {str(e)}")
            raise
    
    def organize_by_date(self, date_format: str = "%Y-%m", dry_run: bool = False) -> Dict[str, int]:
        """
        Organize files by their creation date.
        
        Args:
            date_format (str): Format for date folders (default: "%Y-%m" for Year-Month)
            dry_run (bool): If True, only show what would be moved without actually moving
            
        Returns:
            Dict[str, int]: Statistics of files organized by date period
        """
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory {self.source_dir} does not exist")
        
        stats = {}
        files_moved = 0
        
        try:
            for file_path in self.source_dir.iterdir():
                if file_path.is_file():
                    # Get file creation time
                    creation_time = datetime.datetime.fromtimestamp(file_path.stat().st_ctime)
                    date_folder = creation_time.strftime(date_format)
                    
                    target_folder = self.target_dir / "By_Date" / date_folder
                    target_file = target_folder / file_path.name
                    
                    # Update statistics
                    stats[date_folder] = stats.get(date_folder, 0) + 1
                    
                    if not dry_run:
                        # Create target directory
                        target_folder.mkdir(parents=True, exist_ok=True)
                        
                        # Handle file name conflicts
                        if target_file.exists():
                            base_name = file_path.stem
                            extension = file_path.suffix
                            counter = 1
                            while target_file.exists():
                                new_name = f"{base_name}_{counter}{extension}"
                                target_file = target_folder / new_name
                                counter += 1
                        
                        # Move the file
                        shutil.move(str(file_path), str(target_file))
                        self.logger.info(f"Moved: {file_path.name} -> By_Date/{date_folder}")
                        files_moved += 1
                    else:
                        self.logger.info(f"Would move: {file_path.name} -> By_Date/{date_folder}")
            
            if not dry_run:
                self.logger.info(f"Successfully organized {files_moved} files by date")
            else:
                self.logger.info(f"Dry run completed. {sum(stats.values())} files would be moved")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error during date organization: {str(e)}")
            raise
    
    def get_file_statistics(self) -> Dict[str, int]:
        """
        Get statistics about files in the source directory.
        
        Returns:
            Dict[str, int]: File count by extension
        """
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory {self.source_dir} does not exist")
        
        stats = {}
        
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                extension = file_path.suffix.lower() or 'No extension'
                stats[extension] = stats.get(extension, 0) + 1
        
        return stats
    
    def cleanup_empty_folders(self) -> int:
        """
        Remove empty directories in the target directory.
        
        Returns:
            int: Number of directories removed
        """
        removed_count = 0
        
        try:
            for root, dirs, files in os.walk(self.target_dir, topdown=False):
                for directory in dirs:
                    dir_path = Path(root) / directory
                    try:
                        if not any(dir_path.iterdir()):  # Directory is empty
                            dir_path.rmdir()
                            self.logger.info(f"Removed empty directory: {dir_path}")
                            removed_count += 1
                    except OSError:
                        # Directory not empty or permission denied
                        continue
                        
            return removed_count
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            return removed_count


def main():
    """Main function to handle command line arguments and execute file organization."""
    parser = argparse.ArgumentParser(description='Organize files by extension or date')
    parser.add_argument('source', help='Source directory to organize')
    parser.add_argument('--target', help='Target directory (default: same as source)')
    parser.add_argument('--mode', choices=['extension', 'date'], default='extension',
                       help='Organization mode (default: extension)')
    parser.add_argument('--date-format', default='%Y-%m',
                       help='Date format for date mode (default: %%Y-%%m)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be moved without actually moving')
    parser.add_argument('--stats', action='store_true',
                       help='Show file statistics before organizing')
    parser.add_argument('--cleanup', action='store_true',
                       help='Remove empty directories after organizing')
    
    args = parser.parse_args()
    
    try:
        # Initialize organizer
        organizer = FileOrganizer(args.source, args.target)
        
        # Show statistics if requested
        if args.stats:
            print("\n📊 File Statistics:")
            stats = organizer.get_file_statistics()
            for ext, count in sorted(stats.items()):
                print(f"  {ext}: {count} files")
            print()
        
        # Organize files
        if args.mode == 'extension':
            print("🗂️  Organizing files by extension...")
            results = organizer.organize_by_extension(dry_run=args.dry_run)
        else:
            print("📅 Organizing files by date...")
            results = organizer.organize_by_date(args.date_format, dry_run=args.dry_run)
        
        # Show results
        print("\n📈 Organization Results:")
        for category, count in sorted(results.items()):
            print(f"  {category}: {count} files")
        
        # Cleanup empty folders if requested
        if args.cleanup and not args.dry_run:
            print("\n🧹 Cleaning up empty directories...")
            removed = organizer.cleanup_empty_folders()
            print(f"Removed {removed} empty directories")
        
        print("\n✅ Organization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Basic organization by file extension:
       python file_organizer.py /path/to/messy/folder
    
    2. Organize by extension with dry run (preview only):
       python file_organizer.py /path/to/folder --dry-run
    
    3. Organize by date (Year-Month folders):
       python file_organizer.py /path/to/folder --mode date
    
    4. Organize by date with daily folders:
       python file_organizer.py /path/to/folder --mode date --date-format "%Y-%m-%d"
    
    5. Show file statistics before organizing:
       python file_organizer.py /path/to/folder --stats
    
    6. Organize to a different target directory:
       python file_organizer.py /source/folder --target /organized/folder
    
    7. Full organization with cleanup:
       python file_organizer.py /path/to/folder --stats --cleanup
    """
    exit(main())