# IoT_ESP32 Temp Relay
  ## Overview
  In this lab, we will build a small IoT monitoring node using an ESP32, DHT22 temperature/humidity sensor, and a relay module. The ESP32 runs MicroPython, periodically samples temperature, and communicates with a Telegram Bot.
  ## Features
  - Utilizes DHT22 sensor to monitor temperature
  - Uses Wi-Fi to connect relay module to telegram bot
  - Prompts user through telegram bot when exceeding temp threshold
  - Automatically turn relay off when below temp threshold
  ## Equipment
  - ESP32 Dev Board (MicroPython firmware flashed)
  - DHT22 sensor
  - Relay module
  - Jumper wires
  - USB cable + laptop with Thonny
  - Wi-Fi access (internet)
  ## Wiring and Installation
  ### + Wiring
  <img width="808" height="536" alt="image" src="https://github.com/user-attachments/assets/6a36e219-cec7-47f2-9d1d-6c52a99e7ad9" />

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

  ## Usage
  1. Configuration
     - Copy the `temperature.py`
     - In the user config, change
       ```
       WIFI_SSID     = "Wi-Fi Network ID"
       WIFI_PASSWORD = "Wi-Fi Password"
       BOT_TOKEN     = "User Telegram Bot Token"
       ALLOWED_CHAT_IDS = {"User Chat ID"}
       ```
  2. Upload and Run
     - Upload the code to Thonny and Run
     - If temp exceeds threshold it will prompt through telegram
     - Else relay will remain off

   ## Working Demo (Screenshots and videos)
   



![working1](https://github.com/user-attachments/assets/c7903fb2-bd94-4a39-b977-4dc81d27c807)



https://github.com/user-attachments/assets/09742c5c-6af9-4544-b580-10c48937a7fa

