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

#Import toolchain modules
from bmp_to_pixel_magnitude_list import bmp_to_pixel_magnitude_list
from pixel_magnitude_list_to_normalized_potential_list import pixel_magnitude_list_to_normalized_potential_list
from normalized_potential_list_to_cam_code_list import normalized_potential_list_to_cam_code_list
from cam_code_list_to_gcode_file import cam_code_list_to_gcode_file

import os
import argparse
import ConfigParser

#Parse CMD arguments
parser = argparse.ArgumentParser(description='Generate a GCODE file for rendering an image as a patterned electrochemical deposit on a metal plate.')
parser.add_argument('Input File', help='The relative path to an existing bitmap image file to take as input.')
parser.add_argument('Plate Width', type=float, help='The width (mm) of the metal plate/image surface')
parser.add_argument('Plate Height', type=float, help='The height (mm) of the metal plate/image surface')
parser.add_argument('Plate X', type=float, help='X coordinate of the plates top-left corner')
parser.add_argument('Plate Y', type=float, help='Y coordinate of the plates top-left corner')
parser.add_argument('Plate Z', type=float, help='Z coordinate of the plate')
parser.add_argument('-of', help='Name of the file to create for the tool\'s GCODE output. A .gcode extension is advisable. If omitted, the default output file has the same base filename and path as the input, but with a .gcode extension.', default="0|")

input_vars = vars(parser.parse_args())
plate_x=input_vars['Plate X']
plate_y=input_vars['Plate Y']
plate_z=input_vars['Plate Z']
plate_width=input_vars['Plate Width']
plate_height=input_vars['Plate Height']
input_filename=input_vars['Input File']
output_filename=input_vars['of']

#Determine output filename
pre, ext = os.path.splitext(input_filename)
if output_filename=="0|": output_filename=pre+".gcode"

#Load configuration file
config = ConfigParser.RawConfigParser()
config.read('cam.cfg')
config_dict = {'tool_diameter_mm':config.getfloat('Section1', 'tool_diameter_mm'),'pointilist':config.getboolean('Section1','pointilist'),'retract_mm':config.getfloat('Section1','retract_mm'),'move_feedrate_mm_min':config.getfloat('Section1','move_feedrate_mm_min'),'retract_feedrate_mm_min':config.getfloat('Section1','retract_feedrate_mm_min'),'grow_time_ms':config.getint('Section1','grow_time_ms')}

#Flatten the input bitmap to a list of pixel magnitudes
(bmp_pixel_width,bmp_pixel_height,number_of_pixels,pixel_magnitude_list)=bmp_to_pixel_magnitude_list(input_filename)

#Rescale pixel magnitudes to normalized ([0,1]) electrochemical potentials
normalized_potential_list=pixel_magnitude_list_to_normalized_potential_list(pixel_magnitude_list,config_dict)

#Convert normalized potentials to CAM control codes for the electrochemical voltage source
cam_code_list=normalized_potential_list_to_cam_code_list(normalized_potential_list,config_dict)

#GCode
cam_code_list_to_gcode_file(output_filename, cam_code_list, plate_x, plate_y, plate_z, plate_width, plate_height, bmp_pixel_width, bmp_pixel_height, config_dict)

