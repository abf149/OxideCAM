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
 * Uses 115200 baud serial-over-USB and Arduino Nano ADC pin 0. Max voltage is 3.3V, so you will want to connect the OxidePrinter tool to a voltage divider that brings the voltage at ADC pin 0 below 3.3V.
 * 
 */

void setup() {

  Serial.begin(115200);
  analogReference(DEFAULT); //3.3V analog ref
}

void loop() {
  if(Serial.available() > 0) {
    while (Serial.available() >0) {
      Serial.read();
      delay(100);
    } //Wait for the user to send a request, then make damn sure we've read every byte on the buffer.

    //Measure the OxidePrinter tool voltage and relay it back to the user.
    Serial.println(analogRead(0)*(3.3)/(1023.0));
  }
}
