//#include <Ethernet.h>
//#include <OneWire.h>

#define NUMBER_OF_DS18B20 30
#define NUMBER_OF_PL200 8
#define ID_TAG 69

#define VOLTAGE 0
#define CURRENT 1

#define str_l2(X) #X
#define str(X) str_l2(X)

byte IVDataArray[2][NUMBER_OF_PL200];
byte tempDataArray[NUMBER_OF_DS18B20];

//EthernetSerial Serial;


//JSON FILE STRUCTURE
struct {
  const String prelude = "{";
  const String info = "\n\t\"identity\":\"ETHER" str(ID_TAG) "\"";

//TEMP DATA TRANSMISSION STRUCTURE
//#ifdef TEMPSENS
  struct {
    const String prelude = ",\n\t\"temperature\":{";
    const String error_prelude = "\n\t\t\"error\":";
    String error = "\"\"";
    struct {
      const String prelude = ",\n\t\t\"DS18B20-";
      const String info = "\n\t\t\t\"units\":\"C\"";
      const String temp_prelude = ",\n\t\t\t\"temp\":";
      const String suff = "\n\t\t}";
    } tempdat;
    const String suff = "\n\t}";
  }DS18B20;
//#endif

//VOLTAGE AND CURRENT DATA TRANSMISSION STRUCTURE
//#ifdef BMS
  struct{
    const String prelude = ",\n\t\"current and voltage\":{";
    struct{
      const String prelude = "\n\t\t\"PL200-";
      struct {
        const String prelude = "\n\t\t\t\"voltage\":{";
        const String info = "\n\t\t\t\t\"units\":\"V\"";
        const String V_prelude = ",\n\t\t\t\t\"V\":";
        const String suff = "\n\t\t\t},";
      } V;
      struct {
        const String prelude = "\n\t\t\t\"current\":{";
        const String info = "\n\t\t\t\t\"units\":\"A\"";
        const String I_prelude = ",\n\t\t\t\t\"A\":";
        const String suff = "\n\t\t\t}";
      } I;
      const String suff = "\n\t\t},";
    }sensor;
    const String suff = "\n\t},";
  } PL200;
//#endif

  const String suff = "\n}\n";
} json;

//Serial.print(String(json.DS18B20.).c_str());

//TEMP DATA TRANSMISSION FUNCTION
void send_temp_data(byte *tempDataArrayPointer) {
  Serial.print(String(json.DS18B20.prelude).c_str());
  Serial.print(String(json.DS18B20.error_prelude).c_str());
  Serial.print(String(json.DS18B20.error).c_str());
  
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_DS18B20; ++deviceIndex){ 
    Serial.print(String(json.DS18B20.tempdat.prelude + String(deviceIndex, DEC) + "\":{").c_str());
    Serial.print(String(json.DS18B20.tempdat.info).c_str());
    Serial.print(String(json.DS18B20.tempdat.temp_prelude).c_str());
    Serial.print(String(tempDataArrayPointer[deviceIndex], DEC).c_str());
    Serial.print(String(json.DS18B20.tempdat.suff).c_str());
    
    }
  Serial.print(String(json.DS18B20.suff).c_str());
}


//VOLATAGE AND CURRENT TRANSMISSION FUCNTION
void send_pl200_data(byte (*IVDataArrayPointer)[NUMBER_OF_PL200]){
  Serial.print(String(json.PL200.prelude).c_str());
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_PL200; ++deviceIndex){ 
    Serial.print(String(json.PL200.sensor.prelude + String(deviceIndex, DEC) + "\":{").c_str());
    
    Serial.print(String(json.PL200.sensor.V.prelude).c_str());
    Serial.print(String(json.PL200.sensor.V.info).c_str());
    Serial.print(String(json.PL200.sensor.V.V_prelude).c_str());
    Serial.print(String(IVDataArrayPointer[VOLTAGE][deviceIndex], DEC).c_str());
    Serial.print(String(json.PL200.sensor.V.suff).c_str());
  
    Serial.print(String(json.PL200.sensor.I.prelude).c_str());
    Serial.print(String(json.PL200.sensor.I.info).c_str());
    Serial.print(String(json.PL200.sensor.I.I_prelude).c_str());
    Serial.print(String(IVDataArrayPointer[CURRENT][deviceIndex], DEC).c_str());
    Serial.print(String(json.PL200.sensor.I.suff).c_str());

    Serial.print(String(json.PL200.sensor.suff).c_str());
    
  }
  Serial.print("\b");
  Serial.print(String(json.PL200.suff).c_str());
}

//JSON FILE TRANSMISSION FUNCTION
void send_json(byte *tempDataArrayPointer, byte (*IVDataArrayPointer)[NUMBER_OF_PL200]) {
  Serial.print(String(json.prelude).c_str());
  Serial.print(String(json.info).c_str());
  send_temp_data(tempDataArrayPointer);
  send_pl200_data(IVDataArrayPointer);
  Serial.print(String(json.suff).c_str());
}
  

void setup() {
  /*
  const byte mac[] = {0xde, 0xad, 0xbe, 0xef, 0xfe, ID_TAG};
  const byte gateway[] = {192,168,1,20};
  const byte netmask[] = {255,255,255,0};
  const byte dns[] = {192,168,1,20};
  const byte ip[] = {192,168,1,49};
  const byte server[] = {192,168,1,20};
  const int port = 23;
  */
  
  Serial.begin(9600);
  while (!Serial);

/*
  Ethernet.begin(mac, ip, dns, gateway, netmask);
  delay(1000);
  
  Serial.setSerialTimeout(99000);
  Serial.println(String(Serial.connect(server, port), DEC));

  if (Serial.connected())
    Serial.println("Connected");
  else {
    Serial.println("Could not connect to server");
    fail(1);
  }
  */
}

void loop() {
  send_json(tempDataArray, IVDataArray);

  delay(10000);

}
