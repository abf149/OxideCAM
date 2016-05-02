##
#calibration.py
#Author: Andrew Feldman, 5/2/16
#
#Description: Generates a calibration table for the OxidePrinter's electrochemical voltage source.
#
#Usage
#-Provide the COM port names for the OxidePrinter and the calibration DAQ device.
#-calibration.py cycles the voltage source PWM input duty cycle from 0-255
#-For each duty cycle, calibration.py request a measurement of the voltage drop across the OxidePrinter tool from the DAQ device
#-calibration.py generates a table mapping PWM duty cycle to voltage
import serial
import 

DAQ_COM_NAME="COM3"
PRINTER_COM_NAME="COM4"

DAQ_COM = serial.Serial(
    port=DAQ_COM_NAME,
    baudrate=115200,
)

PRINTER_COM = serial.Serial(
    port=PRINTER_COM_NAME,
    baudrate=115200,
)

