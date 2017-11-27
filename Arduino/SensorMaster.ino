#include <Wire.h>

#define Control 3   //RS485 Direction control

#define RS485Transmit    HIGH
#define RS485Receive     LOW


void setup() {
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
}

void loop() {
  digitalWrite(Control, RS485Transmit);  // Enable RS485 Transmit  
  Wire.requestFrom(8, 1);    // request 1 bytes from slave device #8
  digitalWrite(Control, RS485Receive);  // Disable RS485 Transmit  

  while (Wire.available()) { // slave may send less than requested
    int D = Wire.read(); // receive a byte as int
    Serial.print("Distance: "); Serial.print(D); Serial.println(" cm. ");// Display variables 
  }

  delay(25);
}

