#!/usr/bin/env python3
"""
Google Services Zip Consolidator

This script extracts multiple Google Takeout zip files (Photos, Drive, etc.) and 
consolidates them into a unified folder structure, merging duplicate folders.

Features:
- Extracts all zip files in a directory
- Consolidates duplicate folders (Google Photos albums, Google Drive folders)
- Preserves file names and handles duplicates
- Progress tracking and logging
- Dry run mode for testing
- Support for Google Photos and Google Drive takeout files

Usage:
    python main.py --service photos  # For Google Photos
    python main.py --service drive   # For Google Drive
    python main.py --service both    # For both services
"""

import os
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import List, Set, Dict, Optional
import argparse
import logging
from datetime import datetime
from enum import Enum


class ServiceType(Enum):
    """Supported Google services."""
    PHOTOS = "photos"
    DRIVE = "drive" 
    BOTH = "both"


class GoogleServicesConsolidator:
    """Consolidates Google Services (Photos, Drive) takeout zip files into unified structure."""
    
    def __init__(self, zip_directory: str, output_directory: str, service_type: ServiceType = ServiceType.PHOTOS, dry_run: bool = False):
        """
        Initialize the consolidator.
        
        Args:
            zip_directory: Directory containing zip files
            output_directory: Directory where consolidated files will be stored
            service_type: Type of Google service to consolidate (photos, drive, both)
            dry_run: If True, only show what would be done without actually doing it
        """
        self.zip_directory = Path(zip_directory)
        self.output_directory = Path(output_directory)
        self.service_type = service_type
        self.dry_run = dry_run
        self.temp_dir = None
        
        # Create consolidated directories based on service type
        self.google_photos_dir = self.output_directory / "Google Photos"
        self.google_drive_dir = self.output_directory / "Google Drive"
        
        # Statistics
        self.stats = {
            'zip_files_processed': 0,
            'photos_albums_found': set(),
            'drive_folders_found': set(),
            'files_copied': 0,
            'files_skipped': 0,
            'errors': []
        }
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        log_level = logging.INFO
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        # Create logs directory
        logs_dir = self.output_directory / "logs"
        if not self.dry_run:
            logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup file and console logging
        if not self.dry_run:
            log_file = logs_dir / f"consolidation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            logging.basicConfig(
                level=log_level,
                format=log_format,
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler()
                ]
            )
        else:
            logging.basicConfig(level=log_level, format=log_format, handlers=[logging.StreamHandler()])
        
        self.logger = logging.getLogger(__name__)
    
    def find_zip_files(self) -> List[Path]:
        """
        Find all zip files in the zip directory.
        
        Returns:
            List of zip file paths
        """
        zip_files = list(self.zip_directory.glob("*.zip"))
        self.logger.info(f"Found {len(zip_files)} zip files in {self.zip_directory}")
        
        for zip_file in zip_files:
            self.logger.debug(f"  - {zip_file.name}")
        
        return zip_files
    
    def extract_zip_file(self, zip_path: Path) -> Path:
        """
        Extract a zip file to temporary directory.
        
        Args:
            zip_path: Path to the zip file
            
        Returns:
            Path to the extracted directory
        """
        if not self.temp_dir:
            self.temp_dir = Path(tempfile.mkdtemp(prefix="google_photos_"))
            self.logger.info(f"Created temporary directory: {self.temp_dir}")
        
        extract_dir = self.temp_dir / zip_path.stem
        
        self.logger.info(f"Extracting {zip_path.name}...")
        
        if not self.dry_run:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                self.logger.info(f"  Extracted to: {extract_dir}")
            except Exception as e:
                error_msg = f"Error extracting {zip_path.name}: {str(e)}"
                self.logger.error(error_msg)
                self.stats['errors'].append(error_msg)
                return None
        else:
            self.logger.info(f"  [DRY RUN] Would extract to: {extract_dir}")
        
        return extract_dir
    
    def find_service_paths(self, extract_dir: Path) -> Dict[str, Optional[Path]]:
        """
        Find Google service directories within extracted content.
        
        Args:
            extract_dir: Directory where zip was extracted
            
        Returns:
            Dictionary with paths to Google Photos and Google Drive directories
        """
        result = {'photos': None, 'drive': None}
        
        # Look for Google Photos
        if self.service_type in [ServiceType.PHOTOS, ServiceType.BOTH]:
            # Look for Takeout/Google Photos pattern
            photos_dirs = list(extract_dir.glob("**/Takeout*/Google Photos"))
            if not photos_dirs:
                # Fallback: look for any Google Photos directory
                photos_dirs = list(extract_dir.glob("**/Google Photos"))
            
            if photos_dirs:
                result['photos'] = photos_dirs[0]
                self.logger.info(f"Found Google Photos directory: {photos_dirs[0]}")
            else:
                self.logger.debug(f"No 'Google Photos' directory found in {extract_dir}")
        
        # Look for Google Drive 
        if self.service_type in [ServiceType.DRIVE, ServiceType.BOTH]:
            # Look for Takeout/Drive pattern
            drive_dirs = list(extract_dir.glob("**/Takeout*/Drive"))
            if not drive_dirs:
                # Alternative patterns Google uses
                drive_dirs = list(extract_dir.glob("**/Takeout*/My Drive"))
                if not drive_dirs:
                    drive_dirs = list(extract_dir.glob("**/Drive"))
                    if not drive_dirs:
                        drive_dirs = list(extract_dir.glob("**/My Drive"))
            
            if drive_dirs:
                result['drive'] = drive_dirs[0]
                self.logger.info(f"Found Google Drive directory: {drive_dirs[0]}")
            else:
                self.logger.debug(f"No 'Google Drive' directory found in {extract_dir}")
        
        return result
    
    def get_safe_filename(self, filepath: Path, destination_dir: Path) -> Path:
        """
        Get a safe filename that doesn't conflict with existing files.
        
        Args:
            filepath: Original file path
            destination_dir: Destination directory
            
        Returns:
            Safe file path that won't overwrite existing files
        """
        destination_file = destination_dir / filepath.name
        
        if not destination_file.exists():
            return destination_file
        
        # File exists, create a unique name
        stem = filepath.stem
        suffix = filepath.suffix
        counter = 1
        
        while True:
            new_name = f"{stem}_{counter:03d}{suffix}"
            new_path = destination_dir / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def copy_folder_contents(self, source_folder: Path, dest_folder: Path, folder_type: str = "folder"):
        """
        Copy contents from source folder to destination folder.
        
        Args:
            source_folder: Source folder directory
            dest_folder: Destination folder directory
            folder_type: Type of folder (album, folder, etc.) for logging
        """
        self.logger.info(f"  Processing {folder_type}: {source_folder.name}")
        
        if not self.dry_run:
            dest_folder.mkdir(parents=True, exist_ok=True)
        
        # Get all files in the folder (including subdirectories)
        for item in source_folder.rglob("*"):
            if item.is_file():
                # Skip Google's metadata files
                if item.name.startswith('.') or item.name.endswith(('.json', '.html')):
                    if 'metadata' in item.name.lower() or 'takeout' in item.name.lower():
                        self.logger.debug(f"    Skipping metadata file: {item.name}")
                        continue
                
                # Calculate relative path from folder root
                rel_path = item.relative_to(source_folder)
                dest_file_dir = dest_folder / rel_path.parent
                
                if not self.dry_run:
                    dest_file_dir.mkdir(parents=True, exist_ok=True)
                    dest_file_path = self.get_safe_filename(item, dest_file_dir)
                    
                    try:
                        shutil.copy2(item, dest_file_path)
                        self.stats['files_copied'] += 1
                        self.logger.debug(f"    Copied: {rel_path} -> {dest_file_path.name}")
                    except Exception as e:
                        error_msg = f"Error copying {item}: {str(e)}"
                        self.logger.error(error_msg)
                        self.stats['errors'].append(error_msg)
                        self.stats['files_skipped'] += 1
                else:
                    self.logger.debug(f"    [DRY RUN] Would copy: {rel_path}")
                    self.stats['files_copied'] += 1
    
    def process_google_photos_directory(self, google_photos_dir: Path):
        """
        Process a Google Photos directory and consolidate its albums.
        
        Args:
            google_photos_dir: Path to extracted Google Photos directory
        """
        self.logger.info(f"Processing Google Photos directory: {google_photos_dir}")
        
        # Get all album directories
        albums = [d for d in google_photos_dir.iterdir() if d.is_dir()]
        
        for album in albums:
            album_name = album.name
            self.stats['photos_albums_found'].add(album_name)
            
            # Create corresponding album in consolidated directory
            dest_album = self.google_photos_dir / album_name
            
            self.copy_folder_contents(album, dest_album, "album")
    
    def process_google_drive_directory(self, google_drive_dir: Path):
        """
        Process a Google Drive directory and consolidate its folders.
        
        Args:
            google_drive_dir: Path to extracted Google Drive directory
        """
        self.logger.info(f"Processing Google Drive directory: {google_drive_dir}")
        
        # Get all top-level folders and files
        items = list(google_drive_dir.iterdir())
        
        for item in items:
            if item.is_dir():
                folder_name = item.name
                self.stats['drive_folders_found'].add(folder_name)
                
                # Create corresponding folder in consolidated directory
                dest_folder = self.google_drive_dir / folder_name
                
                self.copy_folder_contents(item, dest_folder, "folder")
            
            elif item.is_file():
                # Handle root-level files in Drive
                if not item.name.startswith('.') and not item.name.endswith(('.json', '.html')):
                    if not self.dry_run:
                        self.google_drive_dir.mkdir(parents=True, exist_ok=True)
                        dest_file_path = self.get_safe_filename(item, self.google_drive_dir)
                        
                        try:
                            shutil.copy2(item, dest_file_path)
                            self.stats['files_copied'] += 1
                            self.logger.debug(f"    Copied root file: {item.name}")
                        except Exception as e:
                            error_msg = f"Error copying root file {item}: {str(e)}"
                            self.logger.error(error_msg)
                            self.stats['errors'].append(error_msg)
                            self.stats['files_skipped'] += 1
                    else:
                        self.logger.debug(f"    [DRY RUN] Would copy root file: {item.name}")
                        self.stats['files_copied'] += 1
    
    def cleanup_temp_directory(self):
        """Clean up temporary extraction directory."""
        if self.temp_dir and self.temp_dir.exists() and not self.dry_run:
            try:
                shutil.rmtree(self.temp_dir)
                self.logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                self.logger.warning(f"Could not clean up temp directory: {e}")
    
    def print_statistics(self):
        """Print consolidation statistics."""
        print("\n" + "="*60)
        print("CONSOLIDATION STATISTICS")
        print("="*60)
        print(f"Service type: {self.service_type.value}")
        print(f"Zip files processed: {self.stats['zip_files_processed']}")
        
        if self.service_type in [ServiceType.PHOTOS, ServiceType.BOTH]:
            print(f"Photo albums found: {len(self.stats['photos_albums_found'])}")
        
        if self.service_type in [ServiceType.DRIVE, ServiceType.BOTH]:
            print(f"Drive folders found: {len(self.stats['drive_folders_found'])}")
        
        print(f"Files copied: {self.stats['files_copied']}")
        print(f"Files skipped: {self.stats['files_skipped']}")
        print(f"Errors encountered: {len(self.stats['errors'])}")
        
        if self.stats['photos_albums_found']:
            print(f"\nPhoto albums consolidated:")
            for album in sorted(self.stats['photos_albums_found']):
                print(f"  - {album}")
        
        if self.stats['drive_folders_found']:
            print(f"\nDrive folders consolidated:")
            for folder in sorted(self.stats['drive_folders_found']):
                print(f"  - {folder}")
        
        if self.stats['errors']:
            print(f"\nErrors:")
            for error in self.stats['errors']:
                print(f"  - {error}")
        
        print("="*60)
    
    def consolidate(self):
        """
        Main consolidation method.
        """
        try:
            self.logger.info(f"Starting Google Services consolidation")
            self.logger.info(f"Service type: {self.service_type.value}")
            self.logger.info(f"Zip directory: {self.zip_directory}")
            self.logger.info(f"Output directory: {self.output_directory}")
            self.logger.info(f"Dry run mode: {self.dry_run}")
            
            # Find all zip files
            zip_files = self.find_zip_files()
            
            if not zip_files:
                self.logger.warning("No zip files found!")
                return
            
            # Create output directories based on service type
            if not self.dry_run:
                if self.service_type in [ServiceType.PHOTOS, ServiceType.BOTH]:
                    self.google_photos_dir.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Created Google Photos directory: {self.google_photos_dir}")
                
                if self.service_type in [ServiceType.DRIVE, ServiceType.BOTH]:
                    self.google_drive_dir.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Created Google Drive directory: {self.google_drive_dir}")
            else:
                if self.service_type in [ServiceType.PHOTOS, ServiceType.BOTH]:
                    self.logger.info(f"[DRY RUN] Would create Google Photos directory: {self.google_photos_dir}")
                if self.service_type in [ServiceType.DRIVE, ServiceType.BOTH]:
                    self.logger.info(f"[DRY RUN] Would create Google Drive directory: {self.google_drive_dir}")
            
            # Process each zip file
            for i, zip_file in enumerate(zip_files, 1):
                self.logger.info(f"\n--- Processing zip {i}/{len(zip_files)}: {zip_file.name} ---")
                
                # Extract zip file
                extract_dir = self.extract_zip_file(zip_file)
                if not extract_dir:
                    continue
                
                # Find service directories
                service_paths = self.find_service_paths(extract_dir)
                
                # Process Google Photos if found and requested
                if service_paths['photos'] and self.service_type in [ServiceType.PHOTOS, ServiceType.BOTH]:
                    self.process_google_photos_directory(service_paths['photos'])
                
                # Process Google Drive if found and requested
                if service_paths['drive'] and self.service_type in [ServiceType.DRIVE, ServiceType.BOTH]:
                    self.process_google_drive_directory(service_paths['drive'])
                
                # Only increment if we processed something
                if service_paths['photos'] or service_paths['drive']:
                    self.stats['zip_files_processed'] += 1
                else:
                    self.logger.warning(f"No relevant service directories found in {zip_file.name}")
            
            self.logger.info("\nConsolidation completed!")
            
        except KeyboardInterrupt:
            self.logger.info("\nConsolidation interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            self.stats['errors'].append(str(e))
        finally:
            self.cleanup_temp_directory()
            self.print_statistics()


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Google Services Zip Consolidator")
    parser.add_argument(
        "--zip-dir", 
        default="/Volumes/Data/Backup/Google Backup/Photos/sanjeevsram@gmail.com",
        help="Directory containing Google Takeout zip files"
    )
    parser.add_argument(
        "--output-dir", 
        default="/Volumes/Data/Backup/Google Backup/Consolidated",
        help="Directory where consolidated files will be stored"
    )
    parser.add_argument(
        "--service",
        choices=["photos", "drive", "both"],
        default="photos",
        help="Which Google service to consolidate (default: photos)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be done without actually doing it"
    )
    
    args = parser.parse_args()
    
    # Validate directories
    zip_dir = Path(args.zip_dir)
    if not zip_dir.exists():
        print(f"Error: Zip directory does not exist: {zip_dir}")
        return 1
    
    # Create consolidator and run
    service_type = ServiceType(args.service)
    consolidator = GoogleServicesConsolidator(
        zip_directory=str(zip_dir),
        output_directory=args.output_dir,
        service_type=service_type,
        dry_run=args.dry_run
    )
    
    consolidator.consolidate()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
