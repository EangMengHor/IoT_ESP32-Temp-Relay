import network
import time
import json
from machine import Pin, I2C
from umqtt.simple import MQTTClient
from bmp280 import BMP280

# ===== Wi-Fi credentials =====
WIFI_SSID = "Robotic WIFI"
WIFI_PASS = "rbtWIFI@2025"

# ===== MQTT setup =====
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
CLIENT_ID = b"esp32-bmp280"
TOPIC = b"/aupp/morning/iotLab2"

# ===== Initialize I2C and BMP280 =====
i2c = I2C(scl=Pin(22), sda=Pin(21))
bmp = BMP280(i2c)

# ===== Connect Wi-Fi =====
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > 15000:
                raise RuntimeError("Wi-Fi connection timeout")
            time.sleep(0.2)
    print("Wi-Fi connected:", wlan.ifconfig())

# ===== Main Loop =====
def main():
    wifi_connect()

    print("Connecting to MQTT broker...")
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=30)
    client.connect()
    print("Connected to MQTT broker:", MQTT_BROKER)

    while True:
        temperature = bmp.temperature
        pressure = bmp.pressure

        payload = json.dumps({
            "temperature": round(temperature, 2),
            "pressure": round(pressure / 100 , 2),
            "altitude": round(bmp.altitude, 2)
        })

        try:
            client.publish(TOPIC, payload)
            print("Published to", TOPIC.decode(), ":", payload)
        except OSError as e:
            print("MQTT publish failed:", e)
            print("Reconnecting to broker...")
            try:
                client.connect()
                print("Reconnected!")
            except Exception as e2:
                print("Reconnect failed:", e2)
                time.sleep(5)

        time.sleep(5)

if __name__ == "__main__":
    main()
