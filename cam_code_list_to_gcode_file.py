##
#cam_code_list_to_gcode_file.py
#Author: Andrew Feldman, 4/24/16
#Description: OxideCAM backend GCODE generator.
import math

#Append an arbitrary number of blank lines to the GCODE file
def blank_lines(number_of_lines=1):
    output_string=""
    for i in range(number_of_lines):
        output_string = output_string + "\n"
    return output_string

#Delay for some milliseconds    
def dwell_command(dwell_ms):
    return "G4 P" + str(dwell_ms) + "\n"
    
#Finish all motion commands in the buffer
def finish_all_moves_command():    
    return "M400\n"
    
    
#Set coordinate system to absolute
def absolute_coordinates_command():
    return "G90\n"    
    
#Set coordinate system to relative
def relative_coordinates_command():
    return "G91\n"

#Move to point in the x/y plane, without affecting z
#Units in mm
def planar_move_command(x,y,feedrate):
    return "G0 X" + str(x) + " Y" + str(y) + " F" + str(feedrate) + "\n"

#Move to a point on the z-axis, without affecting x/y
#units in mm
def z_move_command(z,feedrate): 
    return "G0 Z" + str(z) + " F" + str(feedrate) + "\n"

#Set PWM duty cycle (byte, 0-255) at input to electrochemical potential source
#In 3D printers this GCODE controls fan speed
def electrochemical_potential_command(duty_cycle_byte):
    return "M106 S" + str(duty_cycle_byte) + "\n"

def resolve_configs(config_dict):
    #What is the diameter (mm) of the tool tip?
    tool_diameter_mm=1.0
    if 'tool_diameter_mm' in config_dict:
        tool_diameter_mm=config_dict['tool_diameter_mm']
    else: print "Warning: no \'tool_diameter_mm\' config setting; defaulting to " + str(tool_diameter_mm)
        
    pointilist=False
    #pointilist: spread pixels out to fit plate size; otherwise: pixels are spaced to ensure contiguous color
    if 'pointilist' in config_dict and config_dict['pointilist']:
        pointilist=True
    else: print "Warning: no \'pointilist\' config setting; defaulting to " + str(pointilist)

    retract_mm=1.0
    if 'retract_mm' in config_dict:
        retract_mm=config_dict['retract_mm']
    else: print "Warning: no \'retract_mm\' config setting; defaulting to " + str(retract_mm)        
    
    move_feedrate_mm_min=1500.0
    if 'move_feedrate_mm_min' in config_dict:
        move_feedrate_mm_min=config_dict['move_feedrate_mm_min']
    else: print "Warning: no \'move_feedrate_mm_min\' config setting; defaulting to " + str(move_feedrate_mm_min)
        
    retract_feedrate_mm_min=100.0
    if 'retract_feedrate_mm_min' in config_dict:
        retract_feedrate_mm_min=config_dict['retract_feedrate_mm_min']
    else: print "Warning: no \'retract_feedrate_mm_min\' config setting; defaulting to " + str(retract_feedrate_mm_min)
        
    grow_time_ms=1000
    if 'grow_time_ms' in config_dict:
        grow_time_ms=config_dict['grow_time_ms']        
    else: print "Warning: no \'grow_time_ms\' config setting; defaulting to " + str(grow_time_ms)    
    
    return (tool_diameter_mm,pointilist,retract_mm,move_feedrate_mm_min,retract_feedrate_mm_min,grow_time_ms)
    
#positions, dimensions in mm
#does not require float inputs
def cam_code_list_to_gcode_file(output_filename, cam_code_list, plate_x, plate_y, plate_z, plate_width, plate_height, x_pixels, y_pixels, config_dict={}):
   
    tool_diameter_mm,pointilist,retract_mm,move_feedrate_mm_min,retract_feedrate_mm_min,grow_time_ms=resolve_configs(config_dict)

    if pointilist:
        pixel_size=(float(plate_width)/float(x_pixels),float(plate_height)/float(y_pixels))
    else:
        pixel_size=(tool_diameter_mm,tool_diameter_mm)
    
    #Displacement from pixel corner to pixel center
    pixel_center=(pixel_size[0]/2.0,pixel_size[1]/2.0)
    
    #Gcode output file
    outfile=open(output_filename,'w')
    
    #Device initialization
    #Center tool over top-left pixel    
    initial_position=(plate_x+pixel_center[0],plate_y+pixel_center[1],plate_z-retract_mm)
    outfile.write(absolute_coordinates_command())    
    outfile.write(electrochemical_potential_command(0))    
    outfile.write(z_move_command(initial_position[2],retract_feedrate_mm_min))
    outfile.write(planar_move_command(initial_position[0],initial_position[1],move_feedrate_mm_min))
    outfile.write(relative_coordinates_command())
    outfile.write(blank_lines(10))
    
    column_index=0
    
    while len(cam_code_list)>0:   
        
        potential = cam_code_list.popleft()
        
        if potential==0: #If this pixel is "blank" (will not result in any electrochemical growth)
            #Do not make contact, move right
            outfile.write(planar_move_command(pixel_size[0],0,move_feedrate_mm_min))    
            outfile.write(blank_lines(1))            
        else:        
            #Draw pixel, move right
            outfile.write(finish_all_moves_command())
            outfile.write(electrochemical_potential_command(potential))
            outfile.write(z_move_command(retract_mm,retract_feedrate_mm_min))
            outfile.write(dwell_command(grow_time_ms))
            outfile.write(z_move_command(-retract_mm,retract_feedrate_mm_min))
            outfile.write(planar_move_command(pixel_size[0],0,move_feedrate_mm_min))    
            outfile.write(blank_lines(1))
    
        column_index+=1
    
        if column_index == x_pixels:
            #Carriage return
            outfile.write(blank_lines(4))        
            outfile.write(planar_move_command(-plate_width,pixel_size[1],move_feedrate_mm_min))
            outfile.write(blank_lines(5))        
            column_index=0            

    outfile.close()