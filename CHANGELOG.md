# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Start tracking all changes in this changelog.
- Updated Python GUI to sort images by file type (extension folder, e.g., CR3, JPG, NEF) instead of by filename folder.
- Enhanced user experience in the GUI:
  - Show a preview of how many files will be sorted before running.
  - Added a progress bar that updates as files are sorted.
  - Show a popup notification when sorting is complete.
- Added recursive sorting option to the GUI, which skips folders named after any type (e.g., CR3, JPG, NEF, etc.) to avoid re-sorting already sorted files.

## [2025-10-05]
### Added
- Created a Python Tkinter GUI (`ImageSorterGUI.py`) for sorting images by filename folder.
- Expanded supported image file types to include CR2, CR3, NEF, NRW, ARW, SRF, SR2, ORF, RW2, RAF, PEF, DNG, TIFF, PNG, BMP, JPG, JPEG, and more.
- Updated `README.md` to reflect new GUI and features.
