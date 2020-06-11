from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import os
from os import listdir
from os.path import isfile, join, splitext

# Create TKinter window and set the min size
root = Tk()
root.minsize(600, 480)

bikeDynos = {"Honda (450f)": "crf450v2017", "Husqvarna (450f)": "fc450v2016",
             "Kawasaki (450f)": "kx450fv2016", "KTM (450f)": "450sxfv2016", "Suzuki (450f)": "rmz450v2018", "Yamaha (450f)": "yz450fv2014", "KTM (350f)": "350sxfv2016", "Honda (250f)": "crf250v2018", "Husqvarna (250f)": "fc250v2016", "Kawasaki (250f)": "kx250fv2017", "KTM (250f)": "250sxfv2016", "Suzuki (250f)": "rmz250v2010", "Yamaha (250f)": "yz250fv2014"}

# Opens a TKinter directory browser and the calls populate listbox of directory if path not empty


def open_directory_browser():
    root.directory = filedialog.askdirectory()
    if root.directory != "":
        # Get files from directory
        files = get_files_in_directory(root.directory)
        populate_list_box(files, skinPathListbox)
    skinDirLabel["text"] = f"Skin Directory: {root.directory}"

# Get all the files in a given directory


def get_files_in_directory(dir):
    files = []
    for f in listdir(dir):
        file = join(dir + "/" + f)
        if isfile(file):
            filename, extension = splitext(f)
            if extension == ".png":
                files.append(file)
    if len(files) >= 2:
        files.sort()
    return files


def populate_list_box(items, listbox):
    # Delete all items in the listbox
    clear_list_box(listbox)
    # Insert file paths into listbox
    for f in items:
        listbox.insert(END, f)


def clear_list_box(listbox):
    listbox.delete(0, END)


def sort_map_paths():
    normalMapPath = None
    specMapPath = None
    diffuseMapPaths = []

    isSelection = bikeDynoListBox.curselection()
    if isSelection:
        dynoSelection = bikeDynoListBox.selection_get()
        dynoValue = None
        for item in bikeDynos:
            if dynoSelection == item:
                dynoValue = bikeDynos[dynoSelection]
        if dynoValue != None:
            items = skinPathListbox.get(0, END)

            for i in range(0, len(items)):
                # Normal map
                if "norm" in items[i] or "Norm" in items[i]:
                    if messagebox.askyesno("Is this your normal map?", items[i]):
                        normalMapPath = items[i]
                        print(f"Noraml map path: {normalMapPath}")
                # Spec map
                elif "spec" in items[i] or "Spec" in items[i]:
                    if messagebox.askyesno("Is this your specular map?", items[i]):
                        specMapPath = items[i]
                        print(f"Spec map path: {specMapPath}")
                # Diffuse maps
                else:
                    diffuseMapPaths.append(items[i])
                    print(f"Diffuse map: {items[i]}")
            return (normalMapPath, specMapPath, diffuseMapPaths)
        else:
            return ("", "", "")
            print("The key supplied does not exist in the bikeDynos dictionary")
    else:
        return ("", "", "")
        print("There was not a selection")


def rename_skins():
    # Check to see if skins listbox is empty
    isSelection = skinPathListbox.get(0)
    if not isSelection:
        print("You need to choose a skins directory!")
        return
    # Check to see if model name is blank
    if modelName.get() == "":
        print("You need to enter a model name! Check the JM's to get it.")
        return
    # Check to see if there is a listbox selection
    isSelection = bikeDynoListBox.curselection()
    if not isSelection:
        print("You need to select a dyno!")
        return

    sortedMapPaths = sort_map_paths()

    normalMapPath = sortedMapPaths[0]
    specMapPath = sortedMapPaths[1]
    diffuseMaps = sortedMapPaths[2]

    # Clear the skins list box
    clear_list_box(skinPathListbox)

    # Norm rename
    rename_map(normalMapPath, "norm")
    # Spec rename
    rename_map(specMapPath, "spec")
    # Diffuse maps
    for f in diffuseMaps:
        rename_map(f, "diffuse")


def rename_map(path, special):
    # Separate directory from file path
    pathSplit = path.rsplit("/", 1)
    newPath = pathSplit[0] + "/"
    filename = pathSplit[1].rsplit(".", 1)[0]
    # Do this split if file halfway named
    if "-" in filename:
        filename = filename.rsplit("-", 1)[1]
    # Get bike dyno
    dynoSelection = bikeDynoListBox.selection_get()
    dynoValue = None
    for item in bikeDynos:
        if dynoSelection == item:
            dynoValue = bikeDynos[dynoSelection]
    # Rename the maps
    if special == "norm":
        os.rename(path, f"{newPath}{dynoValue}-{modelName.get()}_norm.png")
    elif special == "spec":
        os.rename(path, f"{newPath}{dynoValue}-{modelName.get()}_spec.png")
    else:
        os.rename(
            path, f"{newPath}{dynoValue}-{modelName.get()}-{filename}.png")


# Skin directory elements
skinDirLabel = Label(root, text="Skin Directory")
skinDirLabel.pack(side=TOP, pady=10)
Button(root, text="Browse", command=open_directory_browser).pack(
    side=TOP, pady=10)
skinPathListbox = Listbox(root)
skinPathListbox.pack(fill=BOTH, expand=1)
# Model detail elements
Label(root, text="Model Name").pack(side=TOP, pady=10)
modelName = StringVar()
modelNameEntered = Entry(root, width=50, textvariable=modelName)
modelNameEntered.pack(side=TOP, pady=10)
# Bike dyno elements
Label(root, text="Bike Dyno").pack(side=TOP, pady=10)
scrollbar = Scrollbar(root, orient=VERTICAL)
bikeDynoListBox = Listbox(root, yscrollcommand=scrollbar.set)
scrollbar.config(command=bikeDynoListBox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
bikeDynoListBox.pack(fill=BOTH, expand=1)
# Populate the bike dynos listbox
populate_list_box(bikeDynos.keys(), bikeDynoListBox)
Button(root, text="Rename", command=rename_skins).pack(
    side=TOP, pady=10)

root.mainloop()
