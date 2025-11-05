#!/usr/bin/env python3
"""
Simple Interactive Google Services Consolidator

Easy-to-use version of the Google Services zip consolidator with interactive prompts.
Supports both Google Photos and Google Drive.
"""

import os
from pathlib import Path
from main import GoogleServicesConsolidator, ServiceType


def get_directory_input(prompt: str, default: str = None) -> str:
    """Get directory input from user with validation."""
    while True:
        if default:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if not user_input:
            print("Please provide a directory path.")
            continue
            
        path = Path(user_input).expanduser().resolve()
        
        if "zip" in prompt.lower():
            # For zip directory, it must exist
            if not path.exists():
                print(f"Directory does not exist: {path}")
                continue
            if not any(path.glob("*.zip")):
                print(f"No zip files found in: {path}")
                continue
        else:
            # For output directory, we can create it
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"Output directory ready: {path}")
            except Exception as e:
                print(f"Cannot create directory {path}: {e}")
                continue
        
        return str(path)


def main():
    """Interactive main function."""
    print("="*60)
    print("GOOGLE SERVICES ZIP CONSOLIDATOR")
    print("="*60)
    print()
    print("This tool will:")
    print("1. Find all .zip files in your specified directory")
    print("2. Extract each zip file temporarily")
    print("3. Consolidate Google Photos albums and/or Google Drive folders")
    print("4. Merge duplicate folders")
    print("5. Handle file name conflicts automatically")
    print()
    
    # Get service type
    print("STEP 1: Service Type")
    print("-" * 15)
    print("What would you like to consolidate?")
    print("1. Google Photos only")
    print("2. Google Drive only") 
    print("3. Both Google Photos and Drive")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            service_type = ServiceType.PHOTOS
            break
        elif choice == "2":
            service_type = ServiceType.DRIVE
            break
        elif choice == "3":
            service_type = ServiceType.BOTH
            break
        else:
            print("Please enter 1, 2, or 3")
    
    print(f"✓ Selected: {service_type.value}")
    print()
    
    # Get zip directory
    default_zip_dir = "/Volumes/Data/Backup/Google Backup/Photos/sanjeevsram@gmail.com"
    print("STEP 2: Zip Files Location")
    print("-" * 25)
    zip_directory = get_directory_input(
        "Enter the directory containing your Google Takeout zip files",
        default_zip_dir if Path(default_zip_dir).exists() else None
    )
    
    # Count zip files
    zip_count = len(list(Path(zip_directory).glob("*.zip")))
    print(f"✓ Found {zip_count} zip files to process")
    print()
    
    # Get output directory
    default_output = "/Volumes/Data/Backup/Google Backup/Consolidated"
    print("STEP 3: Output Location")
    print("-" * 20)
    output_directory = get_directory_input(
        "Enter where you want the consolidated files to be stored",
        default_output
    )
    print()
    
    # Ask about dry run
    print("STEP 4: Execution Mode")
    print("-" * 18)
    dry_run_choice = input("Do you want to do a dry run first? (see what would happen without actually doing it) [y/N]: ").strip().lower()
    dry_run = dry_run_choice in ['y', 'yes']
    
    if dry_run:
        print("✓ Dry run mode selected - no files will be moved")
    else:
        print("⚠️  LIVE MODE - files will be extracted and consolidated")
        confirm = input("Are you sure you want to proceed? [y/N]: ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    print()
    print("="*60)
    print("STARTING CONSOLIDATION")
    print("="*60)
    
    # Create and run consolidator
    consolidator = GoogleServicesConsolidator(
        zip_directory=zip_directory,
        output_directory=output_directory,
        service_type=service_type,
        dry_run=dry_run
    )
    
    try:
        consolidator.consolidate()
        
        if dry_run:
            print()
            print("="*60)
            print("DRY RUN COMPLETED")
            print("="*60)
            print("The dry run is complete. If everything looks good, run this script")
            print("again and choose 'N' when asked about dry run to perform the actual")
            print("consolidation.")
        else:
            print()
            print("="*60)
            print("CONSOLIDATION COMPLETED!")
            print("="*60)
            print(f"Your consolidated files are now available at:")
            
            if service_type in [ServiceType.PHOTOS, ServiceType.BOTH]:
                print(f"Google Photos: {Path(output_directory) / 'Google Photos'}")
            
            if service_type in [ServiceType.DRIVE, ServiceType.BOTH]:
                print(f"Google Drive: {Path(output_directory) / 'Google Drive'}")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()