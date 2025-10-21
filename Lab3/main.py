import network, time, json
from umqtt.simple import MQTTClient
from machine import I2C, Pin
from bmp280 import BMP280  # You need bmp280.py on your ESP32 filesystem

SSID = "Robotic WIFI"
PASS = "rbtWIFI@2025"

TB_HOST = "mqtt.thingsboard.cloud"
TB_PORT = 1883
TB_TOKEN = b"sokUO1qTnG9FWULZArgm"
TOPIC   = b"v1/devices/me/telemetry"

# --- Wi-Fi setup ---
w = network.WLAN(network.STA_IF)
w.active(True)
if not w.isconnected():
    w.connect(SSID, PASS)
    t = time.ticks_ms()
    while not w.isconnected():
        if time.ticks_diff(time.ticks_ms(), t) > 15000:
            raise RuntimeError("Wi-Fi timeout")
        time.sleep(0.2)
print("Wi-Fi connected:", w.ifconfig())

# --- MQTT setup ---
c = MQTTClient(b"esp32-tb", TB_HOST, port=TB_PORT, user=TB_TOKEN, password=b"", keepalive=30, ssl=False)
c.connect()
print("Connected to", TB_HOST, ":", TB_PORT)

# --- BMP280 setup ---
# Adjust pins based on your wiring (default I2C pins for ESP32: 21 = SDA, 22 = SCL)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bmp = BMP280(i2c)

# Optional: set the sea level pressure (in hPa) for accurate altitude
bmp.sea_level = 1013.25

# --- Main loop ---
while True:
    temperature = round(bmp.temperature, 2)  # °C
    pressure = round(bmp.pressure, 2)        # hPa
    pressure = pressure/100
    altitude = round(bmp.altitude, 2)        # meters

    payload = {
        "temperature": temperature,
        "pressure": pressure,
        "altitude": altitude
    }

    msg = json.dumps(payload).encode("utf-8")
    print("Publishing to", TOPIC, "payload:", payload)
    c.publish(TOPIC, msg)
    time.sleep(5)

