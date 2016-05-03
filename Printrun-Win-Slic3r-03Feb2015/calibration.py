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
import time

DAQ_COM_NAME="COM4"
PRINTER_COM_NAME="COM3"

DAQ_COM = serial.Serial(
    port=DAQ_COM_NAME,
    baudrate=115200,
)

PRINTER_COM = serial.Serial(
    port=PRINTER_COM_NAME,
    baudrate=115200,
)

print "Waiting for DAQ and printer..."
DAQ_COM.isOpen()
PRINTER_COM.isOpen()
print "Found DAQ and printer."
DAQ_COM.write("1")
PRINTER_COM.write("M106 S0\n")
time.sleep(5)

#table=""

f=open("cali.cal","w")

DAQ_COM.flush()
for i in range(256):
    print("PWM="+str(i))
    PRINTER_COM.write("M106 S" + str(i) + "\n")
    time.sleep(1)
    DAQ_COM.write("1111111111")
    while(DAQ_COM.in_waiting==0): pass
    voltage=""
    while(DAQ_COM.in_waiting>0):
        voltage=voltage+DAQ_COM.read(DAQ_COM.in_waiting)
        time.sleep(0.05)
    voltage=float(voltage.strip())
    print(str(voltage))
    #table=table+str(voltage)+"\n"
    f.write(str(voltage)+"\n")
    
f.close()

PRINTER_COM.close()
DAQ_COM.close()
    

