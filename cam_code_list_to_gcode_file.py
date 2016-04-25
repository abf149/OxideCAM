##
#cam_code_list_to_gcode_file.py
#Author: Andrew Feldman, 4/24/16
#Description: OxideCAM backend GCODE generator.

#Append an arbitrary number of blank lines to the GCODE file
def blank_lines(number_of_lines=1):
    output_string=""
    for i in range(number_of_lines):
        output_string = output_string + "\n"
    return output_string

#Finish all motion commands in the buffer
def finish_moves_command():    
    return "M400\n"
    
#Set coordinate system to relative
def relative_coordinates_command():
    return "G91\n"

#Move to point in the x/y plane, without affecting z
#Units in mm
def planar_move_command(x,y,feedrate):
    return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " F" + str(feedrate) + "\n"

#Move to a point on the z-axis, without affecting x/y
#units in mm
def z_move_command(z,feedrate): 
    return "G0 Z" + str(z) + " F" + str(feedrate)
    
#positions, dimensions in mm
#does not require float inputs
def cam_code_list_to_gcode_file(output_filename, cam_code_list, plate_x, plate_y, plate_z, plate_width, plate_height, x_pixels, y_pixels, config_dict={}):
    
    pixel_size=(float(plate_width)/float(x_pixels),float(plate_height)/float(y_pixels))
    pixel_center=(pixel_size[0]/2.0,pixel_size[1]/2.0)
    
    outfile=open(output_filename)
    
    #Device initialization
    #Center tool over top-left pixel
    retract=10.0 #REPLACE WITH CONFIG
    move_feedrate=50.0 #REPLACE WITH CONFIG
    retract_feedrate=100.0 #REPLACE WITH CONFIG    
    initial_position=(plate_x+pixel_center[0],plate_y+pixel_center[1],plate_z-retract)
    outfile.write(z_move_command(initial_position[2],retract_feedrate))
    outfile.write(planar_move_command(initial_position[0],initial_position[1],move_feedrate))
    outfile.write(relative_coordinates_command())
    outfile.write(blank_lines(5))
       
    outfile.write(finish_all_moves_command())
    outfile.write(z_move_command(0,0,,))