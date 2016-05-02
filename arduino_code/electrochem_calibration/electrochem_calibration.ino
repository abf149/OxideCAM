/**
 * electrochem_calibration.ino
 * Author: Andrew Feldman, 5/1/16
 * 
 * Description: This code is meant to run on an Arduino Nano. The Nano acts as a data acquisition tool for calibrating the OxidePrinter's digitally controlled electrochemical potential source.
 * 
 * Usage:
 * -User sets the OxidePrinter tool's electrochemical potential using a suitable desktop client for interfacing with the OxidePrinter
 * -User transmits an arbitrary string to the Arduino Nano over serial, then waits for a response without sending any further chars.
 * -Nano receives the string and interprets it as a request for a measurement of the OxidePrinter tool's electrochemical potential
 * -Nano measures electrochemical potential via ADC and relays it back to the user via serial
 * 
 * Uses 115200 baud serial-over-USB and Arduino Nano ADC pin 0. uC operating voltage is 5V, so you will want to connect the OxidePrinter tool to a voltage divider that brings the voltage at ADC pin 0 below 5V.
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

    //Average multiple measurements of the OxidePrinter tool voltage and relay it back to the user.
    //Nano ADC readings are integers 0-1023

    long int accumulator=0;
    for(int j=0; j<i; j++) {
      accumulator+=analogRead(0);
    }
    float mean=float(accumulator)/float(i);
    
    Serial.println(mean*(5.0)/(1023.0));
  }
}
