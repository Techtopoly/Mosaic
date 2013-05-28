#!/usr/bin/env python

from PIL import Image
import numpy
import os
import math

def colorMapFinder(filename, mosaic_row, mosaic_col):
	webPath = 'C:\Apache2\htdocs'
	im = Image.open(filename)
	fileparts = os.path.splitext(filename)
	pix = im.load()
	# Get the step size, width, and height of the image for iterating
	col,row = im.size
	step_row = row/mosaic_row
	step_col = col/mosaic_col
	# Setup empty matrix
	all_tiles = numpy.empty(dtype=list, shape=(mosaic_row,mosaic_col))
	# Build array all_tiles of colors
	for row in range(mosaic_row):
		for col in range(mosaic_col):
			# Get the RGBA Value of the a pixel of an image
			red_pix, green_pix, blue_pix = pix[col*step_col+1,row*step_row+1]
			all_tiles[row,col] = [red_pix, green_pix, blue_pix]
	# Reduce color options by matching similar colors
	all_tiles, colorList = flattenColors(all_tiles)
	# Save matrix as PHP
	saveAsPHP(os.path.join(webPath, fileparts[0] + ".php"), all_tiles)
	# Save colorList as PHP
	saveAsPHP(os.path.join(webPath, "colorList.php"), colorList)
	return

def flattenColors(data):
	THRESHOLD = 8
	NUMBER_OF_COLORS = 3
	colorList = []
	row, col = data.shape
	# Check through all rows and cols of data
	for r in range(row):
		for c in range(col):
			color = data[r,c]
			# Look in colorList for a matching color
			if colorList:
				foundInColorList = False
				for rgb in colorList:
					rgbMatch = 0
					# Check each RGB color of the row col position
					for count, ckey in enumerate(color):
						# Match only colors that are less than the THRESHOLD
						if math.fabs(ckey - rgb[count]) <= THRESHOLD:
							rgbMatch += 1
					# Found matching color
					if rgbMatch == NUMBER_OF_COLORS:
						# Set color and stop search
						data[r,c] = rgb
						foundInColorList = True
						break
				# Add to colorlist if not found
				if foundInColorList == False:
					colorList.append(color)
			# Empty colorList found so add first element
			else:
				colorList.append(color)	
				
	return data, colorList

def saveAsPHP(phpfile, data):
	# Open output file and write headers.
	outfile = createphpfile(phpfile)

	# Write PHP header
	outfile = createphpheader(outfile)
	if type(data) is numpy.ndarray:
		row, col = data.shape
	else:
		row = len(data)
		col = 1
	
	outfile.write('<table class="colormap" align="center" width=85%% border=1>\n')
	# Body
	for r in range(row):
			outfile.write('<tr>\n')
			outfile.write('  <td>\n')
			outfile.write('      <div class="row">%i</div>' % r)
			outfile.write('  </td>\n')
			for c in range(col):
				outfile.write('  <td>\n')
				if type(data) is numpy.ndarray:
					red, green, blue = data[r,c]
				else:
					red, green, blue = data[r]
				outfile.write('      <div class="red">%i</div><div class="green">%i</div><div class="blue">%i</div>\n' % (red, green, blue))
				outfile.write('  </td>\n')
			outfile.write('</tr>\n')
	# End the month
	outfile.write('</table>\n\n')
	
	# Footer
	closephpfile(outfile)
	
def createphpheader(outfile):
	# createphpheader: Prep php file with php header
	phpstr = """
	<?php
		date_default_timezone_set('America/Los_Angeles');
	?>"""

	outfile.write('%s\n' % phpstr)
	outfile.write('<br />\n')
	return outfile
	
# --------------------------------------------------------------------
def createphpfile(phpfile):
	# Create an php output file with a stylesheet header. Returns file id
	# used by fprintf.
	outfile = open(phpfile,'w')
	outfile.write('<html>\n')
	headstr = """<link rel="stylesheet" href="colormap.css" title="colormap-css" media="all" type="text/css">"""
		
	outfile.write('%s\n' % headstr)
	outfile.write('<br />\n<body>\n')
	return outfile

def closephpfile(outfile):
	outfile.write('</body>\n</html>\n')
	outfile.close()
	
rows = 25
cols = 112
filename = 'IMG_6664pt3.jpg'
# filename = 'testimage.jpg'
colorMapFinder(filename, rows, cols)
