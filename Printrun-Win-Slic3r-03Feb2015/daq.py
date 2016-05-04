##
#calibration.py
#Author: Andrew Feldman, 5/2/16
#
#Description: Generates a calibration table for the OxidePrinter's electrochemical voltage source.
#
#Usage
#-Provide the COM port names for the OxidePrinter and the calibration DAQ device.
#-calibration.py cycles the voltage source PWM input duty cycle from 0-255
#-For each duty cycle, calibration.py request a measurement of the mean voltage drop across the OxidePrinter tool from the DAQ device
#-calibration.py generates a table mapping PWM duty cycle at the voltage source input to voltage at its output
#
#The DAQ module averages 10 ADC readings before returning a voltage drop measurement.
#
#Each value in the output file is a voltage, and the line number of that value is the corresponding PWM duty cycle.
#
import serial
import time

#Set by user
DAQ_COM_NAME="COM4"
#PRINTER_COM_NAME="COM3"

print "Starting..."

DAQ_COM = serial.Serial(
    port=DAQ_COM_NAME,
    baudrate=115200,
)
print "Connected to DAQ."


#print "Connected to OxidePrinter."

print "Waiting for DAQ and printer..."
DAQ_COM.isOpen()
#PRINTER_COM.isOpen()
print "Found DAQ and printer."

#Give the DAQ and printer time to be fully ready
DAQ_COM.write("1")
#PRINTER_COM.write("M106 S0\n")
time.sleep(5)

f=open("cali.cal","w") #Calibration table file

DAQ_COM.flush()
for i in range(256):
    #For PWM input duty cycles 0-255
    
    print("PWM="+str(i))
    #Send PWM duty cycle command to printer,
    #wait while the printer works,
    #request a measurement from the DAQ of
    #the mean voltage drop across the printer tool,
    #and wait for a response
    #PRINTER_COM.write("M106 S" + str(i) + "\n")
    time.sleep(1)
    DAQ_COM.write("1111111111") #Average 10 ADC readings
    while(DAQ_COM.in_waiting==0): pass
    
    voltage=""
    while(DAQ_COM.in_waiting>0):
        #Collect all response chars from the DAQ,
        #making sure to wait between bursts of bytes
        #so that we don't miss any.
        voltage=voltage+DAQ_COM.read(DAQ_COM.in_waiting)
        time.sleep(0.05)
        
    #Write a table entry for this (PWM,voltage) pair    
    voltage=float(voltage.strip())
    print(str(voltage))
    f.write(str(voltage)+"\n")
    
#Be graceful now...
f.close()
#PRINTER_COM.close()
DAQ_COM.close() #The DAQ really cares about this.
    

