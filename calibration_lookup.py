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

class CalibrationLookupTable:
    #sig_figs: number of matching significant figures necessary to establish equality between floats
    def __init__(decimal_places):
        self.cali_fn=cali_fn
        self.decimal_places=decimal_places
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
        
        
    def search(output_voltage,ptr=self.table_length/2,L=self.table_length,prev_v_pwm=(-1,-1)):
        if abs(self.table[ptr]-output_voltage)<#10^-decimal: return ptr
        if L==1:
            return ptr + (prev_v_pwm[0]<self.table[ptr]) != (abs()abs())