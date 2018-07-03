#define NUMBER_OF_PL200 8
#define VOLTAGE 0
#define CURRENT 1

byte IVDataArray[2][NUMBER_OF_PL200];
uint16_t analogPinArray[16] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A15};

void getIVData(byte (*IVDataArrayPointer)[NUMBER_OF_PL200], uint16_t *analogPinArrayPointer){
  for(uint16_t i = 0; i < (2 * NUMBER_OF_PL200); ++i){
     IVDataArrayPointer[VOLTAGE][i++] = analogRead(analogPinArrayPointer[i++]);
     IVDataArrayPointer[CURRENT][i] = analogRead(analogPinArrayPointer[i]);
  }
 }
void setup() {
  Serial.begin(9600);

  analogReference(INTERNAL2V56);

 //set sensor pins
 for(uint16_t i = 0; i < (2 * NUMBER_OF_PL200); ++i){
  pinMode(analogPinArray[i], INPUT);
 }
}

void loop() {
  
  getIVData(IVDataArray, analogPinArray);
}
