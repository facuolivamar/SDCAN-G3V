# Smog Detector CAN (SDCAN)

## Introduction
This readme provides an overview of the Salas Cuna project developed by the Equipo Villada para la Investigación Espacial (EVIE) from Instituto Técnico Salesiano Villada. The project aims to measure and monitor air pollution levels in the province of Córdoba, Argentina, using a CanSat (Satellite in a Can) device. The CanSat will collect data on pressure, temperature, ozone levels, nitrogen oxides, volatile organic compounds, carbon dioxide, and particulate matter. The project's primary mission is to transmit this data to a ground station in real-time, while the secondary mission involves studying pollution levels in different areas of the province.

## Mission Name: SDCAN (Smog Detector CAN)
Patch:
Team Organization: Roles
- Luciano Michalik - Teacher Advisor
- Maximiliano Smidt – Structure Designer
- Valentino Velez – Hardware and Firmware Developer
- Facundo Oliva Marchetto – Software Developer
- Mateo Marchisone – Software Developer and Outreach

## Mission Objectives
Primary Mission:
The primary mission consists of sensing pressure and temperature and transmitting this data to the ground station at least once per second. The initial data obtained from measuring pressure and temperature before launch will be used to calculate the CANSAT's altitude, which will be utilized in the secondary mission.

Secondary Mission:
The secondary mission involves studying pollution levels based on the following factors:
- Topography of Córdoba: The city's topography, combined with the phenomenon of thermal inversion, leads to the accumulation of pollutants near the ground, resulting in the formation of a smog cloud.
- Levels of nitrogen oxides in the Province of Córdoba: The high concentration of vehicles and industrial activities, particularly in the automotive and agricultural sectors, contributes to elevated levels of nitrogen oxides (NOx).
- Levels of volatile organic compounds in the Province of Córdoba: Agricultural and livestock activities, along with industrial processes, generate high levels of volatile organic compounds (VOCs) such as methane, toluene, and ethylene.
- Particulate matter 2.5 PM: Fine particulate matter with a diameter of 2.5 microns (PM2.5), originating from various sources, poses health and environmental risks.

The mission aims to measure air quality, NOx levels, VOCs, ozone (O3), and carbon dioxide (CO2) in different areas of the province, including industrial parks and agricultural zones, complementing the existing air quality monitoring stations in the city of Córdoba.

## Preliminary Design
Physical Layout:
The CANSAT's behavior during the mission will follow these steps:
1. While loaded into the rocket before launch, the CANSAT will remain in a dormant state to conserve energy.
2. Once in flight, the CANSAT will start recording all data.
3. Upon ejection, the CANSAT will initiate data transmission while continuing to gather more information.
4. During freefall descent, the parachute will deploy, ensuring a controlled landing.

Subsystems:
- Microprocessor (Computer): The ESP32-LoRa provided by CONAE will be used to store and transmit data, as well as read and process various sensor measurements.
- Communications: The LoRa module integrated into the ESP32 will enable long-range and low-energy data transmission.
- Sensors:
  - Ozone and nitrogen dioxide sensor (MQ131): Used to measure ozone (O3) and nitrogen oxides (NOx) levels.
  - LPG, methane, and carbon monoxide sensor (MQ4): Measures LPG, methane, and CO levels.
  - Air quality sensor (MQ135): Measures CO2, benzene, and toluene levels.
  - GPS module (GY-NEO6MV2): Provides real-time location coordinates.
  - Dust and particle sensor (GP2Y1010AU0F): Measures 2.5 PM particles in the air.
  - NH3 and NO2 sensor (Mics 6814): Measures ammonia and nitrogen dioxide levels.

- Power Unit: A 3.7V, 1200mAh lithium battery will be used as the power source. Voltage regulators (step-up and step-down) will be employed to supply the required voltages (3.3V and 5V) to different components.

## Budget of Mass
The estimated total mass of the CANSAT is 239.45 grams.

## Integration and Testing
The components will undergo preliminary individual testing before the CANSAT assembly. Integration tests will include parachute functionality, descent control, and data transmission. Additionally, the CANSAT will be subjected to simulated conditions such as vacuum and vibration tests to ensure its integrity.

## Documentation and Results
The project's progress will be documented using GitHub for version control. Various documents will outline each stage of the project. Videos and photos will be taken to capture key milestones. Results will be shared through a YouTube channel and an Instagram account dedicated to the project.

GitHub Repository: [Project Repository](https://github.com/facuolivamar/SDCAN-G3V/tree/main)

YouTube Channel: [EVIE SDCAN](https://www.youtube.com/@ITSV-SDCAN)

Instagram Account: [@sdcan_itsv](https://www.instagram.com/sdcan_itsv/)

For a detailed description and visual representation of the project, please refer to the [project video](https://www.youtube.com/watch?v=PZLdEqGG1FY&ab_channel=ITSV-SDCAN).
