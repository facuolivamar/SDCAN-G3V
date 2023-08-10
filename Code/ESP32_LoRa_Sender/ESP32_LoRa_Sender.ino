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


/************************Hardware Related Macros************************************/
#define Board_MQ4 ("LoRa ESP32")
#define Pin_MQ4 (38)  //Analog input 4 of your arduino
/***********************Software Related Macros************************************/
#define Type_MQ4 ("MQ-4")  //MQ4
#define Voltage_Resolution_MQ4 (3.3)
#define ADC_Bit_Resolution_MQ4 (12)  // For arduino UNO/MEGA/NANO
#define RatioMQ4CleanAir_MQ4 (4.4)   //RS / R0 = 60 ppm

MQUnifiedsensor MQ4(Board_MQ4, Voltage_Resolution_MQ4, ADC_Bit_Resolution_MQ4, Pin_MQ4, Type_MQ4);


#define Board_MQ131 ("LoRa ESP32")
#define Voltage_Resolution_MQ131 (3.3)
#define Pin_MQ131 (39)                 //Analog input 0 of your arduino
#define Type_MQ131 ("MQ-131")          //MQ131
#define ADC_Bit_Resolution_MQ131 (12)  // For arduino UNO/MEGA/NANO
#define RatioMQ131CleanAir_MQ131 (15)  //RS / R0 = 15 ppm
//#define calibration_button 13 //Pin to calibrate your sensor

//Declare Sensor
MQUnifiedsensor MQ131(Board_MQ131, Voltage_Resolution_MQ131, ADC_Bit_Resolution_MQ131, Pin_MQ131, Type_MQ131);


#define Board_MQ135 ("LoRa ESP32")
#define Voltage_Resolution_MQ135 (3.3)
#define Pin_MQ135 (37) //Analog input 0 of your arduino
#define Type_MQ135 ("MQ-135") //MQ135
#define ADC_Bit_Resolution_MQ135 (12) // For arduino UNO/MEGA/NANO
#define RatioMQ135CleanAir (3.6) //RS / R0 = 3.6 ppm  

MQUnifiedsensor MQ135(Board_MQ135, Voltage_Resolution_MQ135, ADC_Bit_Resolution_MQ135, Pin_MQ135, Type_MQ135);


void setup() {
  //initialize Serial Monitor
  Serial.begin(115200);

  MQ4.setRegressionMethod(1);
  MQ4.init();

  MQ131.setRegressionMethod(1);
  MQ131.setA(23.943);
  MQ131.setB(-1.11);
  MQ131.init();

  Serial.print("Calibrating please wait.");
  float calcR0_MQ4 = 0;
  for (int i = 1; i <= 10; i++) {
    MQ4.update();  // Update data, the arduino will read the voltage from the analog pin
    calcR0_MQ4 += MQ4.calibrate(RatioMQ4CleanAir_MQ4);
    Serial.print(".");
  }
  MQ4.setR0(calcR0_MQ4 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0_MQ4)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1)
      ;
  }
  if (calcR0_MQ4 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1)
      ;
  }
  /*****************************  MQ CAlibration ********************************************/



  Serial.print("Calibrating please wait.");
  float calcR0_MQ131 = 0;
  for (int i = 1; i <= 10; i++) {
    MQ131.update();  // Update data, the arduino will read the voltage from the analog pin
    calcR0_MQ131 += MQ131.calibrate(RatioMQ131CleanAir_MQ131);
    Serial.print(".");
  }
  MQ131.setR0(calcR0_MQ131 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0_MQ131)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1)
      ;
  }
  if (calcR0_MQ131 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1)
      ;
  }
  /*****************************  MQ CAlibration ********************************************/
  MQ131.serialDebug(true);
  Serial.println("Ignore Ratio = RS/R0, for this example we will use readSensorR0Rs, the ratio calculated will be R0/Rs. Thanks :)");


  MQ135.setRegressionMethod(1);
  MQ135.init(); 

  Serial.print("Calibrating please wait.");
  float calcR0_MQ135 = 0;
  for(int i = 1; i<=10; i ++)
  {
    MQ135.update(); // Update data, the arduino will read the voltage from the analog pin
    calcR0_MQ135 += MQ135.calibrate(RatioMQ135CleanAir);
    Serial.print(".");
  }
  MQ135.setR0(calcR0_MQ135/10);
  Serial.println("  done!.");
  
  if(isinf(calcR0_MQ135)) {Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply"); while(1);}
  if(calcR0_MQ135 == 0){Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply"); while(1);}


  while (!Serial)
    ;
  Serial.println("LoRa Sender");

  //setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);

  //replace the LoRa.begin(---E-) argument with your location's frequency
  while (!LoRa.begin(865.0625E6)) {
    Serial.println(".");
    delay(500);
  }

  // Change sync word (0xF3) to match the receiver
  // The sync word assures you don't get LoRa messages from other LoRa transceivers
  // ranges from 0-0xFF
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");


  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP085 sensor, check wiring!");
    while (1) {}
  }


  neogps.begin(9600, SERIAL_8N1, RXD2, TXD2);
}

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(counter);

  //Send LoRa packet to receiver
  LoRa.beginPacket();
  LoRa.print("- Packet ");
  LoRa.print(counter);
  LoRa.print("\n");


  LoRa.print("- Temperature = ");
  LoRa.print(bmp.readTemperature());
  LoRa.print(" *C \n");
  LoRa.print("- Pressure = ");
  LoRa.print(bmp.readPressure());
  LoRa.println(" Pa");
  LoRa.print("- Altitude = ");
  LoRa.print(bmp.readAltitude());
  LoRa.println(" meters");


  MQ4.update();

  MQ4.setA(3811.9);
  MQ4.setB(-3.113);              // Configure the equation to to calculate CH4 concentration
  float LPG = MQ4.readSensor();  // Sensor will read PPM concentration using the model, a and b values set previously or from the setup


  MQ4.setA(1012.7);
  MQ4.setB(-2.786);              // Configure the equation to to calculate CH4 concentration
  float CH4 = MQ4.readSensor();  // Sensor will read PPM concentration using the model, a and b values set previously or from the setup


  MQ131.update();

  float O3 = MQ131.readSensor();


  LoRa.print("- LPG: ");
  LoRa.print(LPG);
  LoRa.print("\n");
  LoRa.print("- CH4: ");
  LoRa.print(CH4);
  LoRa.print("\n");
  LoRa.print("- O3: ");
  LoRa.print(O3);
  LoRa.print("\n");


  MQ135.update();

  MQ135.setA(605.18); MQ135.setB(-3.937); // Configure the equation to calculate CO concentration value
  float CO = MQ135.readSensor(); // Sensor will read PPM concentration using the model, a and b values set previously or from the setup

  MQ135.setA(110.47); MQ135.setB(-2.862); // Configure the equation to calculate CO2 concentration value
  float CO2 = MQ135.readSensor(); // Sensor will read PPM concentration using the model, a and b values set previously or from the setup

  MQ135.setA(102.2 ); MQ135.setB(-2.473); // Configure the equation to calculate NH4 concentration value
  float NH4 = MQ135.readSensor(); // Sensor will read PPM concentration using the model, a and b values set previously or from the setup

  MQ135.setA(44.947); MQ135.setB(-3.445); // Configure the equation to calculate Toluen concentration value
  float Toluen = MQ135.readSensor(); // Sensor will read PPM concentration using the model, a and b values set previously or from the setup


  LoRa.print("- CO: ");
  LoRa.print(CO);
  LoRa.print("\n");
  LoRa.print("- CO2: ");
  LoRa.print(CO2);
  LoRa.print("\n");
  LoRa.print("- NH4: ");
  LoRa.print(NH4);
  LoRa.print("\n");
  LoRa.print("- Toluen: ");
  LoRa.print(Toluen);
  LoRa.print("\n");


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
      LoRa.print("- Latitude: ");
      LoRa.print(gps.location.lat(), 10);
      LoRa.print("\n");
      LoRa.print("- Longitude: ");
      LoRa.print(gps.location.lng(), 10);
      LoRa.print("\n");


      if (gps.speed.isValid() == 1) {
        LoRa.print("- Speed: ");
        LoRa.print(gps.speed.kmph());
        LoRa.print(" km/h");
        LoRa.print("\n");
      }

    } else {
      LoRa.print("No Data");
    }

    LoRa.endPacket();

    counter++;

    delay(1000);
  }
}