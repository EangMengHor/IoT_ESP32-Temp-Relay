# IoT-Webserver-with-LED-Sensors-and-LCD-Control
## Overview 
 In this lab, we will build a Webserver to display the distance and temperature using ESP32, temperature/humidity sensor (DHT22), ultrasonic sensor and LCD display. 
## Features
 - Utilizes DHT22 to monitor the temperature
 - Utilizes Ultrasonic Sensor to monitor the distance
 - Build a Webserver to control the DHT22 and Ultrasonic Sensor
 - Show the information on a LCD display
## Equipment
 - ESP32 Dev Board (MicroPython firmware flashed)
 - DHT22 
 - Ultrasonic Sensor
 - Jumper wires
 - USB cable + laptop with Thonny
 - Wi-Fi access (internet)
## Wiring and Installation
### + Wiring
<img width="972" height="523" alt="Screenshot 2025-09-15 092408" src="https://github.com/user-attachments/assets/33bd9344-e12a-4377-909b-e9c7a061a9b6" />
  
 ### + Installation
  - Install [Thonny IDE](https://thonny.org/)
<img width="735" height="655" alt="Screenshot 2025-09-01 144153" src="https://github.com/user-attachments/assets/565f7346-1d6b-437c-b200-5c666f6f9be6" />
    
  - Configure Thonny interpreter
<img width="554" height="532" alt="Screenshot 2025-09-01 144754" src="https://github.com/user-attachments/assets/a5ef4f2f-e67f-456a-998e-896004919479" />
<img width="721" height="693" alt="Screenshot 2025-09-01 144808" src="https://github.com/user-attachments/assets/fc258244-0738-4982-9ef4-800d402f630e" />
<img width="660" height="596" alt="Screenshot 2025-09-01 144840" src="https://github.com/user-attachments/assets/102facab-4a91-40e7-914c-efd92dfc2451" />

  - **Note:**
    In cases of error code 2 when installing interpreter, when downloading hold the small boot button on the ESP32 chip
<img width="249" height="416" alt="image" src="https://github.com/user-attachments/assets/50c9f1d4-1181-4528-87f3-fbf7ccebe249" />

 Thonny IDE  "https://thonny.org/".

  ## Usage
  1. Configuration
     - Copy the `server.py`
     - In the user config, change
       ```
       WIFI_SSID     = "Wi-Fi Network ID"
       WIFI_PASSWORD = "Wi-Fi Password"
       ```
  2. Upload and Run
     - Upload the code to Thonny and Run
     - Click on the wanted action




 ## Working Demo (Screenshots and videos)

![photo_2025-09-11_09-43-37](https://github.com/user-attachments/assets/c0b3ea21-3db0-456c-82c1-de36882db020)

https://github.com/user-attachments/assets/b4ba0532-9a1f-4f7a-81ee-6e4b2587af3a


