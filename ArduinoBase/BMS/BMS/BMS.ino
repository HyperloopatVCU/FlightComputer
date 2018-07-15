#include <OneWire.h>

#define ONE_WIRE_BUS 2
#define TEMP_PRECISION 9
#define NUMBER_OF_DS18B20 30

#define DELAY 500

#define SERIAL 1
#define COMPARE 1
#define LOG 1

#define NUMBER_OF_PL200 8
#define VOLTAGE 0
#define CURRENT 1

#define NUMBER_OF_DS18B20 30
#define NUMBER_OF_PL200 8
#define ID_TAG 69

#define VOLTAGE 0
#define CURRENT 1

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

//PL200 ARRAYS
uint16_t analogPinArray[16] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A15};
byte IVDataArray[2][NUMBER_OF_PL200];
uint16_t pl200ErrorArray[NUMBER_OF_PL200];

//DS18B20 ARRAY
byte sensorAddress[NUMBER_OF_DS18B20][8] = {
/*Sensor 0*/   {0x28,0x4,0x77,0xD3,0x8,0x0,0x0,0x52},
/*Sensor 1*/   {0x28,0x29,0xCD,0xD4,0x8,0x0,0x0,0xDA},
/*Sensor 2*/   {0x28,0x53,0x87,0xD3,0x8,0x0,0x0,0x5F},
/*Sensor 3*/   {0x28,0xB3,0xC0,0xD3,0x8,0x0,0x0,0xCE},
/*Sensor 4*/   {0x28,0x88,0xD5,0xD5,0x8,0x0,0x0,0x7C},
/*Sensor 5*/   {0x28,0x38,0x9,0xD4,0x8,0x0,0x0,0x8B},
/*Sensor 6*/   {0x28,0xAC,0xAF,0xD5,0x8,0x0,0x0,0xC6},
/*Sensor 7*/   {0x28,0xF9,0x2A,0xD2,0x8,0x0,0x0,0x9C},
/*Sensor 8*/   {0x28,0xDD,0x80,0xD2,0x8,0x0,0x0,0x78},
/*Sensor 9*/   {0x28,0xFF,0xBE,0xC8,0xC1,0x16,0x4,0x5F},
/*Sensor 10*/  {0x28,0xEB,0xCE,0x8F,0x9,0x0,0x0,0x82},
/*Sensor 11*/  {0x28,0xB1,0x1E,0x8D,0x9,0x0,0x0,0x3A},
/*Sensor 12*/  {0x28,0x5E,0x0,0x8F,0x9,0x0,0x0,0xEE},
/*Sensor 13*/  {0x28,0x14,0xD4,0x8C,0x9,0x0,0x0,0x9D},
/*Sensor 14*/  {0x28,0xE5,0xC7,0x8F,0x9,0x0,0x0,0x62},
/*Sensor 15*/  {0x28,0xF5,0x90,0x8C,0x9,0x0,0x0,0x75},
/*Sensor 16*/  {0x28,0xF5,0x90,0x8C,0x9,0x0,0x0,0x75},
/*Sensor 17*/  {0x28,0x6F,0xB7,0x8F,0x9,0x0,0x0,0x2A},
/*Sensor 18*/  {0x28,0xF8,0xC5,0x8F,0x9,0x0,0x0,0xF0},
/*Sensor 19*/  {0x28,0x93,0x63,0x8D,0x9,0x0,0x0,0x63},
/*Sensor 20*/  {0x28,0x90,0xFD,0x8C,0x9,0x0,0x0,0xA0},
/*Sensor 21*/  {0x28,0x5C,0x8F,0x8F,0x9,0x0,0x0,0x24},
/*Sensor 22*/  {0x28,0xAA,0x68,0x8E,0x9,0x0,0x0,0xE0},
/*Sensor 23*/  {0x28,0x9,0x82,0x8F,0x9,0x0,0x0,0x0D},
/*Sensor 24*/  {0x28,0xA0,0x3B,0x8F,0x9,0x0,0x0,0x7B},
/*Sensor 25*/  {0x28,0xDC,0xA8,0x8C,0x9,0x0,0x0,0xEF},
/*Sensor 26*/  {0x28,0xD1,0x8D,0x8C,0x9,0x0,0x0,0x8F},
/*Sensor 27*/  {0x28,0xFA,0xAC,0x8F,0x9,0x0,0x0,0x7C},
/*Sensor 28*/  {0x28,0x5A,0x30,0x8E,0x9,0x0,0x0,0x39},
/*Sensor 29*/  {0x28,0x2F,0x26,0x8D,0x9,0x0,0x0,0x22}
  };
byte DS18B20DataArray[12][NUMBER_OF_DS18B20];
byte tempDataArray[NUMBER_OF_DS18B20];
uint16_t ds18b20ErrorArray[NUMBER_OF_DS18B20];

OneWire oneWire(ONE_WIRE_BUS); // DS18B20 sensors on pin defined by ONE_WIRE_BUS

//BMS JSON STRUCTURE
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

//JSON FILE FUNCTIONS
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

//FUNCTIONS
void getDS18B20Data(byte (*sensorAddressPointer)[8], byte (*DS18B20DataArrayPointer)[NUMBER_OF_DS18B20]){
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_DS18B20; ++deviceIndex){
    oneWire.reset();
    oneWire.select(sensorAddressPointer[deviceIndex]);
    oneWire.write(0x44); // Initiate temperature conversion
  }
  
  delay(DELAY);     // maybe 750ms is enough, maybe not

  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_DS18B20; ++deviceIndex){
    oneWire.reset();
    oneWire.select(sensorAddressPointer[deviceIndex]);    
    oneWire.write(0xBE);         // Read Scratchpad
    for ( uint8_t i = 0; i < 9; i++) {           // we need 9 bytes
       DS18B20DataArrayPointer[i][deviceIndex]= oneWire.read();
    }
  }
}

void getIVData(byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *analogPinArrayPointer){
  for(uint16_t i = 0; i < (2 * NUMBER_OF_PL200); ++i){
     IVDataArrayPointer[VOLTAGE][i++] = analogRead(analogPinArrayPointer[i++]);
     IVDataArrayPointer[CURRENT][i] = analogRead(analogPinArrayPointer[i]);
  }
}

void errorClear(uint16_t *ds18b20ErrorArrayPointer, uint16_t *pl200ErrorArrayPointer){
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_DS18B20; ++deviceIndex){
    ds18b20ErrorArrayPointer[deviceIndex] = 0;
  }
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_PL200; ++deviceIndex){
    pl200ErrorArrayPointer[deviceIndex] = 0;
  }
}

void DS18B20TempConv(byte (*IVDataArrayPointer)[NUMBER_OF_PL200], float *tempDataArrayPointer[NUMBER_OF_PL200]){
  for(uint16_t deviceIndex = 0; deviceIndex < NUMBER_OF_DS18B20; ++deviceIndex){
    int16_t raw = (DS18B20DataArray[1][deviceIndex] << 8) | DS18B20DataArray[0][deviceIndex];
  
    byte cfg = (DS18B20DataArray[4][deviceIndex] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time

    tempDataArray[deviceIndex] = ((float)raw / 16.0) * 1.8 + 32.0;
  }
}


void DS18B20Error(byte (*DS18B20DataArrayPointer)[NUMBER_OF_DS18B20], uint16_t *ds18b20ErrorArrayPointer){
   //ERROR DETECTION CODE
   return;
}


void PL200Error(byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *pl200ErrorArrayPointer){
  //ERROR DETECTION CODE
  return;
}

void setup() {
  Serial.begin(9600);

  analogReference(INTERNAL2V56);

  //set PL200 sensor pins
  for(uint16_t i = 0; i < (2 * NUMBER_OF_PL200); ++i){
    pinMode(analogPinArray[i], INPUT);
 }
}

void loop() {
  errorClear(ds18b20ErrorArray, pl200ErrorArray);
  getIVData(IVDataArray, analogPinArray);
  getDS18B20Data(sensorAddress, DS18B20DataArray);
  send_json(tempDataArray, IVDataArray, ds18b20ErrorArray, pl200ErrorArray);
}
