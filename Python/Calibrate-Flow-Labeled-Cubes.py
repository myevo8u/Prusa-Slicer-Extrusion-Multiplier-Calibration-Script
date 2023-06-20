#################################################################
# Prusa Extrusion Multiplier Calibration Post Processing Script
# V1.0
# Created by: Kevin Pidliskey
# https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/
#################################################################

import tkinter as tk
from tkinter import filedialog
import os
import re

print("Prusa Extrusion Multiplier Calibration Post Processing Script V1.0")
input("Press Enter to select a Prusa Slicer GCode Generated File to modify:")

# Create the root window
root = tk.Tk()
root.withdraw()

# Display the file dialog for selecting a .gcode file
file_path = filedialog.askopenfilename(filetypes=[("G-Code Files", "*.gcode")])
file_name = os.path.basename(file_path)

# Check if a file was selected
if file_path:
    # File path is not empty, do something with the selected file
    with open(file_path, 'r') as file:
        # Perform operations on the file
        file_content = file.read()
        # Process the file content as needed
        print(f"G-Code File Loaded: {file_name}\n\n\n\n")
else:
    # No file was selected
    print("No file selected.")

unique_lines = set()  # Set to store unique lines

#Find unique objects
for line in file_content.split("\n"):
    if line.startswith("; printing object") and line not in unique_lines:
        unique_lines.add(line)

num_models = len(unique_lines)  # Get the unique count of lines
print(f"Found {num_models} unique models in G-Code\n\n")

base_extrusion_Multiplier = 0.0
for l in unique_lines:
    extracted_Multiplier = float(re.search("; printing object EM_Cube-(.*).stl", l).group(1))
    if extracted_Multiplier > base_extrusion_Multiplier:
        base_extrusion_Multiplier = extracted_Multiplier
print(f"Highest extrusion multiplier found in gcode is: {base_extrusion_Multiplier}")

replacementsmade = []
modified_content = file_content
for l in unique_lines:
    obj_name = re.search("; printing object (.*) id", l).group(1)
    print(f"\nModifying Object: {obj_name}")
    # Get the new Extrusion Multiplier for model
    extrusion_Multiplier = float(re.search("; printing object EM_Cube-(.*).stl", l).group(1))
    percentage_remaining = (extrusion_Multiplier / base_extrusion_Multiplier) * 100
    rounded_percentage = round(percentage_remaining, 2)

    # Perform operations specific to each model
    for j, line in enumerate(modified_content.split("\n")):
        if line == l:
            replacecount = modified_content.count(line)
            modified_line = line + f"\nM221 S{rounded_percentage} ; Set Extrusion Multiplier to {extrusion_Multiplier} : Modified by PPScript"  # Modify the line
            modified_content = modified_content.replace(line, modified_line)  # Replace the line in modified_content
            replacementsmade.append(f'Object {obj_name} modified: {replacecount} times | Flow set to: {rounded_percentage}% | Extrusion Multiplier set to: {extrusion_Multiplier}')
            break
    print(f"G-Code Extrusion Multiplier Modifications for Object {obj_name}: M221 S{rounded_percentage}\n")
# Save the modified content back to the file
with open(file_path, 'w') as file:
    file.write(modified_content)
print(f"********************Modifications Complete*******************************\n")
for i in replacementsmade:
    print(i)

exit = input("\nPress Enter to Exit: ")