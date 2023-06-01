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

#Find unique instances
for line in file_content.split("\n"):
    if line.startswith("; printing object") and re.search(r"copy \d+$", line) and line not in unique_lines:
        unique_lines.add(line)

num_models = len(unique_lines)  # Get the unique count of lines
print(f"Found {num_models} unique models in G-Code\n\n")

while True:
    print(f"********Set Base Extrusion Multiplier**********\nThis is your starting/base Extrusion Multiplier that is defined in your filament settings profile. \nTypically keep this set to 1 when calibrating your extrusion multiplier. \nThe script will also calculate the flow percentage if you use a smaller default value such as .90\n")
    base_extrusion_Multiplier = input("Enter starting/base Extrusion Multiplier (e.g., 1): ")
    try:
        base_extrusion_Multiplier = float(base_extrusion_Multiplier)
        break
    except ValueError:
        print("\nInvalid input. Please enter a decimal value to two places.")

replacementsmade = []
modified_content = file_content
for i in range(num_models):
    print("\nModifying Instance:", i + 1)
    # Get the new Extrusion Multiplier for model
    while True:
        extrusion_Multiplier = input(f"Enter an extrusion Multiplier for Instance {i + 1}, (e.g., .95 or .925): ")
        try:
            extrusion_Multiplier = float(extrusion_Multiplier)
            break
        except ValueError:
            print(f"Invalid input. Please enter a decimal value to two places.\n")
    #calculate percent difference from base Extrusion Multiplier
    percentage_remaining = (extrusion_Multiplier / base_extrusion_Multiplier) * 100
    rounded_percentage = round(percentage_remaining, 2)

    # Perform operations specific to each model
    for j, line in enumerate(modified_content.split("\n")):
        if line.startswith("; printing object") and f"copy {i}" in line:
            replacecount = modified_content.count(line)
            modified_line = line + f"\nM221 S{rounded_percentage} ; Set Extrusion Multiplier to {extrusion_Multiplier} : Modified by PPScript"  # Modify the line
            modified_content = modified_content.replace(line, modified_line)  # Replace the line in modified_content
            replacementsmade.append(f'Instance {i + 1} modified: {replacecount} times | Flow set to: {rounded_percentage}% | Extrusion Multiplier set to: {extrusion_Multiplier}')
            break
    print(f"G-Code Extrusion Multiplier Modifications for Instance {i + 1}: M221 S{rounded_percentage}\n")
# Save the modified content back to the file
with open(file_path, 'w') as file:
    file.write(modified_content)
print(f"********************Modifications Complete*******************************\n")
for i in replacementsmade:
    print(i)

exit = input("\nPress Enter to Exit: ")