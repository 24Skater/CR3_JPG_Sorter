# CR3 and JPG Sorter

![Version](https://img.shields.io/github/v/release/24Skater/CR3_JPG_Sorter?style=flat-square)
![License](https://img.shields.io/github/license/24Skater/CR3_JPG_Sorter?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows-blue?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square)

**Version 2.2.0 released! UX Enhancements: Undo/Rollback, Drag & Drop, and Statistics Dashboard.**

This project sorts camera image files into organized folders by file type, with a simple desktop GUI and PowerShell script.

## What's New in v2.2.0

**UX Enhancements:**
- ⟲ **Undo/Rollback** - Reverse your last sort operation with one click
- 🎯 **Drag & Drop** - Drop folders directly onto the window
- 📊 **Statistics Dashboard** - See detailed breakdown by file type after sorting

**Previous (v2.1.0) High Priority Enhancements:**
- 🔍 Preview Mode | ⚡ Background Threading | ❌ Cancel Button
- 📝 Comprehensive Logging | ⚙️ Configuration Management | 🛡️ Better Error Handling

[See CHANGELOG.md for full details](CHANGELOG.md)

## Features
- Sorts images by type (CR3, JPG, NEF, etc.) into corresponding folders.
- Supports many DSLR/mirrorless camera formats (CR2, CR3, NEF, ARW, DNG, TIFF, etc.).
- **Undo/Rollback** - Reverse your last sort operation with one click.
- **Drag & Drop** - Drop folders directly onto the window.
- **Statistics Dashboard** - Detailed breakdown by file type after sorting.
- **Preview mode** - See what will be moved before executing.
- **Background threading** - GUI remains responsive during operations.
- **Cancel button** - Stop sorting at any time.
- **Custom file extensions** - Add your own file types via configuration.
- **Comprehensive logging** - All operations logged to file for troubleshooting.
- **Configuration management** - Remembers your preferences and last used folder.
- Optionally moves unsupported files to an 'Other' folder.
- Recursive sorting (with skip for already sorted folders).
- Progress bar, file count preview, and robust error handling.
- Modular Python code (GUI and core logic separated).
- Windows installer with Start Menu and desktop shortcut support.

## Quick Start (Python GUI)
1. **Requirements:** Python 3.8+ and install dependencies:
   ```
   pip install tkinterdnd2
   ```
2. **Run the app:**
   ```
   python ImageSorterGUI_v4.py
   ```
3. **Usage:**
   - **Drag & drop** a folder onto the window, or click 'Browse' to select.
   - (Optional) Check 'Include subfolders (recursive)' to sort recursively.
   - (Optional) Check 'Move unsupported files to Other folder'.
   - Click 'Preview' to see what will be moved (recommended first time).
   - Click 'Sort Images' to perform the sort operation.
   - View **statistics** after sorting showing breakdown by type.
   - Use '**Undo Last Sort**' button to reverse if needed.
   - Use 'Cancel' to stop during sorting.
   - Check `logs/` folder for detailed operation logs.

## Configuration
The app stores preferences in `config.json`:
- Last used folder
- Checkbox states (recursive, move_other)
- Window size and position
- Custom file extensions

To add custom file extensions, edit `config.json` and add to the `custom_extensions` array:
```json
{
  "custom_extensions": [".heic", ".webp"]
}
```

## Download

**[Download the latest installer from GitHub Releases](https://github.com/24Skater/CR3_JPG_Sorter/releases/latest)**

Or build from source:

## Packaging as an .exe
- Install PyInstaller:
  ```
  pip install pyinstaller
  ```
- Build the executable:
  ```
  python -m PyInstaller pyinstaller.spec
  ```
- The `.exe` will be in the `dist/ImageSorter/` folder.

## Creating a Windows Installer
- Use Inno Setup to create a professional installer with Start Menu and desktop shortcut support.
- Compile `imagesorter.iss` with Inno Setup after building the .exe.
- Output: `dist/ImageSorterSetup.exe`

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

### Main Window (v2.2.0)
![Main Window](screenshots/main-window-v2.2.png)
*Updated UI with Undo button and Drag & Drop support*

### Statistics Dashboard
![Statistics Dialog](screenshots/statistics-dialog.png)
*Detailed breakdown by file type after sorting*

### Undo Ready
![Undo Ready](screenshots/undo-ready.png)
*Undo button shows number of files that can be reversed*

### Legacy Screenshots
<details>
<summary>Click to view older screenshots</summary>

#### Original Main Window
![Main Window](screenshots/main-window.png)

#### Sorting Progress
![Sorting Progress](screenshots/sorting-progress.png)
</details>

---

