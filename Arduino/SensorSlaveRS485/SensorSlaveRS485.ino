 

#include <Wire.h>


#define SDAControl 7    //RS485 Direction control for the SDA line
#define SCLControl 6  //RS485 Direction control for the SCL line

#define RS485Transmit    HIGH // pulse pin high to transmit
#define RS485Receive     LOW // pulse pin low to receive

int x = 0;
char D[6] = "hello"; //this value is the test character array that will be sent to the master when requested

//NewPing sensor = NewPing(TriggerPin, EchoPin, MAX_DISTANCE); // Each sensor's trigger pin, echo pin, and max distance to ping.


void setup() {
  Serial.begin(9600); // initialize interface to host computer
  Serial.println("Slave Arduino Serial Output:");
  Serial.println("Setup...");
  
  pinMode(SDAControl, OUTPUT); // set SDAControl pin mode
  pinMode(SCLControl, OUTPUT); // set SCLControl pin mode
  
  digitalWrite(SDAControl, RS485Receive); //set the RS485 converters to be ready to recieve data from the slave(s)
  Serial.println("Enabled SDA Receive...");
  
  digitalWrite(SCLControl, RS485Receive); //set the RS485 converters to be ready to recieve data from the slave(s)
  Serial.println("Enabled SCL Receive...");

  Wire.begin(8);                // join i2c bus with address #8
  Serial.println("Joined I2C bus as slave...");
  
  Wire.onRequest(requestEvent); // register requestevent
  
  Serial.println("Setup Complete!");
}


void requestEvent() {
  Serial.println("Request Recieved");
  delay(100);
  
  digitalWrite(SDAControl, RS485Transmit);  // Enable RS485 Transmit 
  Serial.println("Transmit Enabled");  
  delay(10);
  
  Wire.write(D); //write "D" to the I2C bus
  Serial.println("Wrote to I2C bus");
  delay(10);
  
  digitalWrite(SDAControl, RS485Receive);  // Disable RS485 Transmit
  Serial.println("Recieve Enabled");  
 
  Serial.print("requestEvent() run:"); Serial.println(x);     
}

void loop()
{
delay(100);
}


