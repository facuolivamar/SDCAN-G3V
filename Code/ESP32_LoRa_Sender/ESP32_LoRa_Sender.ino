#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <MQUnifiedsensor.h>
#include <TinyGPS++.h>

//define the pins used by the transceiver module
#define ss 18
#define rst 14
#define dio0 26

#define RXD2 16
#define TXD2 17
HardwareSerial neogps(2);
TinyGPSPlus gps;

int counter = 0;
Adafruit_BMP085 bmp;

#define Board ("LoRa ESP32")
#define Voltage_Resolution (3.3)
#define ADC_Bit_Resolution (12)


//MQ4
#define Type_MQ4 ("MQ-4")
#define RatioMQ4CleanAir (4.4)
#define Pin_MQ4 (38)
MQUnifiedsensor MQ4(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin_MQ4, Type_MQ4);


//MQ131
#define Pin_MQ131 (39)                 
#define Type_MQ131 ("MQ-131")          
#define RatioMQ131CleanAir (15)  
MQUnifiedsensor MQ131(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin_MQ131, Type_MQ131);


//MQ135
#define Pin_MQ135 (37)                 
#define Type_MQ135 ("MQ-135")          
#define RatioMQ135CleanAir (3.6)       
MQUnifiedsensor MQ135(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin_MQ135, Type_MQ135);


void setup() {
  //initialize Serial Monitor
  Serial.begin(115200);
  Serial.println();
  Serial.println();
  
  // neogps.begin(115200, SERIAL_8N1, RXD2, TXD2);

  MQ4.setRegressionMethod(1);
  MQ4.init();

  MQ131.setRegressionMethod(1);
  MQ131.setA(23.943);
  MQ131.setB(-1.11);
  MQ131.init();

  MQ135.setRegressionMethod(1);
  MQ135.init();

  // Setups and Calibrates MQ4
  setUpAndCalibrateMQ4();

  // Setups and Calibrates MQ131
  setUpAndCalibrateMQ131();

  // Setups and Calibrates MQ135
  setUpAndCalibrateMQ135();

  // Setup LoRa
  setUpLoRa();

  // Check BMP
  checkBMP();


}

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(counter);

  //Send LoRa packet to receiver
  LoRa.beginPacket();

  printValue("Packet", counter, "");


  printValue("Temperature", bmp.readTemperature(), "°C");
  printValue("Pressure", bmp.readPressure(), "Pa");
  printValue("Altitude", bmp.readAltitude(), "meters");


  MQ4.update();
  printValue("LPG", readLiquidPetrolGas(), "");
  printValue("CH4", readMethane(), "");

  MQ131.update();
  printValue("O3", MQ131.readSensor(), "");

  MQ135.update();
  printValue("CO", readCarbonMonoxide(), "");
  printValue("CO2", readCarbonDioxide(), "");
  printValue("NH4", readAmmonium(), "");
  printValue("Toluen", readToluen(), "");

  // Get locatioan and speed
  //getLocationAndSpeed();

  LoRa.endPacket();

  counter++;

  delay(10);
}


void setUpAndCalibrateMQ4() {
  Serial.print("Calibrating MQ4 please wait.");
  float calcR0 = 0;
  for (int i = 1; i <= 10; i++) {
    MQ4.update();  // Update data, the arduino will read the voltage from the analog pin
    calcR0 += MQ4.calibrate(RatioMQ4CleanAir);
    Serial.print(".");
  }
  MQ4.setR0(calcR0 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1)
      ;
  }
  if (calcR0 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1)
      ;
  }
}

void setUpAndCalibrateMQ131() {
  Serial.print("Calibrating MQ131 please wait.");
  float calcR0 = 0;
  for (int i = 1; i <= 10; i++) {
    MQ131.update();  // Update data, the arduino will read the voltage from the analog pin
    calcR0 += MQ131.calibrate(RatioMQ131CleanAir);
    Serial.print(".");
  }
  MQ131.setR0(calcR0 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1)
      ;
  }
  if (calcR0 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1)
      ;
  }
}

void setUpAndCalibrateMQ135() {
  Serial.print("Calibrating MQ135 please wait.");
  float calcR0 = 0;
  for (int i = 1; i <= 10; i++) {
    MQ135.update();  // Update data, the arduino will read the voltage from the analog pin
    calcR0 += MQ135.calibrate(RatioMQ135CleanAir);
    Serial.print(".");
  }
  MQ135.setR0(calcR0 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1)
      ;
  }
  if (calcR0 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1)
      ;
  }
}

void setUpLoRa() {
  while (!Serial)
    ;
  Serial.println("LoRa Sender");
  LoRa.setPins(ss, rst, dio0);

  while (!LoRa.begin(865.0625E6)) {
    Serial.println(".");
    delay(500);
  }

  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");
}


void checkBMP() {
  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP085 sensor, check wiring!");
    while (1) {}
  }
}



void printValue(char* valueName, double value, char* unit) {
  LoRa.print("- ");
  LoRa.print(valueName);
  LoRa.print(": ");
  LoRa.print(value);
  LoRa.print(" ");
  LoRa.print(unit);
  LoRa.print("\n");
}

float readLiquidPetrolGas() {
  return readMQ4(3811.9, -3.113);
}

float readMethane() {
  return readMQ4(1012.7, -2.786);
}

float readCarbonMonoxide() {
  return readMQ135(605.18, -3.937);
}

float readCarbonDioxide() {
  return readMQ135(110.47, -2.862);
}

float readAmmonium() {
  return readMQ135(102.2, -2.473);
}

float readToluen() {
  return readMQ135(44.947, -3.445);
}

float readMQ4(float a, float b) {
  MQ4.setA(a);
  MQ4.setB(b);
  return MQ4.readSensor();
}

float readMQ135(float a, float b) {
  MQ135.setA(a);
  MQ135.setB(b);
  return MQ135.readSensor();
}

void getLocationAndSpeed() {

  boolean Data = false;
  for (unsigned long start = millis(); millis() - start < 1000;) {
    while (neogps.available()) {
      if (gps.encode(neogps.read())) {
        Data = true;
      }
    }
  }

  if (Data == true) {
    Data = false;

    if (gps.location.isValid() == 1) {

      printLocation();

      if (gps.speed.isValid() == 1) {
        printValue("Speed", gps.speed.kmph(), "km/h");
      }

    } else {
      printValue("No Data", 404, "");
    }
  }
}

void printLocation() {
  LoRa.print("- Latitude: ");
  LoRa.print(gps.location.lat(), 10);
  LoRa.print("\n");
  LoRa.print("- Longitude: ");
  LoRa.print(gps.location.lng(), 10);
  LoRa.print("\n");
}
