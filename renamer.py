from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import os, shutil, subprocess
from os import listdir
from os import path
from os.path import isfile, join, splitext

root = Tk()
root.minsize(640, 640)
root.resizable(0, 0)
root.title("MXSkinNamer")
root.directory = None

dynosList = {"Honda (450f)": "crf450v2017", "Husqvarna (450f)": "fc450v2016",
             "Kawasaki (450f)": "kx450fv2016", "KTM (450f)": "450sxfv2016", "Suzuki (450f)": "rmz450v2018", "Yamaha (450f)": "yz450fv2014", "KTM (350f)": "350sxfv2016", "Honda (250f)": "crf250v2018", "Husqvarna (250f)": "fc250v2016", "Kawasaki (250f)": "kx250fv2017", "KTM (250f)": "250sxfv2016", "Suzuki (250f)": "rmz250v2010", "Yamaha (250f)": "yz250fv2014", "Honda (250t)": "cr250", "Kawasaki (250t)": "kx250", "KTM (250t)": "250sx", "Suzuki (250t)": "rm250", "Yamaha (250t)": "yz250", "Honda (125)": "cr125", "Kawasaki (125)": "kx125", "KTM (125)": "125sx", "Yamaha (125)": "yz125", "Suzuki (125)": "rm125", "Rider Body": "rider_body", "Helmet": "rider_head", "Wheels": "wheels"}
jmParts = {"fork_lower", "fork_upper", "frame", "swingarm",
           "side_plates", "front_plate", "rider_body", "rider_head", "wheels"}


def open_directory_browser():
    root.directory = filedialog.askdirectory()
    if not root.directory == "":
        # Get files from directory
        files = get_files_in_directory(root.directory)
        if len(files[0]) > 0 or len(files[1]) > 0:
            mapFiles = files[0]
            jmFiles = files[1]
            # Populate skins listbox
            populate_listbox(skinsListbox, mapFiles)
            # Populate jms listbox
            populate_listbox(jmListbox, jmFiles)
            # Show the user the working dir
            currentWorkingDirectoryLabel["text"] = f"{root.directory}"


def get_files_in_directory(directory):
    mapFiles = []
    jmFiles = []
    for f in listdir(directory):
        filepath = join(directory + "/" + f)
        if isfile(filepath):
            filename, extension = splitext(f)
            if (extension == ".png"):
                mapFiles.append(f)
            elif (extension == ".jm"):
                jmFiles.append(f)
    return (mapFiles, jmFiles)


def populate_listbox(listbox, files):
    # Delete all items in list box
    clear_listbox(listbox)
    # Insert file names into listbox
    for f in files:
        listbox.insert(END, f)


def clear_listbox(listbox):
    listbox.delete(0, END)


def delete_item_skin_lb():
    if skinsListbox.get(0):
        selection = skinsListbox.curselection()
        selectionList = []
        for i in selection:
            selectionList.append(skinsListbox.get(i))
        for i in selection[::-1]:
            skinsListbox.delete(i)
        print(
            f"Removing {selectionList} from available skins and maps...")
    else:
        print("Skins listbox was empty...")


def delete_item_jm_lb():
    if jmListbox.get(0):
        selection = jmListbox.curselection()
        selectionList = []
        for i in selection:
            selectionList.append(jmListbox.get(i))
        for i in selection[::-1]:
            jmListbox.delete(i)
        print(f"Removing {selectionList} from available JMs...")
    else:
        print("JMs listbox was empty...")


def create_directory(directory, modelName):
    rootDir = directory + f"/RenamedFiles/{modelName}"
    jmDir = rootDir + "/JM"
    mapsDir = rootDir + "/Maps"

    rootDirExists = path.exists(rootDir)
    mapsDirExists = path.exists(mapsDir)
    jmDirExists = path.exists(jmDir)

    if rootDirExists and mapsDirExists and jmDirExists:
        print("Save path already exists. This is OK")
        return (rootDir, mapsDir, jmDir)
    else:
        if not rootDirExists:
            os.makedirs(rootDir)
        if not jmDirExists:
            os.mkdir(jmDir)
        if not mapsDirExists:
            os.mkdir(mapsDir)

        return (rootDir, mapsDir, jmDir)


def sort_maps():
    normalMap = None
    specMap = None
    diffuseMaps = []

    dynoSelection = dynoListbox.selection_get()
    dynoValue = None
    for item in dynosList:
        if dynoSelection == item:
            dynoValue = dynosList[dynoSelection]
    if dynoValue != None:
        maps = skinsListbox.get(0, END)
        for i in range(0, len(maps)):
            # Normal Map
            if "norm" in maps[i] or "Norm" in maps[i]:
                if messagebox.askyesno("Is this your normal map?", maps[i]):
                    normalMap = maps[i]
                    print(f"Normal map: {normalMap}")
                else:
                    diffuseMaps.append(maps[i])
            # Spec map
            elif "spec" in maps[i] or "Spec" in maps[i]:
                if messagebox.askyesno("Is this your specular map?", maps[i]):
                    specMap = maps[i]
                    print(f"Specular map: {specMap}")
            else:
                diffuseMaps.append(maps[i])
                print(f"Diffuse map: {maps[i]}")
        return (normalMap, specMap, diffuseMaps)
    else:
        print("The key supplied does not exist in the dynos dictionary...")
        return None


def rename_all_files():
    # Check to see if skins lb or jms lb has items in them
    skinsLbPopulated = skinsListbox.get(0)
    jmsLbPopulated = jmListbox.get(0)
    if not skinsLbPopulated and not jmsLbPopulated:
        print("You need to choose a directory that has skins or jms...")
        return
    # Check to see if the model name entry is blank
    if modelNameEntry.get().lower() == "":
        print("You need to supply a model name...")
        return
    # Check to see if a dyno is selected
    if not dynoListbox.curselection():
        print("You need to select a dyno...")
        return

    # Run the skin renaming
    rename_map_files()
    # Run the JM renaming
    rename_jm_files()


def rename_map_files():
    # Check to see if skins lb or jms lb has items in them
    skinsLbPopulated = skinsListbox.get(0)
    if not skinsLbPopulated:
        print("You need to choose a directory that has skins...")
        return
    # Check to see if the model name entry is blank
    if modelNameEntry.get().lower() == "":
        print("You need to supply a model name...")
        return
    # Check to see if a dyno is selected
    if not dynoListbox.curselection():
        print("You need to select a dyno...")
        return

    # Get the sorted maps
    sortedMaps = sort_maps()
    if sortedMaps == None:
        return

    normalMap = sortedMaps[0]
    specMap = sortedMaps[1]
    diffuseMaps = sortedMaps[2]

    # Create a place to store the maps
    newPaths = create_directory(root.directory, modelNameEntry.get().lower())

    # Create new maps and JMs
    copy_maps_to_directory(newPaths[1])

    # Rename normal map
    if normalMap != None:
        rename_map(f"{newPaths[1]}", normalMap, "norm")
    # Rename spec map
    if specMap != None:
        rename_map(f"{newPaths[1]}", specMap, "spec")
    # Rename diffuse maps
    if len(diffuseMaps) > 0:
        for item in diffuseMaps:
            rename_map(f"{newPaths[1]}", item, "none")


def rename_jm_files():
    # Check to see if jms lb has items in them
    jmsLbPopulated = jmListbox.get(0)
    if not jmsLbPopulated:
        print("You need to choose a directory that has jms...")
        return
    # Check to see if the model name entry is blank
    if modelNameEntry.get().lower() == "":
        print("You need to supply a model name...")
        return
    # Check to see if a dyno is selected
    if not dynoListbox.curselection():
        print("You need to select a dyno...")
        return

    # Get paths for new JMs
    newPaths = create_directory(root.directory, modelNameEntry.get().lower())
    # Copy jms to new directory
    copy_jms_to_directory(newPaths[2])
    # Rename all of the JMs
    for jm in jmListbox.get(0, END):
        rename_jm(newPaths[2], jm)


def copy_maps_to_directory(directory):
    for item in skinsListbox.get(0, END):
        copy = shutil.copyfile(
            f"{root.directory}/{item}", f"{directory}/{item}")


def copy_jms_to_directory(directory):
    for item in jmListbox.get(0, END):
        shutil.copyfile(f"{root.directory}/{item}", f"{directory}/{item}")

def copy_files_to_directory(currentDirectory, copyToDirectory):
    for f in listdir(currentDirectory):
        filepath = join(currentDirectory + "/" + f)
        if isfile(filepath):
            shutil.copyfile(f"{currentDirectory}/{f}", f"{copyToDirectory}/{f}")

def rename_map(directory, map, special):
    # Check to see if map halfway named
    filename = None
    if "-" in map:
        splitName = map.rsplit("-", 1)
        trim = messagebox.askyesno(
            f"Do you want to trim after the '-' in {map}?", f"Not used: {splitName[0]}-, Used: {splitName[1]}")
        if trim == True:
            filename = splitName[1]
        else:
            filename = map
    else:
        filename = map
    dynoSelection = dynoListbox.selection_get()
    dynoValue = None
    for item in dynosList:
        if dynoSelection == item:
            dynoValue = dynosList[dynoSelection]
    # TODO: Check map type to copy and rename
    output = None
    if special == "norm":
        output = f"{directory}/{dynoValue}-{modelNameEntry.get().lower()}_norm.png"
        try:
            os.rename(f"{directory}/{map}", output)
        except OSError as e:
            os.remove(output)
            os.rename(f"{directory}/{map}", output)
    elif special == "spec":
        output = f"{directory}/{dynoValue}-{modelNameEntry.get().lower()}_spec.png"
        try:
            os.rename(f"{directory}/{map}", output)
        except OSError as e:
            os.remove(output)
            os.rename(f"{directory}/{map}", output)
    else:
        output = f"{directory}/{dynoValue}-{modelNameEntry.get().lower()}-{filename}"
        try:
            os.rename(f"{directory}/{map}", output)
        except OSError as e:
            os.remove(output)
            os.rename(f"{directory}/{map}", output)

def rename_jm(directory, jm):
    # Get the selected dyno
    dynoSelection = dynoListbox.selection_get()
    dynoValue = None
    for item in dynosList:
        if dynoSelection == item:
            dynoValue = dynosList[dynoSelection]
    # Extract JM type
    jmType = None
    for type in jmParts:
        if type.lower() == "wheels":
            saveDir = f"{directory}"
            filename = None
            if "front_wheel" in jm.lower():
                filename = f"front_wheel-{modelNameEntry.get().lower()}.jm"
            elif "rear_wheel" in jm.lower():
                filename = f"rear_wheel-{modelNameEntry.get().lower()}.jm"
            else:
                continue
            # See if file exists - need to delete if so or error on windows, MacOS and Linux OK
            if os.path.exists(f"{saveDir}/{filename}"):
                os.remove(f"{saveDir}/{filename}")
            # Rename the jm file
            os.rename(f"{saveDir}/{jm}", f"{saveDir}/{filename}")
        else:
            # Cast to lowercase just in case the JM is saved weird
            if type.lower() in jm.lower():
                jmType = type
                saveDir = f"{directory}"
                filename = f"{dynoValue}_{jmType}-{modelNameEntry.get().lower()}.jm"
                # Change file name to only dyno and model name if rider or wheels
                if jmType.lower() == "rider_body" or jmType.lower() == "rider_head":
                    filename = f"{dynoValue}-{modelNameEntry.get().lower()}.jm"
                # See if file exists - need to delete if so or error on windows, MacOS and Linux OK
                if os.path.exists(f"{saveDir}/{filename}"):
                    os.remove(f"{saveDir}/{filename}")
                # Rename the jm file
                os.rename(f"{saveDir}/{jm}", f"{saveDir}/{filename}")


def run_saf_files():
    # Change into working directory just to be safe
    os.chdir(workingDirectory)
    # Check to see if the model name is empty
    if modelNameEntry.get().lower() == "":
        print("SAF Files: You need to supply a model name to saf your files...")
        return
    else:
        # Check to see if there is a root directory
        if root.directory == None:
            print("SAF Files: You need to supply a diredctory...")
            return
        else:
            # Make TEMP folder in plugins
            if not path.exists("plugins/TEMP"):
                os.makedirs("plugins/TEMP")
                print("SAF Files: Created temp export directory...")
            # Copy all necessary files to the temp folder
            renamedFilesDirectory = f"{root.directory}/RenamedFiles"
            subDirs = os.listdir(renamedFilesDirectory)
            modelDir = None
            # Get all the sub-directories and set modelDir if one matches the modelEntry
            for dir in subDirs:
                if dir.lower() == modelNameEntry.get().lower():
                    modelDir = f"{renamedFilesDirectory}/{dir}"

            if modelDir == None:
                print("[SAF Files]: Your model name does not match any existing directories...")
                return
            else:
                # Copy maps to export folder
                if not path.exists(f"{modelDir}/Maps"):
                    print(f"[SAF Files]: No map files were found...")
                else:
                    copy_files_to_directory(f"{modelDir}/Maps", "plugins/TEMP")  # Map files
                # Copy JMs to export folder
                if not path.exists(f"{modelDir}/JM"):
                    print(f"[SAF Files]: No JM files were found...")
                else:
                    copy_files_to_directory(f"{modelDir}/JM", "plugins/TEMP")  # JM files
                # Copy all file names to a string to run in saf.py
                args = []
                # Add args to args list
                args.append('python')
                args.append('saf.py')
                files = os.listdir(f"plugins/TEMP")
                for f in files:
                    if not f == f"{modelNameEntry.get().lower()}.saf" and not f == "saf.py":
                        args.append(f"{f}")  # \s was not working so make sure the space stays
                # Add saf name to args list
                args.append(f"{modelNameEntry.get().lower()}.saf")

                fullCommand = ""
                for f in args:
                    fullCommand += f"{f} "
                print(fullCommand)

                # Copy the saf script to the Export folder
                if not path.exists("plugins/TEMP/saf.py"):
                    shutil.copyfile(f"plugins/saf.py", f"plugins/TEMP/saf.py")

                # Change into the plugins/TEMP directory
                os.chdir("plugins/TEMP")
                #TODO:  SAF the files
                safName = f"{modelNameEntry.get().lower()}.saf"
                safCreationCommand = subprocess.Popen(args, shell=True)
                # Move the saf file back to the renamed files directory
                safFilePath = f"{root.directory}/RenamedFiles/{modelNameEntry.get().lower()}/Saf"
                if not path.exists(safFilePath):
                    os.makedirs(safFilePath)
                shutil.copyfile(f"{safName}", f"{safFilePath}/{safName}")
                # Change back into the working directory
                os.chdir(workingDirectory)
                # Clean up the temp directory
                #clean_temp_folders()


def clean_temp_folders():
    try:
        if path.exists("plugins/TEMP"):
            shutil.rmtree("plugins/TEMP")
    except OSError as e:
        print("[Clean TEMP Directory]: Could not remove TEMP directory...")

def on_window_close():
    # Clean up the TEMP folders
    clean_temp_folders()
    # Destory the root window
    root.destroy();

# Run the TK setup and loop
if __name__ == "__main__": # TODO: put the initialization code into a function
    # General elements
    workingDirectoryLabel = Label(
        root, text="Working Directory", font="TkDefaultFont 16 bold")
    currentWorkingDirectoryLabel = Label(
        root, text=" no working directory", font="TkDefaultFont 8 bold")
    openDirectoryButton = Button(
        root, text="Browse", command=open_directory_browser)
    modelNameLabel = Label(root, text="Model Name", font="TkDefaultFont 16 bold")
    modelNameEntry = Entry(root)
    renameLabel = Label(root, text="Rename", font="TkDefaultFont 16 bold")
    renameAllButton = Button(root, text="Rename All", command=rename_all_files)
    renameMapsButton = Button(root, text="Rename Maps", command=rename_map_files)
    renameJMsButton = Button(root, text="Rename JMs", command=rename_jm_files)
    safLabel = Label(root, text="SAF", font="TKDefaultFont 16 bold")
    scramLabel = Label(root, text="SCRAM", font="TKDefaultFont 16 bold")
    safButton = Button(root, text="SAF Files", command=run_saf_files)

    # Skins category elements
    skinsCategoryLabel = Label(
        root, text="Skins and Maps", font="TkDefaultFont 16 bold")
    skinsLbScrollbar = Scrollbar(root)
    skinsListbox = Listbox(root, selectmode=EXTENDED,
                        yscrollcommand=skinsLbScrollbar.set)
    skinsDeleteButton = Button(root, text="-", command=delete_item_skin_lb)
    # JM category elements
    jmCategoryLabel = Label(
        root, text="JMs", font="TkDefaultFont 16 bold")
    jmLbScrollbar = Scrollbar(root)
    jmListbox = Listbox(root, selectmode=EXTENDED,
                        yscrollcommand=jmLbScrollbar.set)
    jmsDeleteButton = Button(root, text="-", command=delete_item_jm_lb)
    # Dyno rename category
    dynoCategoryLabel = Label(
        root, text="Dyno", font="TkDefaultFont 16 bold")
    dynoLbScrollbar = Scrollbar(root)
    dynoListbox = Listbox(root, yscrollcommand=dynoLbScrollbar.set)

    # Place elements into the root
    workingDirectoryLabel.place(x=20, y=10, width=250, height=30)
    currentWorkingDirectoryLabel.place(x=62.5, y=40, width=160, height=30)
    openDirectoryButton.place(x=62.5, y=70, width=160, height=30)
    modelNameLabel.place(x=20, y=160, width=250, height=30)
    modelNameEntry.place(x=62.5, y=200, width=160, height=30)
    renameLabel.place(x=20, y=290, width=250, height=30)
    renameAllButton.place(x=62.5, y=330, width=160, height=30)
    renameMapsButton.place(x=62.5, y=370, width=160, height=30)
    renameJMsButton.place(x=62.5, y=410, width=160, height=30)
    safLabel.place(x=62.5, y=470, width=160, height=30)
    safButton.place(x=62.5, y=510, width=160, height=30)

    skinsCategoryLabel.place(x=320, y=10, width=250, height=30)
    skinsLbScrollbar.place(x=570, y=40, width=15, height=100)
    skinsListbox.place(x=320, y=40, width=250, height=100)
    skinsDeleteButton.place(x=550, y=140, width=20, height=20)

    jmCategoryLabel.place(x=320, y=160, width=250, height=30)
    jmLbScrollbar.place(x=570, y=200, width=15, height=100)
    jmListbox.place(x=320, y=200, width=250, height=100)
    jmsDeleteButton.place(x=550, y=300, width=20, height=20)

    dynoCategoryLabel.place(x=320, y=320, width=250, height=30)
    dynoLbScrollbar.place(x=570, y=350, width=15, height=100)
    dynoListbox.place(x=320, y=350, width=250, height=100)

    scramLabel.place(x=320, y=470, width=250, height=30)

    # Configure scrollbars
    skinsLbScrollbar.config(command=skinsListbox.yview)
    jmLbScrollbar.config(command=jmListbox.yview)
    dynoLbScrollbar.config(command=dynoListbox.yview)
    # Populate dynos list box
    populate_listbox(dynoListbox, dynosList.keys())

    # Get the working directory
    workingDirectory = os.getcwd()

    # Window close protocol to clean up TEMP folder
    root.protocol("WM_DELETE_WINDOW", on_window_close)
    # Run the main loop
    root.mainloop()