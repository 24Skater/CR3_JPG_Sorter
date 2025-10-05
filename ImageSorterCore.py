import os
import shutil
from typing import List, Tuple, Optional, Set
from Logger import logger
from Config import config
from TransactionManager import transaction_manager

# Base image extensions
BASE_IMAGE_EXTS: List[str] = [
    '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2', '.orf', '.rw2',
    '.raf', '.pef', '.dng', '.tif', '.tiff', '.png', '.bmp', '.jpg', '.jpeg'
]

def get_image_extensions() -> List[str]:
    """Get all image extensions including custom ones from config."""
    return BASE_IMAGE_EXTS + config.get_custom_extensions()

IMAGE_EXTS: List[str] = get_image_extensions()
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
    """Check if file is a supported image type."""
    ext = os.path.splitext(filename)[1].lower()
    all_exts = get_image_extensions()
    return ext in all_exts

def move_to_type_folder(filepath: str, dest_root: str) -> Tuple[bool, Optional[str]]:
    """
    Move file to folder based on its type/extension.
    
    Args:
        filepath: Source file path
        dest_root: Root directory for sorting
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        ext = os.path.splitext(filepath)[1].lower()
        folder = ext_to_folder(ext)
        dest_dir = os.path.join(dest_root, folder)
        
        # Create destination directory
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create directory {dest_dir}: {e}")
            return False, f"Cannot create destination folder: {e}"
        
        dest_path = os.path.join(dest_dir, os.path.basename(filepath))
        
        # Skip if already in correct location
        if os.path.abspath(filepath) == os.path.abspath(dest_path):
            logger.debug(f"File already in correct location: {filepath}")
            return True, None
        
        # Find unique filename if duplicate exists
        i = 1
        unique_dest_path = dest_path
        while os.path.exists(unique_dest_path):
            base = os.path.splitext(os.path.basename(filepath))[0]
            unique_dest_path = os.path.join(dest_dir, f"{base} ({i}){ext}")
            i += 1
        
        # Attempt to move file
        shutil.move(filepath, unique_dest_path)
        logger.info(f"Moved: {filepath} -> {unique_dest_path}")
        
        # Record transaction for undo
        transaction_manager.add_transaction(filepath, unique_dest_path)
        
        return True, None
        
    except PermissionError as e:
        logger.warning(f"Permission denied: {filepath} - {e}")
        return False, f"Permission denied: {e}"
    except OSError as e:
        logger.warning(f"OS error moving {filepath}: {e}")
        return False, f"OS error: {e}"
    except Exception as e:
        logger.error(f"Unexpected error moving {filepath}: {e}")
        return False, f"Unexpected error: {e}"

def move_to_other_folder(filepath: str, dest_root: str) -> Tuple[bool, Optional[str]]:
    """
    Move unsupported file to 'Other' folder.
    
    Args:
        filepath: Source file path
        dest_root: Root directory for sorting
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        dest_dir = os.path.join(dest_root, 'Other')
        
        # Create destination directory
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create directory {dest_dir}: {e}")
            return False, f"Cannot create destination folder: {e}"
        
        ext = os.path.splitext(filepath)[1].lower()
        base = os.path.splitext(os.path.basename(filepath))[0]
        dest_path = os.path.join(dest_dir, os.path.basename(filepath))
        
        # Skip if already in correct location
        if os.path.abspath(filepath) == os.path.abspath(dest_path):
            logger.debug(f"File already in 'Other' folder: {filepath}")
            return True, None
        
        # Find unique filename if duplicate exists
        i = 1
        unique_dest_path = dest_path
        while os.path.exists(unique_dest_path):
            unique_dest_path = os.path.join(dest_dir, f"{base} ({i}){ext}")
            i += 1
        
        # Attempt to move file
        shutil.move(filepath, unique_dest_path)
        logger.info(f"Moved to Other: {filepath} -> {unique_dest_path}")
        
        # Record transaction for undo
        transaction_manager.add_transaction(filepath, unique_dest_path)
        
        return True, None
        
    except PermissionError as e:
        logger.warning(f"Permission denied: {filepath} - {e}")
        return False, f"Permission denied: {e}"
    except OSError as e:
        logger.warning(f"OS error moving {filepath}: {e}")
        return False, f"OS error: {e}"
    except Exception as e:
        logger.error(f"Unexpected error moving {filepath}: {e}")
        return False, f"Unexpected error: {e}"

def get_files(folder: str, recursive: bool = False) -> List[str]:
    """
    Get list of files in folder, optionally recursively.
    
    Args:
        folder: Folder path to scan
        recursive: Whether to scan subfolders
        
    Returns:
        List of file paths
    """
    if not os.path.exists(folder):
        logger.error(f"Folder does not exist: {folder}")
        return []
    
    if not os.path.isdir(folder):
        logger.error(f"Path is not a directory: {folder}")
        return []
    
    files: List[str] = []
    try:
        for root, dirs, filenames in os.walk(folder) if recursive else [(folder, [], os.listdir(folder))]:
            # Skip type folders and 'Other'
            dirs[:] = [d for d in dirs if d.upper() not in TYPE_FOLDERS and d != 'Other']
            for f in filenames:
                files.append(os.path.join(root, f))
        logger.debug(f"Found {len(files)} files in {folder} (recursive={recursive})")
    except PermissionError as e:
        logger.error(f"Permission denied accessing {folder}: {e}")
    except OSError as e:
        logger.error(f"OS error accessing {folder}: {e}")
    
    return files
