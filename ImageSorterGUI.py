import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Supported image extensions (case-insensitive)
IMAGE_EXTS = [
    '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2', '.orf', '.rw2',
    '.raf', '.pef', '.dng', '.tif', '.tiff', '.png', '.bmp', '.jpg', '.jpeg'
]

def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in IMAGE_EXTS

def move_to_type_folder(filepath, dest_root):
    ext = os.path.splitext(filepath)[1].lower()
    if ext.startswith('.'):
        ext_folder = ext[1:].upper()
    else:
        ext_folder = ext.upper()
    dest_dir = os.path.join(dest_root, ext_folder)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(filepath))
    # Avoid overwrite
    if os.path.abspath(filepath) == os.path.abspath(dest_path):
        return
    i = 1
    unique_dest_path = dest_path
    while os.path.exists(unique_dest_path):
        base = os.path.splitext(os.path.basename(filepath))[0]
        unique_dest_path = os.path.join(dest_dir, f"{base} ({i}){ext}")
        i += 1
    shutil.move(filepath, unique_dest_path)

def get_image_files(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and is_image_file(f)]

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorter")
        self.root.geometry("420x260")
        self.root.resizable(False, False)
        self.folder_path = tk.StringVar()
        self.status = tk.StringVar()
        self.file_count = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select folder to sort images:", font=("Segoe UI", 12)).pack(pady=10)
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.folder_path, width=35, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)
        tk.Label(self.root, textvariable=self.file_count, font=("Segoe UI", 10), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Sort Images", command=self.sort_images, font=("Segoe UI", 11, "bold"), bg="#4CAF50", fg="white").pack(pady=10)
        self.progressbar = ttk.Progressbar(self.root, variable=self.progress, maximum=100, length=300)
        self.progressbar.pack(pady=2)
        tk.Label(self.root, textvariable=self.status, font=("Segoe UI", 10), fg="blue").pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.status.set("")
            self.update_file_count()
            self.progress.set(0)

    def update_file_count(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            self.file_count.set("")
            return
        files = get_image_files(folder)
        self.file_count.set(f"{len(files)} image files will be sorted.")

    def sort_images(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        files = get_image_files(folder)
        total = len(files)
        if total == 0:
            self.status.set("No image files to sort.")
            return
        self.progress.set(0)
        self.progressbar.update()
        count = 0
        for i, entry in enumerate(files, 1):
            full_path = os.path.join(folder, entry)
            move_to_type_folder(full_path, folder)
            count += 1
            self.progress.set(i * 100 / total)
            self.progressbar.update()
        self.status.set(f"Done. Sorted {count} image files.")
        self.update_file_count()
        self.progress.set(100)
        self.progressbar.update()
        messagebox.showinfo("Complete", f"Done. Sorted {count} image files.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorterApp(root)
    root.mainloop()
