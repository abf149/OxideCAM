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
    def __init__(decimal_places):
        self.cali_fn=cali_fn
        self.equality_threshold=math.pow(10,-decimal_places)
        self.table=[]
        self.table_length=0
        
    #calibration_file_name: filename of the file containing OxidePrinter voltage source calibration data
    def load_calibration(calibration_file_name):
        self.table=[]
        self.table_length=0
        
        cali_file=open(calibration_file_name,'r')
        for file_line in cali_file:
            try:
                self.table.append(float(file_line))
            except ValueError: #Fill self.table with calibration file lines that are numeric.
                pass
        cali_file.close()
        
        self.table_length=len(self.table)
        
    #log complexity binary search for a table entry that matches output_voltage to within self.equality_threshold
    #Another module calls this method as search(output_voltage), leaving other arguments to their default values.
    #The other arguments are used for recursion.
    def search(output_voltage,ptr=-1,L=-1,prev_v_pwm=(-1,-1)):
        #Default values
        if L==-1: L=self.table_length
        if ptr==-1: ptr=L/2
    
        if abs(self.table[ptr]-output_voltage)<self.equality_threshold: return ptr #Exact match
        
        if L==1: #Terminating condition: choose PWM byte that best approximates output_voltage
            return ptr + ((prev_v_pwm[0]<self.table[ptr]) != (abs(prev_v_pwm[0]-output_voltage)>abs(self.table[ptr]-output_voltage)))
            
        #Search upper or lower halfs     
        if output_voltage <self.table[ptr]:
            return search(output_voltage,ptr-ptr/2,L/2,(self.table[ptr],ptr))
        else:
            return search(output_voltage,ptr+ptr/2,L/2,(self.table[ptr],ptr))        