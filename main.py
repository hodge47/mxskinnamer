from tkinter import *
from tkinter import filedialog
from os import listdir
from os.path import isfile, join, splitext

# Create TKinter window and set the min size
root = Tk()
root.minsize(600, 480)

bikeDynos = {"Husqvarna 450": "fc450v2016", "Kawasaki 450": "fc450v2016"}

# Opens a TKinter directory browser and the calls populate listbox of directory if path not empty


def open_directory_browser():
    root.directory = filedialog.askdirectory()
    if root.directory != "":
        # Get files from directory
        files = get_files_in_directory(root.directory)
        populate_list_box(files, skinPathListbox)
    print(f"Working directory: {root.directory}")

# Get all the files in a given directory


def get_files_in_directory(dir):
    files = []
    for f in listdir(dir):
        file = join(dir, f)
        if isfile(file):
            filename, extension = splitext(f)
            if extension == ".png":
                files.append(file)
    if len(files) >= 2:
        files.sort()
    return files


def populate_list_box(items, listbox):
    # Delete all items in the listbox
    listbox.delete(0, END)
    # Insert file paths into listbox
    for f in items:
        listbox.insert(END, f)


def rename_skins():
    isSelection = bikeDynoListBox.curselection()
    if isSelection:
        dynoSelection = bikeDynoListBox.selection_get()
        dynoValue = None
        for item in bikeDynos:
            if dynoSelection == item:
                dynoValue = bikeDynos[dynoSelection]
        if dynoValue != None:
            print(dynoValue)
        else:
            print("The key supplied does not exist in the bikeDynos dictionary")
    else:
        print("There was not a selection")


Label(root, text="Skin Directory").pack(side=TOP, pady=10)
Button(root, text="Browse", command=open_directory_browser).pack(
    side=TOP, pady=10)
skinPathListbox = Listbox(root)
skinPathListbox.pack(fill=BOTH, expand=1)
Label(root, text="Bike Dyno").pack(side=TOP, pady=10)
bikeDynoListBox = Listbox(root)
bikeDynoListBox.pack(fill=BOTH, expand=1)
# Populate the bike dynos listbox
populate_list_box(bikeDynos.keys(), bikeDynoListBox)
Button(root, text="Rename", command=rename_skins).pack(side=TOP, pady=10)

root.mainloop()
