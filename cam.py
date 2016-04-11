##
#cam.py
#Author: Andrew Feldman, 4/10/16
#Description: OxideCAM tool main file.
#
#Syntax: python cam.py plate_width_mm plate_height_mm plate_position_mm_x plate_position_mm_y plate_position_mm_z output_filename
#-plate_width_mm: 
#
#
#
#Dependencies:
#
#Expects config.txt in local directory.
#
#TODO: input args
#TODO: config file
#TODO: create/write to file
#TODO: pixel magnitude rescale
#TODO: map to control value
#TODO: file top comments
##

from bmp_to_pixel_magnitude_list import bmp_to_pixel_magnitude_list

(bmp_pixel_width,bmp_pixel_height,number_of_pixels,pixel_magnitude_list)=bmp_to_pixel_magnitude_list("surfviewer.bmp")


