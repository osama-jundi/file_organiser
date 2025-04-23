import os
import shutil
path_list = []
path_dic = {}
count = 0
dir_path = r"D:\telegram desktop"


for path in os.scandir(dir_path):
    if path.is_file():
        count += 1
        path_list.append(path.path)


for path in path_list:
    ext = os.path.splitext(path)[1][1:]
    if ext:
        path_dic[ext] = path


for ext in path_dic:
    folder_path = os.path.join(dir_path, ext)
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass
    except Exception as e:
        print(f"Error creating directory {folder_path}: {e}")


for path in path_list:
    ext = os.path.splitext(path)[1][1:]
    if ext:
        dest_folder = os.path.join(dir_path, ext)
        try:
            shutil.move(path, dest_folder)
        except Exception as e:
            print(f"File {path} not moved: {e}")

print('File count:', count)
