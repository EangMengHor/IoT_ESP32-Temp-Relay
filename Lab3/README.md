# IoT-BMP280-Sensor-with-ThingsBoard-Cloud
## Overview
In this lab, we will use an **ESP32** with the **BMP280** sensor to measure **temperature**, **pressure**, and **altitude**.  
The ESP32 connects to **Wi-Fi** and sends the sensor data to **ThingsBoard Cloud** using the **MQTT protocol** for real-time IoT monitoring and visualization.

## Features
- Utilizes **BMP280** sensor to measure:
  - Temperature (°C)
  - Pressure (hPa)
  - Altitude (m)
- Connects to **Wi-Fi**
- Publishes sensor data to **ThingsBoard Cloud** using **MQTT**
- Provides real-time IoT data visualization on the dashboard

## Equipment
- **ESP32 Dev Board** (flashed with MicroPython firmware)  
- **BMP280 Sensor**  
- **Jumper Wires**  
- **USB Cable + Laptop with Thonny IDE**  
- **Wi-Fi access (Internet)**  
- **ThingsBoard Cloud account** ([https://thingsboard.cloud](https://thingsboard.cloud))

## Wiring and Installation
### + Wiring

| BMP280 Pin | ESP32 Pin |
|-------------|-----------|
| VIN         | 3.3V      |
| GND         | GND       |
| SCL         | GPIO 22   |
| SDA         | GPIO 21   |

<img width="800" alt="bmp280_wiring_diagram" src="https://github.com/Theara-Seng/iot_micropython/blob/main/Lab3/image/connection.png" />

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
   - Copy the `main.py` file into Thonny.  
   - Update the Wi-Fi and ThingsBoard credentials in the user configuration section:
     ```python
     WIFI_SSID     = "Your_WiFi_Name"
     WIFI_PASSWORD = "Your_WiFi_Password"
     THINGSBOARD_HOST = "mqtt.thingsboard.cloud"
     ACCESS_TOKEN = "Your_Device_Access_Token"
     ```

2. **Upload and Run**
   - Upload the code to your ESP32 using Thonny.
   - Run the script.
   - The ESP32 will:
     - Connect to your Wi-Fi network
     - Read data from the BMP280 sensor
     - Publish sensor data to ThingsBoard Cloud via MQTT

3. **View Data on ThingsBoard**
   - Log in to your **ThingsBoard Cloud** account.
   - Go to your device dashboard to view real-time:
     - **Temperature**
     - **Pressure**
     - **Altitude**
   - You can also visualize the data using charts and gauges.

## Code Overview
```python
# Key Functional Sections:
# 1. Connect to Wi-Fi using provided SSID and password
# 2. Initialize BMP280 sensor via I2C
# 3. Read temperature, pressure, and altitude
# 4. Establish MQTT connection with ThingsBoard Cloud
# 5. Publish sensor data periodically
