##
#OutputStream.py
#Author: Andrew Feldman, 1/18/15
#
#Part of the OxideCAM project. Abstracts to the CNC code output stream, allowing
#GCODE to be redirected to stdout, file, or virtual serial (pronsole).

def writeLine(gcode):
	print(gcode) #Automatically adds newline.
