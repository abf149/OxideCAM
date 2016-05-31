##
#imgmap.py
#Author: Andrew Feldman, 5/30/16
#Description: Convert an input bitmap to a new bitmap that is indexed to colors printable by the OxidePrinter
from PIL import Image
import numpy as np
import csv
import colorsys as csys
import math

process="dist"

input_file="./composites/tiger_head_rainbow_diag_110_110.bmp"

if process=="hue":
    color_file="./color_data/v_to_hsv.csv"
elif process=="dist" or process=="hsv_dist":
    color_file="./color_data/v_to_rgb.csv"    
    
v_min=5.04521
v_max=31.489147

color_table=[]
color_f=open(color_file,'rb')
color_csv=csv.reader(color_f, delimiter=' ', quotechar='|')

for r in color_csv:
    row=[float(x) for x in r[0].split(',')]
    #V_next=row[0]
    color_table.append([0 for i in range(4)])    
    color_table[-1][0]=row[0]
    color_table[-1][1]=row[1]
    color_table[-1][2]=row[2]
    color_table[-1][3]=row[3]
    
color_f.close()

print("Color table loaded.")

#print(color_table)

im = Image.open(input_file)
width, height = im.size
number_of_pixels=width*height

rgb_array = im.load()

indexed_pic=[]
pixel_dict={}
pixel_array=[]
pixel_hist=[]
index=0

for y in range(width):
    indexed_pic.append([])
    for x in range(height):
        p=rgb_array[x,y]
        if p in pixel_dict: 
            indexed_pic[y].append(pixel_dict[p])
            pixel_hist[pixel_dict[p]]+=1
        else:
            pixel_array.append(p)
            pixel_hist.append(1)
            pixel_dict[p]=index
            indexed_pic[y].append(index)
            index+=1

print("Pixels indexed.")            

import matplotlib.pyplot as pp

pp.hist(pixel_hist)
#print pixel_hist
k=open('hist.csv','w')
for x in pixel_hist:
    k.write(str(x)+'\n')
k.close()
            
palette_map=[0 for i in range(len(pixel_array))]
            
if process=="hue":
    hsv_pixel_array=[csys.rgb_to_hsv(pixel_array[i][0],pixel_array[i][1],pixel_array[i][2]) for i in range(len(pixel_array))]
    
    for i in range(len(hsv_pixel_array)):
        img_hue=hsv_pixel_array[i][0]
    
        min_delta_hue=10
        min_index=-1
        for j in range(len(color_table)):        
            real_hue=color_table[j][1]
            delta_hue=min(abs(img_hue-real_hue),1-abs(img_hue-real_hue))
            #print(delta_hue)
            if delta_hue<min_delta_hue:
                min_delta_hue=delta_hue
                min_index=j
                
        #print(min_index)
        palette_map[i]=min_index
        #print(min_index)

elif process=="dist":
    
    for i in range(len(pixel_array)):
        img_coord=pixel_array[i]
    
        min_dist=100000
        min_index=-1
        for j in range(len(color_table)):        
            real_coord=(color_table[j][1],color_table[j][2],color_table[j][3])
            dist=math.sqrt((img_coord[0]-real_coord[0])**2+(img_coord[1]-real_coord[1])**2+(img_coord[2]-real_coord[2])**2)
            #print(delta_hue)
            if dist<min_dist:
                min_dist=dist
                min_index=j
                
        #print(min_index)
        palette_map[i]=min_index
        #print(min_index)

elif process=="hsv_dist":
    
    for i in range(len(pixel_array)):
        img_coord=pixel_array[i]
    
        hsv_img=csys.rgb_to_hsv(img_coord[0],img_coord[1],img_coord[2])                
    
        min_dist=100000
        min_index=-1
        for j in range(len(color_table)):        
            real_coord=(color_table[j][1],color_table[j][2],color_table[j][3])
           
            hsv_real=csys.rgb_to_hsv(real_coord[0],real_coord[1],real_coord[2])

            delta_hue=(10*min(abs(hsv_real[0]-hsv_img[0]),1-abs(hsv_real[0]-hsv_img[0])))**2.5
            #print delta_hue
            dist=math.sqrt(abs(img_coord[0]-real_coord[0])**2+abs(img_coord[1]-real_coord[1])**2+abs(img_coord[2]-real_coord[2])**2) + delta_hue
            #print(delta_hue)
            if dist<min_dist:
                min_dist=dist
                min_index=j
                
        #print(min_index)
        palette_map[i]=min_index
        #print(min_index)        
        
print("Color-mapping chosen.")
        
palette_V=[color_table[palette_map[i]][0] for i in range(len(palette_map))]            
palette_pwm=[palette_map[i] for i in range(len(palette_map))]

print("Voltage-mapping chosen.")

f=open('test.volt','w')
g=open('test.pwm','w')

for y in range(height):
    for x in range(width):
        f.write(str(palette_V[indexed_pic[y][x]])+'\n')
        g.write(str(palette_pwm[indexed_pic[y][x]])+'\n')
        
f.close()            
            
print("Voltage file written.")
            
outr=[[ color_table[palette_map[indexed_pic[y][x]]][1] for x in range(width)] for y in range(height)]
outg=[[ color_table[palette_map[indexed_pic[y][x]]][2] for x in range(width)] for y in range(height)]
outb=[[ color_table[palette_map[indexed_pic[y][x]]][3] for x in range(width)] for y in range(height)]

if process=="hue":
    for x in range(width):
        for y in range(height):
            outr[y][x],outg[y][x],outb[y][x]=csys.hsv_to_rgb(outr[y][x],outg[y][x],outb[y][x])
            outr[y][x]=255*outr[y][x]
            outg[y][x]=255*outg[y][x]
            outb[y][x]=255*outb[y][x]
            
#print(pixel_array)            
            
rar=np.asarray(outr)
gar=np.asarray(outg)
bar=np.asarray(outb)
rgbArray = np.zeros((width,height,3), 'uint8')
rgbArray[...,0]=rar
rgbArray[...,1]=gar
rgbArray[...,2]=bar
j=Image.fromarray(rgbArray)
j.save("test2.bmp")

print("Image preview saved.")