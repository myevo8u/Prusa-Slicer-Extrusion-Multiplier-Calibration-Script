
# Prusa Slicer Extrusion Multiplier Calibration Script

This postprocessing script allows you to calibrate your extrusion multiplier using multiple objects in a single print that was generated with Prusa Slicer. 

After reading through Ellis 3dp tuning guide on calibrating your extrusion multiplier in Prusa Slicer, I became annoyed after consecutively having to print multiple times just to fine the right flow for my printer. Ellis guide on calibrating your extrusion multiplier can be found here: https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html

Eventually I was sitting here doing manual modifications to the Gcode to find each object start position and adding a M221 S90 or whatever flow I needed. This also was annoying, so I decided to write a post processing script to automatically calculate the flow percentages based on the defined extrusion multiplier for your current filament profile selected.

This script works for Marlin Firmware, but can be edited easily to work on klipper by modifying line 75 in the script with approriate gcode. (I think klipper can use M221? DOUBLE CHECK!)

# Latest Release:

[Download Here](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/releases/tag/v1.0)

# Explanation:

Your base Multiplier is set to 1 under filament settings, if you wanted to print 3 objects, one being at an extrusion multiplier of 1, the other .98, and the third .97. This script will add the associated M221 S100, S98, S97 to your gcode for each instance of an object. 

Now, say your base extrusion set in the profile was different, like .935 This script will also account for this and calculate the correct flow compensation. If you wanted to print 3 objects, one being at an extrusion multiplier of .94, the other .93, and the third .92. This script will then calculate the associated M221 S100.53, S99.47, S98.4 to your gcode. So as you can see it is adopts to whatever your base extrusion multiplier is set to. 

# Pre-requirements

* This script. (You can use the .exe or python script) [Download Here](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/releases/tag/v1.0)
* This script works for Marlin Firmware, but can be edited easily to work on klipper by modifying line 75 in the script with approriate gcode. (I think klipper can use M221? DOUBLE CHECK!)
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/instances.png?raw=true)

# Usage

Alright, now that you have some things setup. Lets walk through the steps:

1. As recommended in Ellis guide, I use 30x30x3 blocks to calibrate my extrusion multiplier. You can download mine [Here](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/tree/main/Models): 
2. Import your block into Prusa Slicer, then as mentioned previously. Duplicate it as many times as you need to by **_Adding New Instances_**. Do not use separate objects!!! You should have multiple instances starting with one.
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/instances.png?raw=true)
 Make sure your blocks are aligned and sorted correctly, Instance 1, 2, 3, 4, So you can easily remember what flows you defined when looking over them. 
3. Note your **_Extrusion Multiplier_** value defined under **_Filament Settings_** (I recommend just setting this to 1, but as mentioned above the script can calculate the correct flow percentage even if use a different base value)
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/extrusionmultiplier.png?raw=true)
4. Now go ahead and slice and save your Gcode to a folder.
5. Now lets start up our script, you have two options, one being use the compiled .exe or using python and downloading the raw script. The choice is yours, you can run the script with python using **_python Calibrate-Flow.py_**. Otherwise just double click on the .exe
6. The script will tell you to hit enter to open a file dialog and select your gcode you just created:
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/loadgcode.png?raw=true)
6. Now we need to tell the script our base extrusion multiplier that is currently set in prusa slicer from step 3, in my case it is 1. We can also see the script found our 4 instances.
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/setbaseem.png?raw=true)
7. Now we need to define what we would like our extrusion multiplier to be for each instance. The scale can be any percentage in decimal format. (e.g., 100% would be 1, 102% would be 1.02, 98.5% would be .985, etc.)
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/setmodifiers.png?raw=true)
8. AND WE ARE DONE! The script will give you an output of the settings and save over the existing file:
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/complete.png?raw=true)

Just to show what the output would look like if we didn't use 1 as the base extrusion multiplier (We can see the percentages are way different from if we used a value of 1 as the base):
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/altem.png?raw=true)

9. Final step is to check your GCODE! You can do a find for **_Modified by PPScript_** in a text editor to verify M221 has been added properly:
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/gcodecheck.png?raw=true)

10. That's it, you are ready to print. Hope you find this script useful!

# Usage (PrusaSlicer Embedded with Labeled Cubes)

Alternately, this script can be executed via a PrusaSlicer-embedded workflow when combined with [AndrewEllis93's Labelled Cubes](https://github.com/AndrewEllis93/Print-Tuning-Guide/tree/main/test_prints/extrusion_multiplier_cubes/labeled).

Please note these instructions make the following assumptions:

    * You are using a 0.4mm nozzle
    * You have Python installed on your machine
    * Python is in your PATH (i.e. you can run `python` in your terminal and it opens)

1. Go to [https://github.com/AndrewEllis93/Print-Tuning-Guide/tree/5ebf40e8c67c88b959420d83502aa34fcf81567b](https://github.com/AndrewEllis93/Print-Tuning-Guide/tree/5ebf40e8c67c88b959420d83502aa34fcf81567b), click on the green `Code` button, then choose `Download ZIP`
1. Extract the ZIP, and pull out the folder `test_prints/extrusion_multiplier_cubes/labeled`
    * The rest of the extracted ZIP can be discarded
1. Download needed scripts from this repository and save them wherever you like
    * All platforms: [Calibrate-Flow-Embedded.py](https://raw.githubusercontent.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/main/Python/Calibrate-Flow-Embedded.py)
    * Windows: [Calibrate-Flow-Embedded-Wrapper.bat](https://raw.githubusercontent.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/main/Python/Calibrate-Flow-Embedded-Wrapper.bat)
    * macOS/Linux: [Calibrate-Flow-Embedded-Wrapper.sh](https://raw.githubusercontent.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/main/Python/Calibrate-Flow-Embedded-Wrapper.bat)
1. Record the full path to the wrapper script for your platform for later use
1. Open PrusaSlicer, go to `Print Settings`, and choose whichever the normal 0.20mm profile for your printer is
1. Change the following settings for the profile to match the print settings recommended by the Ellis3DP tuning guide and integrate this script:
    * Layers and perimeters
        * `Solid layers: Top`: 10
        * `Solid layers: Bottom`: 2
    * Infill
        * `Fill density`: 30%
        * `Top fill pattern`: Monotonic Lines
    * Output options
        * `Label objects`: OctoPrint comments
        * `Post-processing scripts`: The full path to the wrapper script you recorded earlier
    * Advanced
        * `Top solid infill`: 0.4mm
1. Save the print profile as something like `Calibration - Extrusion Multiplier`
1. Create a new project using the cubes you downloaded, choosing whichever extrusion multiplier values you wish to test
1. Note the highest EM value you selected, and set `Filament settings` > `Filament` > `Extrusion multiplier` to match
    * It is CRITICALLY important not to miss this step, or your calibration test will yield an incorrect value
1. Slice and export the file
    * Upon export, the processing script will run and adjust the values for each object
1. Check the generated GCODE to ensure it has been modified properly. You can do a find for **_Modified by PPScript_** in a text editor to verify M221 has been added properly:
![alt text](https://github.com/myevo8u/Prusa-Slicer-Extrusion-Multiplier-Calibration-Script/blob/main/Screenshots/gcodecheck.png?raw=true)