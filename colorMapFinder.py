#!/usr/bin/env python

from PIL import Image
import numpy

def colorMapFinder(filename, mosaic_row, mosaic_col):
  im = Image.open(filename)
	x = 1
	y = 1
	pix = im.load()
	# Get the width and hight of the image for iterating over
	row,col = im.size
	step_row = mosaic_row/row
	step_col = mosaic_col/col
	# Get the RGBA Value of the a pixel of an image
	all_tiles = numpy.zeros(shape=(mosaic_row,mosaic_col))
	for r in range(mosaic_row):
		for c in range(mosaic_col):
			print [pix[r*step_row+1,c*step_col+1]]
			
			all_tiles[r,c] = [pix[r *step_row+1,c*step_col+1]]
	print all_tiles[x,y] 
	# pix[x,y] = value # Set the RGBA Value of the image (tuple)

rows = 25
cols = 112
filename = 'IMG_6664pt3.jpg'
colorMapFinder(filename, rows, cols)
