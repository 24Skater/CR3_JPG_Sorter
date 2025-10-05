import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional
from ImageSorterCore import (
    IMAGE_EXTS, TYPE_FOLDERS, is_image_file, move_to_type_folder, move_to_other_folder, get_files
)

class ImageSorterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Image Sorter")
        self.root.geometry("480x340")
        self.root.resizable(False, False)
        self.folder_path = tk.StringVar()
        self.status = tk.StringVar()
        self.file_count = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.recursive = tk.BooleanVar(value=False)
        self.move_other = tk.BooleanVar(value=False)
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Select folder to sort images:", font=("Segoe UI", 12)).pack(pady=10)
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.folder_path, width=35, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)
        tk.Checkbutton(self.root, text="Include subfolders (recursive)", variable=self.recursive, command=self.update_file_count).pack(pady=2)
        tk.Checkbutton(self.root, text="Move unsupported files to 'Other' folder", variable=self.move_other, command=self.update_file_count).pack(pady=2)
        tk.Label(self.root, textvariable=self.file_count, font=("Segoe UI", 10), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Sort Images", command=self.sort_images, font=("Segoe UI", 11, "bold"), bg="#4CAF50", fg="white").pack(pady=10)
        self.progressbar = ttk.Progressbar(self.root, variable=self.progress, maximum=100, length=350)
        self.progressbar.pack(pady=2)
        tk.Label(self.root, textvariable=self.status, font=("Segoe UI", 10), fg="blue").pack(pady=5)

    def browse_folder(self) -> None:
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.status.set("")
            self.update_file_count()
            self.progress.set(0)

    def update_file_count(self) -> None:
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            self.file_count.set("")
            return
        files = get_files(folder, self.recursive.get())
        count = 0
        for f in files:
            ext = f.lower().rsplit('.', 1)[-1] if '.' in f else ''
            if is_image_file(f) or (self.move_other.get() and os.path.isfile(f) and os.path.splitext(f)[1].lower() not in IMAGE_EXTS):
                count += 1
        self.file_count.set(f"{count} files will be sorted.")

    def sort_images(self) -> None:
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        files = get_files(folder, self.recursive.get())
        to_sort = []
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if is_image_file(f) or (self.move_other.get() and os.path.isfile(f) and ext not in IMAGE_EXTS):
                to_sort.append(f)
        total = len(to_sort)
        if total == 0:
            self.status.set("No files to sort.")
            return
        self.progress.set(0)
        self.progressbar.update()
        count = 0
        skipped = []
        for i, full_path in enumerate(to_sort, 1):
            ext = os.path.splitext(full_path)[1].lower()
            if is_image_file(full_path):
                ok, err = move_to_type_folder(full_path, folder)
            else:
                ok, err = move_to_other_folder(full_path, folder)
            if ok:
                count += 1
            else:
                skipped.append(f"{os.path.basename(full_path)}: {err}")
            self.progress.set(i * 100 / total)
            self.progressbar.update()
        self.status.set(f"Done. Sorted {count} files.")
        self.update_file_count()
        self.progress.set(100)
        self.progressbar.update()
        msg = f"Done. Sorted {count} files."
        if skipped:
            msg += f"\n\nSkipped {len(skipped)} files:\n" + "\n".join(skipped)
        messagebox.showinfo("Complete", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorterApp(root)
    root.mainloop()
