##
#normalized_potential_list_to_cam_code_list.py
#Author: Andrew Feldman, 4/24/16
#Description: Part of the OxideCAM tool. Maps normalized electrochemical potentials to CAM codes for the electrochemical voltage supply.

import collections

def resolve_configs(config_dict):
    min_useful_voltage=6.0
    if 'min_useful_voltage' in config_dict:
        min_useful_voltage=config_dict['min_useful_voltage']
    else: print "Warning: no \'min_useful_voltage\' config setting; defaulting to " + str(min_useful_voltage)
    
    max_useful_voltage=31.489147 
    if 'max_useful_voltage' in config_dict:
        max_useful_voltage=config_dict['max_useful_voltage']        
    else: print "Warning: no \'max_useful_voltage\' config setting; defaulting to " + str(max_useful_voltage)
    
    return (min_useful_voltage,max_useful_voltage)

#normalized_potential_list: list of normalized potentials to use in printing pixels.
#calibration_table: a CalibrationLookupTable pre-loaded with calibration data.
#config_dict: OxideCAM configuration settings.
#
#Returns a list of byte values (0-255) which 
def normalized_potential_list_to_cam_code_list(normalized_potential_list,calibration_table,config_dict={}):
    min_useful_voltage,max_useful_voltage=resolve_configs(config_dict) #Range of electrochemically useful voltages
    
    #Range of voltages the system can generate   
    min_attainable_voltage=calibration_table.min_voltage
    max_attainable_voltage=calibration_table.max_voltage
    
    #The voltage range that we will map normalized potentials onto
    v_range_low=max(min_attainable_voltage,min_useful_voltage)
    v_range_high=min(max_attainable_voltage,max_useful_voltage)
    v_range=v_range_high-v_range_low
    
    #Mapping: normalized potentials -> absolute potentials -> bytes that encode PWM duty cycle
    return collections.deque([calibration_table.search(norm_pot*v_range+v_range_low) for norm_pot in normalized_potential_list])