# CR3 and JPG Sorter

This project sorts camera image files into organized folders.

## PowerShell Script
- `CR3andJPGMover.ps1`: Moves CR3 and JPG/JPEG files into `CR3` and `JPG` subfolders, respectively.

## Python GUI (Coming Soon)
- A simple desktop GUI is being added using Python and Tkinter.
- The GUI will let you pick a folder and sort images with a click.
- Supported file types will include: CR2, CR3, NEF, NRW, ARW, SRF, SR2, ORF, RW2, RAF, PEF, DNG, TIFF, PNG, BMP, JPG, JPEG, and more.
- Each image will be moved into a subfolder named after its filename (e.g., `IMG_1234.CR3` → `IMG_1234/IMG_1234.CR3`).
- The GUI will be designed for easy packaging as a standalone `.exe` (e.g., with PyInstaller).

---

