# OxideCAM

usage: cam.py [-h] [-of OF]
              Input File Plate Width Plate Height Plate X Plate Y Plate Z

Generate a GCODE file for rendering an image as a patterned electrochemical
deposit on a metal plate.

positional arguments:
  Input File    The relative path to an existing bitmap image file to take as
                input.
  Plate Width   The width (mm) of the metal plate/image surface
  Plate Height  The height (mm) of the metal plate/image surface
  Plate X       X coordinate of the plates top-left corner
  Plate Y       Y coordinate of the plates top-left corner
  Plate Z       Z coordinate of the plate

optional arguments:
  -h, --help    show this help message and exit
  -of OF        Name of the file to create for the tool's GCODE output. A
                .gcode extension is advisable. If omitted, the default output
                file has the same base filename and path as the input, but
                with a .gcode extension.
