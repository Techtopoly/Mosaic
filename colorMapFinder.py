#!/usr/bin/env python

from PIL import Image
import numpy as np
import os
import math
from generatePhp import generatePhp

def colorMapFinder(filename, mosaic_row, mosaic_col, *args):
    # Load a file and create a color map with pixel dimensions by specified row and column
    if len(args) == 0:
        webPath = os.getcwd()
    else:
        webPath = args[0]
    im = Image.open(filename)
    fileparts = os.path.splitext(filename)
    pix = im.load()
    # Get the step size, width, and height of the image for iterating
    col,row = im.size
    step_row = row/mosaic_row
    step_col = col/mosaic_col
    # Setup empty matrix
    all_tiles = np.empty(dtype=list, shape=(mosaic_row,mosaic_col))
    # Build array all_tiles of colors
    for row in range(mosaic_row):
        for col in range(mosaic_col):
            # Get the RGBA Value of the a pixel of an image
            red_pix, green_pix, blue_pix = pix[col*step_col+1,row*step_row+1]
            all_tiles[row,col] = [red_pix, green_pix, blue_pix]
    # Reduce color options by matching similar colors
    all_tiles, colorList = flattenColors(all_tiles)
    # 
    php = generatePhp()
    # Save matrix as PHP
    php.saveAsPhp(os.path.join(webPath, fileparts[0] + ".php"), all_tiles)
    # Save colorList as TXT
    saveAsTxt(os.path.join(webPath, fileparts[0] +  "_colorList.txt"), colorList)
    return

def findMatch(color, colorList, colorDifference, loc):
    newColor = "_".join(map(str,color))
    NUMBER_OF_COLORS = 3
    if colorList:
        foundMatch = False
        # Compare to each color
        for rgb in colorList:
            # Round if all colors are less than threshold
            colorRgb = map(int,rgb.split("_"))
            if sum(colorDifference(zip(color,colorRgb))) == NUMBER_OF_COLORS:
                # Found a matching color
                colorList[rgb].append(loc)
                # Replace existing color with matched color
                color = colorRgb
                # Found a match so set it to true
                foundMatch = True
                # No need to continue after match found, exit loop
                break
        # Add new color to colorList if no match found
        if not foundMatch:
            colorList[newColor] = [loc]
    else:
        # Initialize colorList
        colorList[newColor] = [loc]
    return color, colorList
    
        
def flattenColors(data):
    # flattenColors - Look at nearby colors and match the color if they are below the threshold
    THRESHOLD = 10
    colorList = {}
    # Check through all rows and cols of data and compare against the threshold
    colorDifference = lambda x: [1 for c,last in x if math.fabs(c-last) <= THRESHOLD]
    for r,row in enumerate(data):
        lastValue = []
        for c, color in enumerate(row):
            # Create color list of all colors
            currentColor = "_".join(map(str,color))
            # Round if all colors are less than threshold
            data[r,c], colorList = findMatch(color,colorList,colorDifference,(r,c))
    return data, colorList

def saveAsTxt(txtfile, data):
    f = open(txtfile, "w")
    for color,loc_list in data.iteritems():
        loc = ",".join(map(str,loc_list))
        f.write("%s %s\n" % (color, loc))
    f.close()
    return

# --------------------------------------------------------------------

def main():
    # Pixelation count by row and column
    # rows = 77
    # cols = 33
    # filename = 'valsparpaint.png'
    output_path = 'C:\Apache2\htdocs'
    rows = 25
    cols = 112
    filename = 'IMG_6664pt3.jpg'
    # filename = 'testimage.jpg'
    colorMapFinder(filename, rows, cols, output_path)


# Command line direct call
if __name__ == "__main__":
    main()
