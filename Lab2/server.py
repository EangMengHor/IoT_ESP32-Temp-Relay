import usocket as socket
import network
import esp
import gc
from machine import Pin, time_pulse_us, SoftI2C
from time import sleep, sleep_us
import dht
from machine_i2c_lcd import I2cLcd
import json

# Disable debug & collect garbage
esp.osdebug(None)
gc.collect()

# ---------------- WIFI CONFIG ----------------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not station.isconnected():
    pass
print("Connection successful")
print("Network config:", station.ifconfig())

# ---------------- DHT SENSOR ----------------
sensor = dht.DHT11(Pin(4))   # GPIO4 for DHT11

def read_dht():
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except Exception as e:
        print("DHT read error:", e)
        return None, None

# ---------------- ULTRASONIC ----------------
TRIG = Pin(27, Pin.OUT)
ECHO = Pin(26, Pin.IN)

def distance_cm():
    TRIG.off()
    sleep_us(2)
    TRIG.on()
    sleep_us(10)
    TRIG.off()
    t = time_pulse_us(ECHO, 1, 30000)  # timeout 30ms
    if t < 0:
        return None
    return (t * 0.0343) / 2.0  # convert to cm

# ---------------- LCD CONFIG ----------------
I2C_ADDR = 0x27
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

lcd.clear()

# ---------------- RELAY CONFIG ----------------
RELAY_PIN = 2  # GPIO5 for relay
RELAY_ACTIVE_LOW = False
relay = Pin(RELAY_PIN, Pin.OUT)

def relay_on():
    relay.value(0 if RELAY_ACTIVE_LOW else 1)

def relay_off():
    relay.value(1 if RELAY_ACTIVE_LOW else 0)

def relay_is_on():
    return (relay.value() == 0) if RELAY_ACTIVE_LOW else (relay.value() == 1)

relay_off()  # Ensure relay is off at startup

# ---------------- WEB PAGE ----------------
def web_page():
    html = """
    <html>
    <head>
        <title>ESP Control Panel</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial; text-align: center; margin-top: 40px; }
            h1 { color: #0F3376; }
            .button { padding: 10px 20px; margin: 10px; border: none; border-radius: 5px; cursor: pointer; }
            .on { background-color: #4CAF50; color: white; }
            .off { background-color: #f44336; color: white; }
            .action { background-color: #008CBA; color: white; }
        </style>
        <script>
            function fetchData() {
                fetch('/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ultrasonic').innerText = data.ultrasonic + " cm";
                    document.getElementById('temperature').innerText = data.temperature + " °C";
                });
            }
            setInterval(fetchData, 1000);  // Fetch data every second
        </script>
    </head>
    <body>
        <h1>ESP Control Panel</h1>
        <p>Ultrasonic: <span id="ultrasonic">N/A</span></p>
        <p>Temperature: <span id="temperature">N/A</span></p>
        <button class="button action" onclick="location.href='/show_ultrasonic'">Show Ultrasonic</button>
        <button class="button action" onclick="location.href='/show_temp'">Show Temperature</button>
        <br>
        <button class="button on" onclick="location.href='/relay_on'">Relay ON</button>
        <button class="button off" onclick="location.href='/relay_off'">Relay OFF</button>
        <br>
        <form action="/send_text" method="get">
            <input type="text" name="text" placeholder="Enter text for LCD">
            <button class="button action" type="submit">Send</button>
        </form>
    </body>
    </html>
    """
    return html

# ---------------- SERVER ----------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind(('', 80))
s.listen(5)

while True:
    # Continuously update distance and temperature data
    ultrasonic_data = distance_cm()
    temperature_data, _ = read_dht()

    # Handle incoming HTTP requests
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    
    # Ignore favicon.ico requests
    if 'GET /favicon.ico' in request:
        conn.send('HTTP/1.1 404 Not Found\n')
        conn.send('Connection: close\n\n')
        conn.close()
        continue

    # Serve the main web page
    if 'GET / ' in request:
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    # Serve the sensor data as JSON
    elif 'GET /data' in request:
        data = {
            "ultrasonic": f"{ultrasonic_data:.1f}" if ultrasonic_data is not None else "N/A",
            "temperature": f"{temperature_data:.1f}" if temperature_data is not None else "N/A"
        }
        response = json.dumps(data)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    # Handle show ultrasonic data
    elif '/show_ultrasonic' in request:
        if ultrasonic_data is not None:
            lcd.move_to(0, 0)  # First row
            lcd.putstr(f"Dist: {ultrasonic_data:.1f} cm")
        else:
            lcd.move_to(0, 0)
            lcd.putstr("Dist: N/A")
        print("Ultrasonic data displayed on LCD")
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    # Handle show temperature data
    elif '/show_temp' in request:
        if temperature_data is not None:
            lcd.move_to(0, 1)  # Second row
            lcd.putstr(f"Temp: {temperature_data:.1f}C")
        else:
            lcd.move_to(0, 1)
            lcd.putstr("Temp: N/A")
        print("Temperature data displayed on LCD")
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    # Handle relay ON
    elif '/relay_on' in request:
        relay_on()
        print("Relay turned ON")
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    # Handle relay OFF
    elif '/relay_off' in request:
        relay_off()
        print("Relay turned OFF")
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    # Handle custom text input
    elif '/send_text' in request:
        text_start = request.find('/send_text?text=') + len('/send_text?text=')
        text_end = request.find(' ', text_start)
        if text_end == -1:
            text_end = len(request)
        text = request[text_start:text_end].replace('+', ' ')
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(text[:16])  # Display first 16 characters
        print(f"Custom text displayed on LCD: {text}")
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    conn.close()
