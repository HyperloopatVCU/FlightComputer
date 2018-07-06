//#include <Ethernet.h>
//#include <OneWire.h>

#define NUMBER_OF_DS18B20 30
#define NUMBER_OF_PL200 8
#define ID_TAG 69

#define VOLTAGE 0
#define CURRENT 1

#define str_l2(X) #X
#define str(X) str_l2(X)

#define HP_TEMP_IND_START 1
#define HP_TEMP_IND_END 2

#define HP_PL200_IND_START 1
#define HP_PL200_IND_END 2

#define LP_TEMP_IND_START 3
#define LP_TEMP_IND_END 4

#define LP_PL200_IND_START 3
#define LP_PL200_IND_END 4

#define BA_TEMP_IND_START 5
#define BA_TEMP_IND_END 6

#define BA_PL200_IND_START 7
#define BA_PL200_IND_END 7

#define BB_TEMP_IND_START 7
#define BB_TEMP_IND_END 8

#define BB_PL200_IND_START 8
#define BB_PL200_IND_END 8

byte IVDataArray[2][NUMBER_OF_PL200];
byte tempDataArray[NUMBER_OF_DS18B20];
uint16_t ds18b20ErrorArray[NUMBER_OF_DS18B20];
uint16_t pl200ErrorArray[NUMBER_OF_PL200];

//EthernetSerial Serial;


//JSON FILE STRUCTURE
struct {
  const String prelude = "{";
  const String info = "\n\t\"identity\":\"BMS\"";
  const String highpower = "\n\t\"high power\":{";
  const String lowpower = "\n\t\"low power\":{";
  const String brakeayy = "\n\t\"brake a\":{";
  const String brakebee = "\n\t\"brake b\":{";
  const String locsuff = "\n\t},";
//TEMP DATA TRANSMISSION STRUCTURE
  struct {
    const String prelude = "\n\t\t\"temperature-";
    const String presuff = "\":{";
    const String error_prelude = "\n\t\t\t\"error\":";
    const String info = "\n\t\t\t\"units\":\"C\"";
    const String temp_prelude = ",\n\t\t\t\"temp\":";
    const String suff = "\n\t\t},";
  }DS18B20;
//VOLTAGE AND CURRENT DATA TRANSMISSION STRUCTURE
  struct{
    const String prelude = "\n\t\t\"voltage&current-";
    const String presuff = "\":{";
    const String error_prelude = "\n\t\t\t\"error\":";
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
  } PL200;
  const String suff = "\n}\n";
} json;

void errorClear(uint16_t *ds18b20ErrorArrayPointer, uint16_t *pl200ErrorArrayPointer){
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_DS18B20; ++deviceIndex){
    ds18b20ErrorArrayPointer[deviceIndex] = 0;
  }
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_PL200; ++deviceIndex){
    pl200ErrorArrayPointer[deviceIndex] = 0;
  }
}

//TEMP DATA TRANSMISSION FUNCTION
void send_temp_data(byte *tempDataArrayPointer, uint16_t sensIndStart, uint16_t sensIndEnd, uint16_t *ds18b20ErrorArrayPointer) { 
  for(uint16_t deviceIndex = sensIndStart; deviceIndex <= sensIndEnd; ++deviceIndex){
    Serial.print(String(json.DS18B20.prelude).c_str());
    Serial.print(deviceIndex, DEC);
    Serial.print(String(json.DS18B20.presuff).c_str());
    Serial.print(String(json.DS18B20.error_prelude).c_str());
    Serial.print(ds18b20ErrorArrayPointer[deviceIndex], DEC); 
    Serial.print(String(json.DS18B20.info).c_str());
    Serial.print(String(json.DS18B20.temp_prelude).c_str());  
    Serial.print(String(tempDataArrayPointer[deviceIndex], DEC).c_str());
    Serial.print(String(json.DS18B20.suff).c_str());
    }
}

//VOLATAGE AND CURRENT TRANSMISSION FUCNTION
void send_pl200_data(byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t pl200IndStart, uint16_t pl200IndEnd, uint16_t *pl200ErrorArrayPointer){
  for(uint16_t deviceIndex = pl200IndStart; deviceIndex <= pl200IndEnd; ++deviceIndex){ 
    Serial.print(String(json.PL200.prelude + String(deviceIndex, DEC) + String(json.PL200.presuff)).c_str());
    Serial.print(String(json.PL200.error_prelude).c_str());
    Serial.print(pl200ErrorArrayPointer[deviceIndex], DEC);
    Serial.print(String(json.PL200.V.prelude).c_str());
    Serial.print(String(json.PL200.V.info).c_str());
    Serial.print(String(json.PL200.V.V_prelude).c_str());
    Serial.print(String(IVDataArrayPointer[VOLTAGE][deviceIndex], DEC).c_str());
    Serial.print(String(json.PL200.V.suff).c_str());
    Serial.print(String(json.PL200.I.prelude).c_str());
    Serial.print(String(json.PL200.I.info).c_str());
    Serial.print(String(json.PL200.I.I_prelude).c_str());
    Serial.print(String(IVDataArrayPointer[CURRENT][deviceIndex], DEC).c_str());
    Serial.print(String(json.PL200.I.suff).c_str());
    Serial.print(String(json.PL200.suff).c_str());
  }
  Serial.print("\b");
}


void send_highpwr(byte *tempDataArrayPointer, byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *ds18b20ErrorArrayPointer, uint16_t *pl200ErrorArrayPointer){
  Serial.print(String(json.highpower).c_str());
  send_temp_data(tempDataArrayPointer, HP_TEMP_IND_START, HP_TEMP_IND_END, ds18b20ErrorArrayPointer);
  send_pl200_data(IVDataArrayPointer, HP_PL200_IND_START, HP_PL200_IND_END, pl200ErrorArrayPointer); 
  Serial.print(String(json.locsuff).c_str());
}


void send_lowpwr(byte *tempDataArrayPointer, byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *ds18b20ErrorArrayPointer, uint16_t *pl200ErrorArrayPointer){
  Serial.print(String(json.lowpower).c_str());
  send_temp_data(tempDataArrayPointer, LP_TEMP_IND_START, LP_TEMP_IND_END, ds18b20ErrorArrayPointer);
  send_pl200_data(IVDataArrayPointer, LP_PL200_IND_START, LP_PL200_IND_END, pl200ErrorArrayPointer);
  Serial.print(String(json.locsuff).c_str());
}


void send_brake_a(byte *tempDataArrayPointer, byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *ds18b20ErrorArrayPointer, uint16_t *pl200ErrorArrayPointer){
  Serial.print(String(json.brakeayy).c_str());
  send_temp_data(tempDataArrayPointer, BA_TEMP_IND_START, BA_TEMP_IND_END, ds18b20ErrorArrayPointer);
  send_pl200_data(IVDataArrayPointer, BA_PL200_IND_START, BA_PL200_IND_END, pl200ErrorArrayPointer);
  Serial.print(String(json.locsuff).c_str()); 
}


void send_brake_b(byte *tempDataArrayPointer, byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *ds18b20ErrorArrayPointer, uint16_t *pl200ErrorArrayPointer){
  Serial.print(String(json.brakebee).c_str());
  send_temp_data(tempDataArrayPointer, BB_TEMP_IND_START, BB_TEMP_IND_END, ds18b20ErrorArrayPointer);
  send_pl200_data(IVDataArrayPointer, BB_PL200_IND_START, BB_PL200_IND_END, pl200ErrorArrayPointer);
  Serial.print(String(json.locsuff).c_str());
}


//JSON FILE TRANSMISSION FUNCTION
void send_json(byte *tempDataArrayPointer, byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *ds18b20ErrorArrayPointer, uint16_t *pl200ErrorArrayPointer) {
  Serial.print(String(json.prelude).c_str());
  Serial.print(String(json.info).c_str());
  send_highpwr(tempDataArrayPointer, IVDataArrayPointer, ds18b20ErrorArrayPointer, pl200ErrorArrayPointer);
  send_lowpwr(tempDataArrayPointer, IVDataArrayPointer, ds18b20ErrorArrayPointer, pl200ErrorArrayPointer);
  send_brake_a(tempDataArrayPointer, IVDataArrayPointer, ds18b20ErrorArrayPointer, pl200ErrorArrayPointer);
  send_brake_b(tempDataArrayPointer, IVDataArrayPointer, ds18b20ErrorArrayPointer, pl200ErrorArrayPointer);
  Serial.print("\b");
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
  errorClear(ds18b20ErrorArray, pl200ErrorArray);
  send_json(tempDataArray, IVDataArray, ds18b20ErrorArray, pl200ErrorArray);

  delay(10000);

}
