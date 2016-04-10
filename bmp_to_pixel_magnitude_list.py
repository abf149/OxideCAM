##
#bmp_to_pixel_magnitude_list.py
#Author: Andrew Feldman, 4/10/16
#Description: OxideCAM tool front-end.
#
#Input: Bitmap filepath (as argument to eponymous function) 
#Output: ([list of pixel magnitudes sorted by row then column],pixel-width of image, pixel-height of image,total number of pixels)
#
#"Pixel magnitude" is the pythagorean sum of pixel color components.
#
#On exception: prints error message and attempts to exit gracefully, returning empty list and 0 for width/height/pixel-count
#
#Dependencies: PIL (pip install pillow)
#
#TODO: check that file is a bmp
#
##

from PIL import Image
import exceptions

def bmp_to_pixel_magnitude_list(bmp_filepath):
    try:
        im = Image.open(bmp_filepath)
        width, height = im.size
        number_of_pixels=width*height
        
        rgb_list = im.load()
        
        return ([ for rgb_pixel in im.load()],width,height,number_of_pixels)
        
    except exceptions.BaseException as detail: #Complain and then end gracefully
        print "FAIL: " + __file__ + ": " + detail
        return ([],0,0,0)