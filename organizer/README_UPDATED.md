# Google Services Zip Consolidator

A Python tool to extract and consolidate Google Takeout zip files into a unified folder structure. Supports both **Google Photos** and **Google Drive**.

## Problem It Solves

When you download your data using Google Takeout, you often get:
- Multiple zip files (due to size limits)
- Each zip contains a `Takeout/Google Photos/` or `Takeout/Drive/` structure
- Album/folder contents are split across multiple zips
- Manual extraction creates duplicate folders

This tool automatically:
- Extracts all zip files
- Consolidates duplicate albums/folders
- Preserves your original folder structure
- Handles file name conflicts intelligently
- Works with both Google Photos and Google Drive

## Supported Services

✅ **Google Photos** - Albums and photo collections  
✅ **Google Drive** - Folders and files  
✅ **Both Services** - Process mixed takeout files  

## Before vs After

### Before (Manual Extraction):
```
/Your Directory/
├── Takeout/Google Photos/Album1/
├── Takeout 2/Google Photos/Album1/
├── Takeout/Drive/Documents/
├── Takeout 2/Drive/Documents/
└── Takeout 3/Drive/Projects/
```

### After (Using This Tool):
```
/Consolidated/
├── Google Photos/
│   └── Album1/          # All album files merged
└── Google Drive/
    ├── Documents/       # All document files merged
    └── Projects/        # All project files merged
```

## Features

✅ **Multi-Service Support**: Handle Google Photos, Google Drive, or both  
✅ **Automatic Extraction**: Processes all zip files in a directory  
✅ **Smart Consolidation**: Merges duplicate folders across zips  
✅ **File Safety**: Handles naming conflicts (adds `_001`, `_002`, etc.)  
✅ **Progress Tracking**: Shows detailed progress and statistics  
✅ **Dry Run Mode**: Preview what will happen before actual execution  
✅ **Logging**: Comprehensive logs for troubleshooting  
✅ **Interactive Mode**: Easy-to-use guided interface  

## Quick Start

### Option 1: Interactive Mode (Recommended)
```bash
python interactive.py
```
Follow the prompts to specify your service type, directories, and options.

### Option 2: Command Line
```bash
# Google Photos only
python main.py --service photos --zip-dir "/path/to/zips" --output-dir "/path/to/output"

# Google Drive only
python main.py --service drive --zip-dir "/path/to/zips" --output-dir "/path/to/output"

# Both services
python main.py --service both --zip-dir "/path/to/zips" --output-dir "/path/to/output"

# Dry run first (recommended)
python main.py --service both --zip-dir "/path/to/zips" --output-dir "/path/to/output" --dry-run
```

## Usage Examples

### Example 1: Your Google Photos (Original Use Case)
```bash
# Interactive mode
python interactive.py
# Choose "1" for Google Photos only

# Or command line
python main.py \
  --service photos \
  --zip-dir "/Volumes/Data/Backup/Google Backup/Photos/sanjeevsram@gmail.com" \
  --output-dir "/Volumes/Data/Backup/Google Backup/Consolidated"
```

### Example 2: Google Drive Only
```bash
python main.py \
  --service drive \
  --zip-dir "/Users/john/Downloads/GoogleDrive" \
  --output-dir "/Users/john/Documents/Consolidated"
```

### Example 3: Both Services
```bash
python main.py \
  --service both \
  --zip-dir "/path/to/mixed/takeout/files" \
  --output-dir "/path/to/consolidated"
```

### Example 4: Dry Run First
```bash
# See what would happen for both services
python main.py --service both --zip-dir "/path/to/zips" --output-dir "/path/to/output" --dry-run
```

## Service-Specific Handling

### Google Photos
- Consolidates **albums** (like "Vacation 2023", "Family Photos")
- Preserves photo metadata and timestamps
- Handles duplicate photos across multiple takeout files
- Skips Google's metadata JSON files

### Google Drive
- Consolidates **folders** and **files**
- Maintains folder hierarchy and structure
- Handles root-level files in Drive
- Preserves file permissions and timestamps
- Skips Google's internal metadata files

### Mixed Takeout Files
- Automatically detects which service each zip contains
- Can process zips with both Photos and Drive content
- Creates separate consolidated directories for each service

## Output Structure

### Google Photos Only:
```
/Consolidated/
├── Google Photos/
│   ├── Family Events/
│   ├── Vacation 2023/
│   └── Wedding Photos/
└── logs/
```

### Google Drive Only:
```
/Consolidated/
├── Google Drive/
│   ├── Documents/
│   ├── Projects/
│   ├── important_file.pdf
│   └── spreadsheet.xlsx
└── logs/
```

### Both Services:
```
/Consolidated/
├── Google Photos/
│   ├── Album1/
│   └── Album2/
├── Google Drive/
│   ├── Documents/
│   ├── Projects/
│   └── root_file.pdf
└── logs/
```

## Command Line Options

```
python main.py [options]

Options:
  --service SERVICE     Which service to consolidate: photos, drive, or both (default: photos)
  --zip-dir PATH       Directory containing zip files (default: your path)
  --output-dir PATH    Where to store consolidated files (default: Consolidated)
  --dry-run           Show what would be done without doing it
  --help              Show this help message
```

## What Happens During Consolidation

1. **Discovery**: Finds all `.zip` files in your specified directory
2. **Service Detection**: Identifies Google Photos, Drive, or both in each zip
3. **Extraction**: Extracts each zip to a temporary location
4. **Analysis**: Locates the relevant service directories
5. **Consolidation**: Merges album/folder contents into unified structures
6. **Conflict Resolution**: Renames duplicate files safely
7. **Cleanup**: Removes temporary extraction files
8. **Reporting**: Shows detailed statistics

## File Naming

- **No conflict**: Files keep their original names
- **Name conflict**: Files get suffixes like `_001`, `_002`, etc.
- **Metadata preservation**: File timestamps and attributes are preserved
- **Google metadata**: JSON and HTML metadata files are automatically skipped

## Safety Features

- **Dry run mode**: Test before actual execution
- **No overwriting**: Conflicting files are renamed, never overwritten
- **Comprehensive logging**: Every action is logged
- **Progress reporting**: See what's happening in real-time
- **Error handling**: Continues processing even if some files fail
- **Service isolation**: Photos and Drive are kept in separate directories

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
- Sufficient disk space for temporary extraction

## Google Drive Specific Notes

Google Drive takeout files may use different directory names:
- `Takeout/Drive/` (newer format)
- `Takeout/My Drive/` (older format)

The tool automatically detects both formats and handles them correctly.

## Troubleshooting

### "No zip files found"
- Check that your directory path is correct
- Ensure zip files have `.zip` extension
- Verify you have read permissions

### "No Google Photos/Drive directory found"
- Some zip files might have different structures
- Check the logs to see what directories were found
- The tool will skip invalid zip files and continue

### Mixed Results
- If you have both Photos and Drive zips, use `--service both`
- Check the logs to see which service was detected in each zip

## Example Output

```
2023-11-03 14:30:22 - INFO - Starting Google Services consolidation
2023-11-03 14:30:22 - INFO - Service type: both
2023-11-03 14:30:22 - INFO - Found 6 zip files in /path/to/zips
2023-11-03 14:30:23 - INFO - Found Google Photos directory: /tmp/extract/Takeout/Google Photos
2023-11-03 14:30:24 - INFO - Found Google Drive directory: /tmp/extract/Takeout/Drive
...

============================================================
CONSOLIDATION STATISTICS
============================================================
Service type: both
Zip files processed: 6
Photo albums found: 8
Drive folders found: 12
Files copied: 4,523
Files skipped: 0
Errors encountered: 0

Photo albums consolidated:
  - Family Events
  - Vacation Photos
  - Wedding 2023

Drive folders consolidated:
  - Documents
  - Projects
  - Work Files
============================================================
```

## Migration from Photos-Only Version

If you were using the previous Google Photos-only version:

1. **Same commands work**: `--service photos` gives you the same behavior
2. **Same output structure**: Google Photos go to `Google Photos/` folder
3. **New capabilities**: Add `--service drive` or `--service both` for more services

This enhanced version is fully backward compatible with your existing workflows!