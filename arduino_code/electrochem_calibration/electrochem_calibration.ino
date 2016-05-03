/**
 * electrochem_calibration.ino
 * Author: Andrew Feldman, 5/1/16
 * 
 * Description: This code is meant to run on an Arduino Nano. The Nano acts as a data acquisition tool for calibrating the OxidePrinter's digitally controlled electrochemical voltage source.
 * 
 * Usage:
 * -User sets the OxidePrinter tool's electrochemical potential using a suitable desktop client for interfacing with the OxidePrinter
 * -User transmits an arbitrary string to the Arduino Nano over serial, then waits for a response without sending any further chars.
 * -Nano receives the string and interprets it as a request for a measurement of the voltage drop across the oxide printer tool.
 * -Nano measures the voltage drop via ADC and relays it back to the user via serial
 * 
 * The voltage drop across the OxidePrinter's tool is equal to the potential of the nominally-31.5V rail minus the potential at the output of the voltage source.
 * 
 * Uses 115200 baud serial-over-USB and Arduino Nano ADC pins 0 (voltage source) and 1 (31.5V rail). uC operating voltage is 5V, so you will want to utilize ~1:10 voltage dividers that bring the voltage at ADC pins 0 and 1 below 5V.
 * 
 */

void setup() {

  Serial.begin(115200);
  analogReference(DEFAULT); //5V analog ref
}

void loop() {
  if(Serial.available() > 0) {
    int i=0;
    while (Serial.available() >0) {
      Serial.read();
      i++;
      delay(100);
    } //Wait for the user to send a request (arbitrary string). The length of the request encodes the number of measurements to average.

    //Average multiple measurements of the voltage drop across the OxidePrinter tool and relay it back to the user.
    //31.5V rail is on A1, variable voltage source is on A0. 
    long int A0_accumulator=0;
    long int A1_accumulator=0;
    for(int j=0; j<i; j++) {
      A0_accumulator+=analogRead(0);
      A1_accumulator+=analogRead(1);      
    }
    float mean_differential=(10.931*float(A1_accumulator)-10.958*float(A0_accumulator))/float(i); //Mean of (rail-source)
    
    Serial.println(mean_differential*(4.7825)/(1023.0),6); //Arduino Nano ADC readings are integers 0-1023, which maps to 0-5V
  }
}
