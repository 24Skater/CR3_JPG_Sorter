# CR3 and JPG Sorter

This project sorts camera image files into organized folders by file type, with a simple desktop GUI and PowerShell script.

## Features
- Sorts images by type (CR3, JPG, NEF, etc.) into corresponding folders.
- Supports many DSLR/mirrorless camera formats (CR2, CR3, NEF, ARW, DNG, TIFF, etc.).
- Optionally moves unsupported files to an 'Other' folder.
- Recursive sorting (with skip for already sorted folders).
- Progress bar, file count preview, and robust error handling.
- Modular Python code (GUI and core logic separated).

## Quick Start (Python GUI)
1. **Requirements:** Python 3.8+ (Tkinter is included with standard Python).
2. **Run the app:**
   ```
   python ImageSorterGUI.py
   ```
3. **Usage:**
   - Click 'Browse' to select a folder.
   - (Optional) Check 'Include subfolders (recursive)' to sort recursively.
   - (Optional) Check 'Move unsupported files to Other folder'.
   - Click 'Sort Images'.
   - See progress and results in the app window.

## Packaging as an .exe
- Install PyInstaller:
  ```
  pip install pyinstaller
  ```
- Build the executable:
  ```
  pyinstaller pyinstaller.spec
  ```
- The `.exe` will be in the `dist/` folder.

## PowerShell Script
- `CR3andJPGMover.ps1`: Moves CR3 and JPG/JPEG files into `CR3` and `JPG` subfolders, respectively.

## Tests
- Run the test script:
  ```
  python test_sorter.py
  ```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog
See [CHANGELOG.md](CHANGELOG.md).

## Screenshots
*Add screenshots of the GUI here!*

---

