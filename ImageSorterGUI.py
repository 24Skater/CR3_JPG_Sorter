import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Supported image extensions (case-insensitive)
IMAGE_EXTS = [
    '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2', '.orf', '.rw2',
    '.raf', '.pef', '.dng', '.tif', '.tiff', '.png', '.bmp', '.jpg', '.jpeg'
]

def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in IMAGE_EXTS

def move_to_filename_folder(filepath, dest_root):
    basename = os.path.splitext(os.path.basename(filepath))[0]
    ext = os.path.splitext(filepath)[1]
    dest_dir = os.path.join(dest_root, basename)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(filepath))
    # Avoid overwrite
    if os.path.abspath(filepath) == os.path.abspath(dest_path):
        return
    i = 1
    unique_dest_path = dest_path
    while os.path.exists(unique_dest_path):
        unique_dest_path = os.path.join(dest_dir, f"{basename} ({i}){ext}")
        i += 1
    shutil.move(filepath, unique_dest_path)

def sort_images(folder, status_callback):
    count = 0
    for entry in os.listdir(folder):
        full_path = os.path.join(folder, entry)
        if os.path.isfile(full_path) and is_image_file(entry):
            move_to_filename_folder(full_path, folder)
            count += 1
    status_callback(f"Done. Sorted {count} image files.")

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorter")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        self.folder_path = tk.StringVar()
        self.status = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select folder to sort images:", font=("Segoe UI", 12)).pack(pady=10)
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.folder_path, width=35, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)
        tk.Button(self.root, text="Sort Images", command=self.sort_images, font=("Segoe UI", 11, "bold"), bg="#4CAF50", fg="white").pack(pady=15)
        tk.Label(self.root, textvariable=self.status, font=("Segoe UI", 10), fg="blue").pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.status.set("")

    def sort_images(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        try:
            sort_images(folder, self.status.set)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorterApp(root)
    root.mainloop()
