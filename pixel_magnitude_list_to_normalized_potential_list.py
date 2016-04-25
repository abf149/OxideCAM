##
#pixel_magnitude_list_to_normalized_potential_list.py
#Author: Andrew Feldman, 4/24/16
#Description: OxideCAM tool module. Maps pixel magnitude to a normalized scale of electrochemical potential.
#

def pixel_magnitude_list_to_normalized_potential_list(pixel_magnitude_list,config_dict={}):
    min_pixel=float(min(pixel_magnitude_list))
    max_pixel=float(max(pixel_magnitude_list))
    return [(px_mag-min_pixel)*(1.0/(max_pixel-min_pixel)) for px_mag in pixel_magnitude_list]