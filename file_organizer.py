import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm
import os
import shutil
import datetime


root = tk.Tk()
root.title("File Organizer")


dir_path1 = tk.StringVar()
selected_ext = tk.StringVar(value="*")  # Default: organize all files


tk.Label(root, text="Folder Path:").grid(row=0, column=0, sticky="w")
e1 = tk.Entry(root, textvariable=dir_path1, width=40)
e1.grid(row=0, column=1)



def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        dir_path1.set(folder)


tk.Button(root, text="Browse", command=browse_folder).grid(row=0, column=2)


tk.Label(root, text="Filter by extension (e.g., 'jpg'):").grid(row=1, column=0, sticky="w")
tk.Entry(root, textvariable=selected_ext, width=10).grid(row=1, column=1, sticky="w")



def log_error(error_msg):
    log_file = "file_organizer_errors.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {error_msg}\n")



def organize_files():
    dir_path = dir_path1.get()
    if not dir_path:
        messagebox.showerror("Error", "Please select a folder first!")
        return

    path_list = []
    path_dic = {}
    count = 0
    ext_filter = selected_ext.get().lower()

    print("Scanning files...")
    for path in tqdm(os.scandir(dir_path)):
        if path.is_file():
            ext = os.path.splitext(path.name)[1][1:].lower() or "no_extension"


            if ext_filter != "*" and ext != ext_filter:
                continue

            count += 1
            path_list.append(path.path)
            path_dic.setdefault(ext, []).append(path.path)

    if not path_dic:
        messagebox.showinfo("Info", "No matching files found!")
        return

    print("\nCreating subfolders...")
    for ext in tqdm(path_dic.keys()):
        folder_path = os.path.join(dir_path, ext)
        try:
            os.makedirs(folder_path, exist_ok=True)
        except Exception as e:
            error_msg = f"Error creating directory {folder_path}: {e}"
            print(f"\n{error_msg}")
            log_error(error_msg)

    print("\nMoving files...")
    moved_files = 0
    skipped_files = 0

    for ext, files in tqdm(path_dic.items()):
        dest_folder = os.path.join(dir_path, ext)

        for file_path in files:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(dest_folder, filename)

            try:
                if not os.path.exists(dest_path):
                    shutil.move(file_path, dest_folder)
                    moved_files += 1
                else:
                    skipped_files += 1
            except Exception as e:
                error_msg = f"Error moving {filename}: {e}"
                print(f"\n{error_msg}")
                log_error(error_msg)


    result_msg = f"Moved {moved_files} files, skipped {skipped_files} duplicates.\nTotal processed: {count}"
    print(f"\nDone! {result_msg}")
    messagebox.showinfo("Success!", result_msg)



tk.Button(root, text="Organize Files", command=organize_files).grid(row=2, columnspan=3, pady=10)

root.mainloop()