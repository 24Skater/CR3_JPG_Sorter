# ImageSorter - Project Structure

## Overview

**ImageSorter** is a professional Python-based image sorting application with a modern GUI, undo functionality, and Windows installer. It organizes camera files (RAW and JPEG formats) into folders by file type.

---

## Root Directory

### Core Application Files
- **ImageSorterGUI_v4.py** - Main GUI application (current version)
- **ImageSorterCore.py** - Core sorting logic and file operations
- **Logger.py** - Logging system with rotating file handlers
- **Config.py** - Configuration management system
- **TransactionManager.py** - Undo/rollback functionality

### Legacy/Alternative
- **CR3andJPGMover.ps1** - PowerShell script (CLI alternative)

### Build Files
- **pyinstaller.spec** - PyInstaller configuration for building .exe
- **imagesorter.iss** - Inno Setup script for creating installer

### Testing
- **test_sorter.py** - Unit tests for core functionality

### Configuration
- **requirements.txt** - Python dependencies
- **icon.ico** - Application icon

### Documentation (Root)
- **README.md** - Main project documentation
- **CHANGELOG.md** - Version history and changes
- **CONTRIBUTING.md** - Contribution guidelines
- **LICENSE** - MIT License

---

## Folders

### `/docs/`
Developer documentation and release notes:
- **HIGH_PRIORITY_SUMMARY.md** - Technical summary of v2.1.0 enhancements
- **UPGRADE_GUIDE.md** - Migration guide for users
- **RELEASE_NOTES_v2.1.0.md** - v2.1.0 release notes
- **RELEASE_NOTES_v2.2.0.md** - v2.2.0 release notes

### `/screenshots/`
Application screenshots for documentation:
- **main-window-v2.2.png** - Current main window (v2.2.0)
- **statistics-dialog.png** - Statistics dashboard
- **undo-ready.png** - Undo functionality
- **main-window.png** - Legacy main window
- **sorting-progress.png** - Legacy progress view

### `/archive/`
Previous versions of the GUI (for reference):
- **ImageSorterGUI.py** - Original v2.0.0 GUI
- **ImageSorterGUI_v3.py** - v2.1.0 GUI
- **README.md** - Archive documentation

### `/logs/` (created at runtime)
Application log files:
- **imagesorter_YYYYMMDD.log** - Daily log files (rotating)

### `/build/` (created during build)
PyInstaller temporary build files

### `/dist/` (created during build)
Distribution files:
- **ImageSorter/** - Portable application folder
- **ImageSorterSetup.exe** - Windows installer

---

## Ignored Files (.gitignore)

### User-Generated
- `config.json` - User preferences
- `last_transaction.json` - Undo transaction log
- `logs/` - Application logs

### Build Artifacts
- `build/`, `dist/`
- `__pycache__/`
- `*.pyc`, `*.pyo`
- `*.egg-info/`

---

## Module Dependencies

```
ImageSorterGUI_v4.py
├── ImageSorterCore.py
│   ├── Logger.py
│   ├── Config.py
│   └── TransactionManager.py
├── Logger.py
├── Config.py
└── TransactionManager.py
```

---

## Development Workflow

1. **Make changes** to Python files
2. **Test** with `python ImageSorterGUI_v4.py`
3. **Run tests** with `python test_sorter.py`
4. **Build .exe** with `python -m PyInstaller pyinstaller.spec`
5. **Create installer** with Inno Setup (compile `imagesorter.iss`)
6. **Update CHANGELOG.md**
7. **Commit and release**

---

## Version History

- **v1.0.0** - PowerShell script
- **v2.0.0** - Initial Python GUI
- **v2.1.0** - High Priority Enhancements (Preview, Threading, Logging, Config)
- **v2.2.0** - UX Enhancements (Undo, Drag & Drop, Statistics)

---

## Key Features by Version

### v2.0.0
- Basic GUI
- Sort by file type
- Recursive sorting
- Progress bar

### v2.1.0
- Preview mode
- Background threading
- Cancel button
- Comprehensive logging
- Configuration management
- Custom file extensions

### v2.2.0
- Undo/Rollback system
- Drag & Drop support
- Statistics Dashboard
- Enhanced UI

---

Last Updated: v2.2.0 (2025-10-05)

