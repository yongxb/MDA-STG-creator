# MDA STG creator
**Disclaimer:** This is not an official addon to Metamorph, please purchase the scan slide module if official support is needed. Use this at your own risk. The author of this will not be liable for anything that results from the use of this app. Please see the warnings section below for things to look out for when using this.

## Why STG creator?
Metamorph's Multi Dimensional Acquistion is commonly used to allow for the acquistion of multistage, multi-timepoint z-stack images. This opens the possibility of taking multiple overlapping images in a grid and stitching them later. However, it can be tedious to manually add points especially if there are many positions. Thus, STG creator is a GUI to help facilitate the creation of such a grid layout and provides a .STG file which can then be loaded back into Metamorph.

TLDR: Create a grid of image positions in MDA for stitching 

![gui](docs/stg_creator.png?raw=true "STG creator")

## What does it do?
1. Generate multiple grid position by defining the corners 
2. Define overlap based on fixed offset in µm, or as a percentage of the image
3. Define way the grid is scanned (snake along row, row by row)

## How to use it?
1. Type in series name in the input box labelled series name
2. Select type of overlap (defined offset or percentage overlap)
3. Select scan movement (snake along row or percentage overlap)
4. Specify number of rows and columns in the grid
5. Define overlaps 
    1. If defined offset is selected:
        1. Specify the x and y offsets in µm.
        2. \[Hexagonal layout\] Row offset can be used to specify if every alternate row starts from a different starting position.
        3. \[Hexagonal layout\] Row count offset determine if every alternate row has one more \(1\) or one less position \(-1\).
    2. If percentage overlap is selected:
       1. Specify the overlap as a percentage. 
       2. Select the magnification of the lens.
       3. Specify the camera that is being used. Select custom under the camera dropdown if your camera is not listed and specify height and width of the camera image in pixels, and the pixel size in µm.
6. Key in initial positions (Pick either method) 
    1. Manually key in positions
        1. Clear all positions from the stage tab in MDA. 
        2. Go to the top left corner of the grid and adjust the z position until the image is in focus. Add the position to MDA.
        3. Go to the top right corner of the grid and adjust the focus. Add the position to MDA.
        4. Go to the bottom left corner of the grid and adjust the focus. Add the position to MDA.
        5. Save the stage position from MDA and place the file in an accesible location 
        6. Load the stg file by clicking "Load position from file"
        7. Set auto focus offset to zero if it is not used or unsure
        8. Set z2 position offest to zero if a second z motor is not in use
        9. Double check that everything is in order
    2. Manually key in positions
        1. Follow the same steps as in 6i and key in the values manually into the respective fields. 
7. Click "Generate STG file" and save the file in an accesible location
8. Load the file back into MDA and proceed with setting up the rest of MDA

## Warnings!
Always double-check the input that is keyed in, and the output stg file for errors. It is a good idea to test this on a simple 2x2 grid to get a feel of it and ensure that it is working.

Note that this does not check for the limits of the machine such as the z-position and thus has the possibility of crashing the lens into the stage. Please use with caution as this has the potential to damage the microscope if incorrectly used.

## Required python packages
1. PyQt5
2. numpy