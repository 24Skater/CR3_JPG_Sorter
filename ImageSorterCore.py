import os
import shutil
from typing import List, Tuple, Optional, Set

IMAGE_EXTS: List[str] = [
    '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2', '.orf', '.rw2',
    '.raf', '.pef', '.dng', '.tif', '.tiff', '.png', '.bmp', '.jpg', '.jpeg'
]
TYPE_FOLDERS: Set[str] = set(ext[1:].upper() for ext in IMAGE_EXTS)
TYPE_FOLDERS.discard('JPEG')  # Only use JPG for both

def ext_to_folder(ext: str) -> str:
    ext = ext.lower()
    if ext in ('.jpg', '.jpeg'):
        return 'JPG'
    if ext.startswith('.'):
        return ext[1:].upper()
    return ext.upper()

def is_image_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in IMAGE_EXTS

def move_to_type_folder(filepath: str, dest_root: str) -> Tuple[bool, Optional[str]]:
    ext = os.path.splitext(filepath)[1].lower()
    folder = ext_to_folder(ext)
    dest_dir = os.path.join(dest_root, folder)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(filepath))
    if os.path.abspath(filepath) == os.path.abspath(dest_path):
        return True, None
    i = 1
    unique_dest_path = dest_path
    while os.path.exists(unique_dest_path):
        base = os.path.splitext(os.path.basename(filepath))[0]
        unique_dest_path = os.path.join(dest_dir, f"{base} ({i}){ext}")
        i += 1
    try:
        shutil.move(filepath, unique_dest_path)
        return True, None
    except Exception as e:
        return False, str(e)

def move_to_other_folder(filepath: str, dest_root: str) -> Tuple[bool, Optional[str]]:
    dest_dir = os.path.join(dest_root, 'Other')
    os.makedirs(dest_dir, exist_ok=True)
    ext = os.path.splitext(filepath)[1].lower()
    base = os.path.splitext(os.path.basename(filepath))[0]
    dest_path = os.path.join(dest_dir, os.path.basename(filepath))
    if os.path.abspath(filepath) == os.path.abspath(dest_path):
        return True, None
    i = 1
    unique_dest_path = dest_path
    while os.path.exists(unique_dest_path):
        unique_dest_path = os.path.join(dest_dir, f"{base} ({i}){ext}")
        i += 1
    try:
        shutil.move(filepath, unique_dest_path)
        return True, None
    except Exception as e:
        return False, str(e)

def get_files(folder: str, recursive: bool = False) -> List[str]:
    files: List[str] = []
    for root, dirs, filenames in os.walk(folder) if recursive else [(folder, [], os.listdir(folder))]:
        dirs[:] = [d for d in dirs if d.upper() not in TYPE_FOLDERS and d != 'Other']
        for f in filenames:
            files.append(os.path.join(root, f))
    return files
