#include <Wire.h>

#define SDAControl 7  //RS485 Direction control for the SDA line
#define SCLControl 6 // RS485 Direction control for the SCL line

#define RS485Transmit    HIGH
#define RS485Receive     LOW

int serinput = 0;
int x = 0;
int y = 0;
char D;


void setup() {
 
  Serial.begin(9600);  // start serial for output
  Serial.println("Master Arduino Serial Output:");
  Serial.println("Setup...");
  pinMode(SDAControl, OUTPUT); // set SDAControl pin mode
  pinMode(SCLControl, OUTPUT); // set SCLControl pin mode
  digitalWrite(SDAControl, RS485Receive); //set the RS485 converters to be ready to recieve data from the slave(s)
  Serial.println("Enabled SDA Receive...");
  digitalWrite(SCLControl, RS485Transmit); //set the RS485 converters to be ready to recieve data from the slave(s)
  Serial.println("Enabled SCL Transmit...");
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.println("Joined I2C bus as Master...");
  Serial.println("Setup Complete!");
  Serial.println("Press ENTER to send request...");
}

void SendRequest(){ // here we define a function to send a request for data to the slave
  digitalWrite(SDAControl, RS485Transmit);// Enable RS485 Transmit
  Serial.println("Enabled Transmit");
  //delay(10);
  Wire.requestFrom(8, 6);    // request 1 bytes from slave device #8
  Serial.println("Sent Request");
  //delay(10);
  digitalWrite(SDAControl, RS485Receive);  // Disable RS485 Transmit
  Serial.println("Enabled Receive");
  x = x+1;
  Serial.print("SendRequest() run:"); Serial.println(x); 
}

void loop() {
  if ((Serial.available())and(y == 0))
  {
    serinput = Serial.read();

  }
  if (serinput >= 1){
    SendRequest();
    x = 0;
    serinput = 0;
    y = 1;
  }
  
  digitalWrite(SDAControl, RS485Receive);
  //delay(100);
  
  if (Wire.available()){
    Serial.println("Wire is avalable...");
  }
  while (Wire.available()) { // slave may send less than requested
    D = Wire.read(); // receive a byte
    //Serial.println("Wire recieved");Serial.println(D);
    Serial.print(D);
    y = 0;
  }

  delay(100);
}

