##
#OxideCAM.py
#Author: Andrew Feldman, 1/18/15
#
#Translates a CAD design for a chemical surface coating into a series of CNC commands

import OutputStream

#Units in mm
pixel_width=1.0
pixel_height=1.0
pen_width=2.0

OutputStream.writeLine("G90")


