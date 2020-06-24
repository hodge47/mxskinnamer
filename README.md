# mxskinnamer
This is a python script that appropriately names provided skin textures or JM files for the desired bike dynos. Naming skins for MX Simulator is confusing and tedious so this script was made to make the process easier. This script works with multiple diffuse maps at once and with or without a normal and/or specular map.

## How to Use

**You will need Python installed on your machine to use this*
### Prep
You will need *at least* one diffuse map (You can use as many diffuse maps as you want). This is the map that your graphics are on. This map can be named whatever you want it to be but it cannot have 'N[n]orm' or 'S[s]pec' in it. Optionally you can also use normal and specular maps. These need to have 'N[n]orm' and 'S[s]pec' in the name, respectively.

You can also choose to rename JM files. For a bike these should include "fork_lower.jm", "fork_upper.jm", "frame.jm", and "swingarm.jm". For a rider this would need "rider_body.jm", for a helmet, "rider_head.jm". Lastly, for wheels the JMs you would need are "front_wheel.jm" and "rear_wheel.jm".

You can either rename skins and JMs separately on their own or all together at once.

### Install Python
1. Go to (https://www.python.org/downloads/) and download the latest release of Python
2. Follow the installer instructions for your operating system

### Running the Script

#### Double-Click
1. Extract the script somewhere on your computer
2. Double-click the script
#### Terminal/Command Line
1. Extract the script somewhere to your computer
2. Open a terminal or command line
3. `cd` in the directory that contains the script
4. Run this command `python main.py`

### Usage
1. Click the browse button and navigate to the directory that contains your skins (diffuse textures, normal map, and specular map) or JM files
2. Type the model name you're saving for in the 'Model Name' text box. This is what your JM name is after the dyno
3. Select the dyno that you're saving for in the 'Dyno' list. This contains bikes, rider body, helmet, and wheels
4. Rename buttons
   - Click the 'Rename All' button to rename skins and JM files
   - Click the 'Rename Maps' button to only rename skins and maps
   - Click the 'Rename JMs' button to only rename JM files
5. Navigate to the directory where your skins were saved
   - __*Note: Skins/maps and JM files are now copied and then renamed to avoid a destructive workflow. Your files will be saved in your skins/jm directory under 'RenamedFiles/Model Name/Maps' or 'RenamedFiles/Model Name/JM'*__
6. (Optional) Scram and saf your bike maps
7. Move to your game install directory or personal folder
