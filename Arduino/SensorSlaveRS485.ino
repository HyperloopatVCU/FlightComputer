
#include <NewPing.h>
#include <Wire.h>

#define MAX_DISTANCE 50 // Maximum distance (in cm) to ping.

#define TriggerPin 2
#define EchoPin 3

#define Control 7   //RS485 Direction control

#define RS485Transmit    HIGH
#define RS485Receive     LOW


int D;
NewPing sensor = NewPing(TriggerPin, EchoPin, MAX_DISTANCE); // Each sensor's trigger pin, echo pin, and max distance to ping.


void setup() {
  Serial.begin(115200); // initialize interface to host computer
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
  pinMode(Control, OUTPUT); // set control pin mode
}

void requestEvent() {
  digitalWrite(Control, RS485Transmit);  // Enable RS485 Transmit   
  Wire.write(D); //write "D" to the I2C bus
  digitalWrite(Control, RS485Receive);  // Disable RS485 Transmit       
}

void loop() {
  D = sensor.ping_cm(); // Assign the distance in cm to Variable "D"
  Serial.println("Pitch distance: "); Serial.print(D); Serial.print(" cm. ");// Display variables
// Wait 30 ms between pings
delay(30);
}


