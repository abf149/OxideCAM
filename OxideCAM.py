##
#OxideCAM.py
#Author: Andrew Feldman, 1/18/15
#
#Translates a CAD design for a chemical surface coating into a series of CNC commands

import OutputStream

#Image processing
from scipy import misc
import os
cad_values= misc.imread(os.path.join('./','a.bmp'), flatten= 0)
cad_pixel_width=len(cad_values)
cad_pixel_height=len(cad_values[0])

#Units in mm
retract_distance=10.0
pixel_width=4.0
pixel_height=4.0
pen_diameter=2.0
eff_pixel_width=max(0,int(pixel_width-pen_diameter))
eff_pixel_height=max(0,int(pixel_height-pen_diameter))
dx=min(pen_diameter,pixel_width)
image_width=cad_pixel_width*pixel_width
image_height=cad_pixel_height*pixel_height
columns_per_pixel=int(round(eff_pixel_width/pen_diameter))
eff_pen_diameter=eff_pixel_width/columns_per_pixel

#Fill in an individual pixel; if it is smaller than the pen tip, simply plot a point
def drawPixel():
	for i in range(int(columns_per_pixel)):
		OutputStream.writeLine('G0 Y-' + str(eff_pixel_height))
		OutputStream.writeLine('G0 X' + str(eff_pen_diameter) + ' Y' + str(eff_pixel_height))

#Retract the scribe, home the scribe to the beginning of the next row, and contact the scribe.
#Zero the scribe voltage to be safe.
def homeRow():
	OutputStream.writeLine('G42 V0')
	OutputStream.writeLine('G0 Z' + str(retract_distance))
	OutputStream.writeLine('G0 X-' + str(image_width-pen_diameter) + ' Y-' + str(pixel_height))
	OutputStream.writeLine('G0 Z-' + str(retract_distance))

#Disable scribe and set anodizing voltage to zero.
OutputStream.writeLine('G41 F0')
OutputStream.writeLine('G42 V0')

#Home
OutputStream.writeLine('G28')

#Relative coordinates
OutputStream.writeLine('G91')

#Retract and move to (0,0) pixel, then contact the scribe and enable the anodizing voltage.
OutputStream.writeLine('G0 Z' + str(retract_distance))
OutputStream.writeLine('G0 X' + str(pen_diameter/2.0) + ' Y' + str(pen_diameter/2.0))
OutputStream.writeLine('G0 Z-' + str(retract_distance))
OutputStream.writeLine('G41 F1')

#Draw each row of the image, sequentially.
for y in range(cad_pixel_height):
	for x in range(cad_pixel_width):
		OutputStream.writeLine('G42 V' + str(cad_values[x][y]))
		drawPixel()
		OutputStream.writeLine('G0 X' + str(dx))

	OutputStream.writeLine('G41 F0')
	homeRow()
	OutputStream.writeLine('G41 F1')

