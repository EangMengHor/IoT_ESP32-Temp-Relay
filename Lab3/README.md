# IoT-Webserver-with-BMP280-Sensor
## Overview
In this lab, we will build a simple Webserver using **ESP32** and the **BMP280** sensor to measure **temperature**, **pressure**, and **altitude**. The data collected by the sensor will be displayed through a web interface hosted on the ESP32 board.

## Features
- Utilizes **BMP280** sensor to measure:
  - Temperature (°C)
  - Pressure (hPa)
  - Altitude (m)
- Builds a **Webserver** to display real-time sensor readings
- Simple and user-friendly web interface accessible via Wi-Fi

## Equipment
- **ESP32 Dev Board** (flashed with MicroPython firmware)  
- **BMP280 Sensor**  
- **Jumper Wires**  
- **USB Cable + Laptop with Thonny IDE**  
- **Wi-Fi access (Internet)**  

## Wiring and Installation
### + Wiring

| BMP280 Pin | ESP32 Pin |
|-------------|-----------|
| VIN         | 3.3V      |
| GND         | GND       |
| SCL         | GPIO 22   |
| SDA         | GPIO 21   |

<img width="800" alt="bmp280_wiring_diagram" src="https://github.com/user-attachments/assets/example-bmp280-wiring.png" />

### + Installation
- Install **[Thonny IDE](https://thonny.org/)**  
  <img width="735" height="655" alt="Screenshot 2025-09-01 144153" src="https://github.com/user-attachments/assets/565f7346-1d6b-437c-b200-5c666f6f9be6" />

- Configure the Thonny Interpreter  
  <img width="554" height="532" alt="Screenshot 2025-09-01 144754" src="https://github.com/user-attachments/assets/a5ef4f2f-e67f-456a-998e-896004919479" />  
  <img width="721" height="693" alt="Screenshot 2025-09-01 144808" src="https://github.com/user-attachments/assets/fc258244-0738-4982-9ef4-800d402f630e" />  
  <img width="660" height="596" alt="Screenshot 2025-09-01 144840" src="https://github.com/user-attachments/assets/102facab-4a91-40e7-914c-efd92dfc2451" />  

- **Note:**  
  If you encounter *Error Code 2* when flashing the MicroPython firmware, press and hold the **BOOT** button on the ESP32 during installation.  
  <img width="249" height="416" alt="image" src="https://github.com/user-attachments/assets/50c9f1d4-1181-4528-87f3-fbf7ccebe249" />

## Usage
1. **Configuration**
   - Copy the `server.py` file into Thonny.  
   - Update the Wi-Fi credentials in the user configuration section:
     ```python
     WIFI_SSID     = "Your_WiFi_Name"
     WIFI_PASSWORD = "Your_WiFi_Password"
     ```

2. **Upload and Run**
   - Upload the code to your ESP32 using Thonny.
   - Run the script.
   - The ESP32 will display its IP address in the Thonny Shell.
   - Open that IP address in your web browser to access the webserver and view:
     - **Temperature**
     - **Pressure**
     - **Altitude**

## Working Demo (Screenshots or Videos)
![bmp280-demo](https://github.com/user-attachments/assets/example-bmp280-demo.png)

> Example: Real-time temperature, pressure, and altitude readings displayed on the web interface.
