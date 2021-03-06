##
#calibration_lookup.py
#Author: Andrew Feldman, 5/3/16
#
#Description: calibration data lookup table with log(size) search time.
#
#Usage:
#-Use to map desired electrochemical output voltage to necessary input PWM
#-Loads OxidePrinter calibration file as a list of output voltages; list index encodes PWM byte
#-Provide a log(size) search functionality which interpolates between PWM values by rounding
#
#Float voltage values which match to within a specified number of decimal places are considered "equal".
#
#Requirements:
#-Number of entries in the calibration file must be a power of two!
#
import math

class CalibrationLookupTable:
    #sig_figs: number of matching significant figures necessary to establish equality between floats
    def __init__(self,decimal_places):
        self.cali_fn=""
        self.equality_threshold=math.pow(10,-decimal_places)
        self.table=[]
        self.table_length=0
        self.min_voltage=float('inf')
        self.max_voltage=0
        
    #calibration_file_name: filename of the file containing OxidePrinter voltage source calibration data
    def load_calibration(self,calibration_file_name):
        self.cali_fn=calibration_file_name    
        self.table=[]
        self.table_length=0
        self.min_voltage=float('inf')
        self.max_voltage=0
        
        cali_file=open(calibration_file_name,'r')
        for file_line in cali_file:
            try:
                val=float(file_line)
                if val < self.min_voltage: self.min_voltage=val
                if val > self.max_voltage: self.max_voltage=val
                self.table.append(val)
            except ValueError: #Fill self.table with calibration file lines that are numeric.
                pass
        cali_file.close()
        
        self.table_length=len(self.table)
        
        
    #log complexity binary search for a table entry that matches output_voltage to within self.equality_threshold
    #Another module calls this method as search(output_voltage), leaving other arguments to their default values.
    #The other arguments are used for recursion.
    def search(self,output_voltage,ptr=-1,L=-1,prev_v_pwm=(-1,-1)):
    
        #Default values
        if L==-1: L=self.table_length
        if ptr==-1: ptr=L/2
        
        if abs(self.table[ptr]-output_voltage)<self.equality_threshold: return ptr #Exact match
        
        #Terminating condition: the below logical operation effectively rounds the PWM byte to a value that must closely reproduces output_voltage
        #It also ensures that the value returned is between 0 and 255
        if L==1: 
            return min(max(ptr + ((prev_v_pwm[0]<self.table[ptr]) == (abs(prev_v_pwm[0]-output_voltage)>abs(self.table[ptr]-output_voltage))),0),255)
            
        #Search upper or lower halfs     
        if output_voltage <self.table[ptr]:
            return self.search(output_voltage,int(ptr-L/4.0),L/2,(self.table[ptr],ptr))
        else:
            return self.search(output_voltage,int(ptr+L/4.0),L/2,(self.table[ptr],ptr))        