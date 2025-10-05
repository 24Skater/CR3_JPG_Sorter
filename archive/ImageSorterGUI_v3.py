import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from typing import List, Tuple
import threading
from Logger import logger
from Config import config
from ImageSorterCore import (
    IMAGE_EXTS, TYPE_FOLDERS, is_image_file, move_to_type_folder, 
    move_to_other_folder, get_files, get_image_extensions
)

class ImageSorterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Image Sorter v2.0")
        self.root.geometry(config.get("window_geometry", "500x420"))
        self.root.resizable(False, False)
        
        # State variables
        self.folder_path = tk.StringVar(value=config.get("last_folder", ""))
        self.status = tk.StringVar()
        self.file_count = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.recursive = tk.BooleanVar(value=config.get("recursive", False))
        self.move_other = tk.BooleanVar(value=config.get("move_other", False))
        
        # Threading state
        self.is_sorting = False
        self.cancel_requested = False
        self.sort_thread = None
        
        # Preview data
        self.preview_data: List[Tuple[str, str]] = []
        
        self.create_widgets()
        logger.info("ImageSorter GUI initialized")
        
        # Update file count if last folder exists
        if self.folder_path.get() and os.path.isdir(self.folder_path.get()):
            self.update_file_count()
    
    def create_widgets(self) -> None:
        tk.Label(self.root, text="Select folder to sort images:", font=("Segoe UI", 12)).pack(pady=10)
        
        # Folder selection frame
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.folder_path, width=35, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)
        
        # Options
        tk.Checkbutton(self.root, text="Include subfolders (recursive)", 
                      variable=self.recursive, command=self.on_options_changed).pack(pady=2)
        tk.Checkbutton(self.root, text="Move unsupported files to 'Other' folder", 
                      variable=self.move_other, command=self.on_options_changed).pack(pady=2)
        
        # File count preview
        tk.Label(self.root, textvariable=self.file_count, font=("Segoe UI", 10), fg="gray").pack(pady=2)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.preview_btn = tk.Button(btn_frame, text="Preview", command=self.preview_sort, 
                                     font=("Segoe UI", 10), bg="#2196F3", fg="white", width=10)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.sort_btn = tk.Button(btn_frame, text="Sort Images", command=self.start_sort, 
                                 font=("Segoe UI", 11, "bold"), bg="#4CAF50", fg="white", width=12)
        self.sort_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.cancel_sort, 
                                    font=("Segoe UI", 10), bg="#f44336", fg="white", 
                                    width=10, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progressbar = ttk.Progressbar(self.root, variable=self.progress, maximum=100, length=400)
        self.progressbar.pack(pady=5)
        
        # Status
        tk.Label(self.root, textvariable=self.status, font=("Segoe UI", 10), fg="blue").pack(pady=5)
        
        # Save window geometry on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def browse_folder(self) -> None:
        folder = filedialog.askdirectory(initialdir=self.folder_path.get())
        if folder:
            self.folder_path.set(folder)
            config.set("last_folder", folder)
            self.status.set("")
            self.update_file_count()
            self.progress.set(0)
            logger.info(f"Selected folder: {folder}")
    
    def on_options_changed(self) -> None:
        """Called when options checkboxes change."""
        config.set("recursive", self.recursive.get())
        config.set("move_other", self.move_other.get())
        self.update_file_count()
    
    def update_file_count(self) -> None:
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            self.file_count.set("")
            return
        
        try:
            files = get_files(folder, self.recursive.get())
            count = 0
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                all_exts = get_image_extensions()
                if is_image_file(f) or (self.move_other.get() and os.path.isfile(f) and ext not in all_exts):
                    count += 1
            self.file_count.set(f"{count} files will be sorted.")
        except Exception as e:
            logger.error(f"Error counting files: {e}")
            self.file_count.set("Error counting files")
    
    def preview_sort(self) -> None:
        """Show preview of what files will be moved where."""
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        
        logger.info("Generating preview...")
        self.status.set("Generating preview...")
        self.root.update()
        
        try:
            files = get_files(folder, self.recursive.get())
            preview_data = []
            
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                all_exts = get_image_extensions()
                
                if is_image_file(f):
                    from ImageSorterCore import ext_to_folder
                    dest_folder = ext_to_folder(ext)
                    dest = os.path.join(folder, dest_folder, os.path.basename(f))
                    preview_data.append((f, dest))
                elif self.move_other.get() and os.path.isfile(f) and ext not in all_exts:
                    dest = os.path.join(folder, 'Other', os.path.basename(f))
                    preview_data.append((f, dest))
            
            if not preview_data:
                self.status.set("No files to sort.")
                messagebox.showinfo("Preview", "No files to sort.")
                return
            
            self.show_preview_window(preview_data)
            self.status.set("Preview generated")
            logger.info(f"Preview generated with {len(preview_data)} files")
            
        except Exception as e:
            logger.error(f"Error generating preview: {e}")
            messagebox.showerror("Error", f"Failed to generate preview: {e}")
            self.status.set("Preview failed")
    
    def show_preview_window(self, preview_data: List[Tuple[str, str]]) -> None:
        """Display preview window with source -> destination mappings."""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Preview - Files to be sorted")
        preview_window.geometry("700x500")
        
        tk.Label(preview_window, text=f"Preview: {len(preview_data)} files will be moved", 
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        # Scrolled text widget
        text_widget = scrolledtext.ScrolledText(preview_window, width=80, height=25, font=("Consolas", 9))
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        for src, dest in preview_data:
            src_rel = os.path.relpath(src, self.folder_path.get())
            dest_rel = os.path.relpath(dest, self.folder_path.get())
            text_widget.insert(tk.END, f"{src_rel}\n  → {dest_rel}\n\n")
        
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(preview_window, text="Close", command=preview_window.destroy, 
                 font=("Segoe UI", 10)).pack(pady=10)
    
    def start_sort(self) -> None:
        """Start sorting in background thread."""
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        
        if self.is_sorting:
            messagebox.showwarning("Warning", "Sorting is already in progress.")
            return
        
        # Confirm action
        response = messagebox.askyesno(
            "Confirm Sort", 
            f"Sort images in '{folder}'?\n\nThis operation will move files into subfolders.",
            icon='question'
        )
        if not response:
            return
        
        logger.info(f"Starting sort operation for: {folder}")
        
        # Disable buttons
        self.is_sorting = True
        self.cancel_requested = False
        self.sort_btn.config(state=tk.DISABLED)
        self.preview_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        
        # Start sorting in background thread
        self.sort_thread = threading.Thread(target=self.sort_images_thread, args=(folder,), daemon=True)
        self.sort_thread.start()
    
    def sort_images_thread(self, folder: str) -> None:
        """Sorting operation running in background thread."""
        try:
            files = get_files(folder, self.recursive.get())
            to_sort = []
            
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                all_exts = get_image_extensions()
                if is_image_file(f) or (self.move_other.get() and os.path.isfile(f) and ext not in all_exts):
                    to_sort.append(f)
            
            total = len(to_sort)
            if total == 0:
                self.root.after(0, lambda: self.status.set("No files to sort."))
                self.root.after(0, self.sorting_complete, 0, [])
                return
            
            self.root.after(0, lambda: self.progress.set(0))
            count = 0
            skipped = []
            
            for i, full_path in enumerate(to_sort, 1):
                # Check for cancellation
                if self.cancel_requested:
                    logger.info("Sort operation cancelled by user")
                    self.root.after(0, lambda: self.status.set("Sort cancelled"))
                    self.root.after(0, self.sorting_complete, count, skipped, cancelled=True)
                    return
                
                ext = os.path.splitext(full_path)[1].lower()
                if is_image_file(full_path):
                    ok, err = move_to_type_folder(full_path, folder)
                else:
                    ok, err = move_to_other_folder(full_path, folder)
                
                if ok:
                    count += 1
                else:
                    skipped.append(f"{os.path.basename(full_path)}: {err}")
                
                # Update progress
                progress_val = i * 100 / total
                self.root.after(0, lambda p=progress_val: self.progress.set(p))
                self.root.after(0, lambda c=count: self.status.set(f"Sorted {c} files..."))
            
            logger.info(f"Sort complete. Moved: {count}, Skipped: {len(skipped)}")
            self.root.after(0, self.sorting_complete, count, skipped)
            
        except Exception as e:
            logger.error(f"Error during sort operation: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Sort failed: {e}"))
            self.root.after(0, self.sorting_complete, 0, [])
    
    def sorting_complete(self, count: int, skipped: List[str], cancelled: bool = False) -> None:
        """Called when sorting completes or is cancelled."""
        self.is_sorting = False
        self.sort_btn.config(state=tk.NORMAL)
        self.preview_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress.set(100 if not cancelled else 0)
        
        if cancelled:
            self.status.set(f"Cancelled. Sorted {count} files before stopping.")
            return
        
        self.status.set(f"Done. Sorted {count} files.")
        self.update_file_count()
        
        msg = f"Done. Sorted {count} files."
        if skipped:
            msg += f"\n\nSkipped {len(skipped)} files:\n" + "\n".join(skipped[:10])
            if len(skipped) > 10:
                msg += f"\n... and {len(skipped) - 10} more."
        
        messagebox.showinfo("Complete", msg)
    
    def cancel_sort(self) -> None:
        """Request cancellation of sort operation."""
        if self.is_sorting:
            self.cancel_requested = True
            self.cancel_btn.config(state=tk.DISABLED)
            self.status.set("Cancelling...")
            logger.info("User requested cancel")
    
    def on_close(self) -> None:
        """Save config and close application."""
        if self.is_sorting:
            response = messagebox.askyesno(
                "Sorting in Progress", 
                "Sorting is in progress. Are you sure you want to quit?"
            )
            if not response:
                return
            self.cancel_requested = True
        
        # Save window geometry
        config.set("window_geometry", self.root.geometry())
        logger.info("Application closing")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    # Set window icon if icon.ico exists
    if os.path.exists('icon.ico'):
        root.iconbitmap('icon.ico')
    app = ImageSorterApp(root)
    root.mainloop()

