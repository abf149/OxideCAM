##
#normalized_potential_list_to_cam_code_list.py
#Author: Andrew Feldman, 4/24/16
#Description: Part of the OxideCAM tool. Maps normalized electrochemical potentials to CAM codes for the electrochemical voltage supply.

def normalized_potential_list_to_cam_code_list(normalized_potential_list,config_dict={}):
    return [norm_pot*255.0 for norm_pot in normalized_potential_list]