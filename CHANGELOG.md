# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Changed
- Reorganized project structure for better maintainability
  - Created `docs/` folder for documentation
  - Created `screenshots/` folder for images
  - Created `archive/` folder for old GUI versions
  - Cleaned up root directory
  - Updated README paths for screenshots

## [2.2.0] - 2025-10-05
### Added - UX Enhancements
- **Undo/Rollback System** - TransactionManager tracks all file moves
  - Undo button reverses last sort operation
  - Shows number of files that can be undone
  - Transaction log saved to `last_transaction.json`
  - Handles errors gracefully (files moved/deleted)
- **Drag & Drop Support** - Drop folders directly onto GUI window
  - Visual hint at top of window
  - Uses tkinterdnd2 library
  - Falls back gracefully if library not available
- **Statistics Dashboard** - Shows detailed results after sorting
  - Breakdown by file type (CR3, JPG, etc.)
  - Shows total sorted and skipped counts
  - Persistent display in GUI
  - Also shown in completion dialog
- Added 3 new screenshots showcasing v2.2.0 features

### Changed
- Updated GUI to v4 (ImageSorterGUI_v4.py)
- Enhanced completion dialog with statistics
- Improved visual feedback throughout app
- Window size increased to accommodate new features (520x480)

### Technical
- Added TransactionManager.py module for undo functionality
- Updated ImageSorterCore.py to record transactions
- Added tkinterdnd2 as a dependency
- Updated .gitignore to exclude transaction files
- All new code fully type-annotated

## [2.1.0] - 2025-10-05
### Added
- **Logging system** with rotating file handlers and detailed operation logs
- **Configuration management** system that saves user preferences (folder, options, window size)
- **Custom file extension support** via config.json
- **Preview mode** to see file movements before executing
- **Background threading** for responsive GUI during operations
- **Cancel button** to stop sorting operations
- Comprehensive error handling with specific exception types
- Better validation of folder paths and permissions
- Added badges to README (version, license, platform, Python version)
- Added screenshots to README (main window and sorting progress)
- Added UPGRADE_GUIDE.md for migration documentation (see docs/)
- Added HIGH_PRIORITY_SUMMARY.md for developer reference (see docs/)

### Changed
- Improved error messages with more specific details
- Enhanced logging with timestamps and severity levels
- Updated README with new features and configuration documentation
- Fixed requirements.txt format
- Updated pyinstaller.spec to use ImageSorterGUI_v3.py
- Updated Inno Setup script for v2.1.0

### Technical
- Refactored core with proper docstrings and type hints
- Added Logger.py module for centralized logging
- Added Config.py module for configuration management
- Created ImageSorterGUI_v3.py with all new features
- All modules fully type-annotated
- ~600 lines of production code added

## [2.0.0] - 2025-10-05
### Major Overhaul
- Complete rewrite and modularization of the codebase.
- Added a modern Python Tkinter GUI for sorting images by file type.
- Added support for many DSLR/mirrorless camera formats (CR2, CR3, NEF, ARW, DNG, TIFF, etc.).
- Optionally move unsupported files to an 'Other' folder.
- Recursive sorting with skip for already sorted folders.
- Progress bar, file count preview, and robust error handling.
- PowerShell script still included for CLI users.
- Added installer and packaging instructions, test script, and documentation improvements.
