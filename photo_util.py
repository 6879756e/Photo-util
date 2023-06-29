import sys
import os
import shutil
import logging
from pathlib import Path

deletable_file_suffix = ["ds_store", "aae"]
target_file_suffix = ["jpg", "mp4"]

base_folder = None


def search_folder(folder_name: str):
    folder_abs_path = os.path.abspath(folder_name)
    files_in_folder = os.listdir(folder_abs_path)

    # Recursively looks for folders
    print("in", folder_abs_path, "is\n\t", " ".join(files_in_folder))
    for f in files_in_folder:
        file = os.path.join(folder_abs_path, f)
        file_suffix = f.split(".")[-1]
        if file_suffix.lower() in deletable_file_suffix:
            os.remove(file)

        if os.path.isdir(file):
            logging.debug(f + " is a directory so going to call search_folder recursively")
            print(f + " is a directory so going to call search_folder recursively")
            search_folder(file)

    if folder_name == base_folder:
        return

    # It is important that we call 'files_in_folder' again, as the files in the folder may have changed since the first
    # call. This is because the first loop can move img files from the nested folders up to the parent folder.
    files_in_folder = os.listdir(folder_abs_path)

    for f in files_in_folder:
        file = os.path.join(folder_abs_path, f)
        path = Path(file)
        file_suffix = f.split(".")[-1]

        if file_suffix.lower() in target_file_suffix:
            # move jpg files to parent's parent folder
            shutil.move(path, path.parent.parent)
            print("Moved file", file, "to", str(path.parent.parent))
            logging.debug("Moved file " + file + " to " + str(path.parent.parent))

    if not os.listdir(folder_abs_path):
        print("directory", folder_abs_path, "is empty so it will be deleted")
        shutil.rmtree(folder_abs_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] + " [folder_name]")
        exit(1)
    elif not os.listdir(sys.argv[1]):
        print("folder is empty")

    logging.basicConfig(filename="log.txt", level=logging.DEBUG)
    logging.debug("Start of debug file")

    base_folder = sys.argv[1]

    search_folder(base_folder)
