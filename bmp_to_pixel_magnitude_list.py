##
#bmp_to_pixel_magnitude_list.py
#Author: Andrew Feldman, 4/10/16
#Description: OxideCAM tool front-end.
#
#Input: Bitmap filepath (as argument to eponymous function) 
#Output: (pixel-width of image, pixel-height of image,total number of pixels, [list of pixel magnitudes sorted by row then column])
#
#"Pixel magnitude" is the pythagorean sum of pixel color components.
#
#On exception: prints error message and attempts to exit gracefully, returning empty list and 0 for width/height/pixel-count
#
#Dependencies: PIL (pip install pillow)
#
#TODO: check that file is a bmp
#TODO: rescale/threshold
#
##

from PIL import Image
import exceptions
import math

#Flatten a 2D array of pixels into a 1D list of pixels
#Example, in MATLAB notation: [1,2,3;4,5,6] => [1,2,3,4,5,6]
def flatten_image(pixel_array,width,height):
    flat_pixel_list=[]
    for y in range(height):
        for x in range(width):
            flat_pixel_list.append(pixel_array[x,y])

    return flat_pixel_list
            
#Pythagorean sum of RGB components of a pixel
def rgb_to_magnitude(rgb_tuple):
    if isinstance( rgb_tuple, int ):
        return rgb_tuple #This image does not have RGB pixels; each pixel is an int.
        
    return math.sqrt(rgb_tuple[0]**2 + rgb_tuple[1]**2 + rgb_tuple[2]**2)    

#See file-top comments    
def bmp_to_pixel_magnitude_list(bmp_filepath):
    #try:
    im = Image.open(bmp_filepath)
    width, height = im.size
    number_of_pixels=width*height
    
    rgb_array = im.load()
    flat_pixel_list=flatten_image(rgb_array,width,height)
    
    return ( width , height , number_of_pixels, [rgb_to_magnitude(flat_pixel_list[i]) for i in range(number_of_pixels)] )
        
    #except exceptions.BaseException as detail: #Complain and then end gracefully
    #    print "FAIL: " + __file__ + ": " + str(detail)
    #    return (0,0,0,[])