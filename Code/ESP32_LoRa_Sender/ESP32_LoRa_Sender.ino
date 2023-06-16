#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>

//define the pins used by the transceiver module
#define ss 18
#define rst 14
#define dio0 26

int counter = 0;
Adafruit_BMP085 bmp;

void setup() {
  //initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);
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
  LoRa.endPacket();

  counter++;

  delay(1000);
}