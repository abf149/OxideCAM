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
from pixel_magnitude_list_to_normalized_potential_list import pixel_magnitude_list_to_normalized_potential_list
from normalized_potential_list_to_cam_code_list import normalized_potential_list_to_cam_code_list

#Flatten the input bitmap to a list of pixel magnitudes
(bmp_pixel_width,bmp_pixel_height,number_of_pixels,pixel_magnitude_list)=bmp_to_pixel_magnitude_list("surfviewer.bmp")

#Rescale pixel magnitudes to normalized ([0,1]) electrochemical potentials
normalized_potential_list=pixel_magnitude_list_to_normalized_potential_list(pixel_magnitude_list,{})

#Convert normalized potentials to CAM control codes for the electrochemical voltage source
cam_code_list=normalized_potential_list_to_cam_code_list(normalized_potential_list,{})

#GCode



