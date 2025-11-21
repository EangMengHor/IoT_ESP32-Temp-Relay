import network, socket, ure, time
from machine import Pin, PWM
import urequests
import ntptime

# ---------------------------------------------------------
#                   Wi-Fi Config
# ---------------------------------------------------------
WIFI_SSID = "Robotic WIFI"
WIFI_PASS = "rbtWIFI@2025"
INFLUX_DB = "esp32logs"      # Your InfluxDB database
INFLUX_HOST = "10.30.0.182"  # UPDATE THIS! Find your Mac's IP on Robotic WIFI

def wifi_connect():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect()         # disconnect from any previous network
    time.sleep(1)

    print("Connecting to WiFi:", WIFI_SSID)
    sta.connect(WIFI_SSID, WIFI_PASS)

    for _ in range(80):
        if sta.isconnected():
            break
        time.sleep(0.25)

    if not sta.isconnected():
        raise RuntimeError("WiFi connect failed")

    ip = sta.ifconfig()[0]
    print("WiFi connected! IP:", ip)
    return ip

def sync_time():
    """Sync time with NTP server"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Syncing time (attempt {attempt + 1}/{max_retries})...")
            ntptime.settime()  # Sync with NTP server
            current_time = time.localtime()
            print(f"Time synced: {current_time[0]}-{current_time[1]:02d}-{current_time[2]:02d} "
                  f"{current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}")
            return True
        except Exception as e:
            print(f"NTP sync failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    print("WARNING: Could not sync time with NTP server!")
    return False

# ---------------------------------------------------------
#               InfluxDB 1.x Configuration
# ---------------------------------------------------------
# MicroPython time.time() returns seconds since 2000-01-01
# Unix timestamp starts from 1970-01-01
# Offset: 946684800 seconds (30 years difference)
EPOCH_OFFSET = 946684800

def log_to_influx(action, speed, direction="stop"):
    ts = int(time.time()) + EPOCH_OFFSET  # Convert to Unix timestamp
    line = f"motor_logs action=\"{action}\",speed={speed},direction=\"{direction}\" {ts}000000000"
    url = f"http://{INFLUX_HOST}:8086/write?db={INFLUX_DB}"
    try:
        r = urequests.post(url, data=line)
        print("InfluxDB:", r.status_code, r.text)
        r.close()
    except Exception as e:
        print("Influx error:", e)

# ---------------------------------------------------------
#                   Motor Pins Setup
# ---------------------------------------------------------
IN1 = Pin(26, Pin.OUT)
IN2 = Pin(27, Pin.OUT)
ENA = PWM(Pin(25), freq=1000)

PWM_MAX = 1023
_speed_pct = 70
_current_direction = "stop"  # Track current motor state
_last_log_time = 0
LOG_THROTTLE = 0.5  # Minimum seconds between logs

def set_speed(pct, log=False):
    global _speed_pct, _last_log_time
    pct = int(max(0, min(100, pct)))
    _speed_pct = pct
    ENA.duty(int(PWM_MAX * (_speed_pct / 100.0)))
    print("Speed:", _speed_pct, "%")
    
    # Only log if requested and enough time has passed
    if log and (time.time() - _last_log_time) >= LOG_THROTTLE:
        _last_log_time = time.time()
        # Log with current direction and adjusted speed
        if _current_direction == "forward":
            log_to_influx("speed_change", _speed_pct, "forward")
        elif _current_direction == "backward":
            log_to_influx("speed_change", -_speed_pct, "backward")
        else:
            log_to_influx("speed_change", 0, "stop")

def motor_forward():
    global _current_direction, _last_log_time
    set_speed(_speed_pct)
    IN1.on()
    IN2.off()
    _current_direction = "forward"
    print("Forward")
    _last_log_time = time.time()
    log_to_influx("forward", _speed_pct, "forward")

def motor_backward():
    global _current_direction, _last_log_time
    set_speed(_speed_pct)
    IN1.off()
    IN2.on()
    _current_direction = "backward"
    print("Backward")
    _last_log_time = time.time()
    log_to_influx("backward", -_speed_pct, "backward")

def motor_stop():
    global _current_direction, _last_log_time
    IN1.off()
    IN2.off()
    ENA.duty(0)
    _current_direction = "stop"
    print("Stop")
    _last_log_time = time.time()
    log_to_influx("stop", 0, "stop")

# ---------------------------------------------------------
#                      HTTP Server
# ---------------------------------------------------------
HEAD_OK_TEXT = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\n"
)

HEAD_OK_HTML = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\n"
)

HEAD_404 = (
    "HTTP/1.1 404 Not Found\r\n"
    "Content-Type: text/plain\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\nNot Found"
)

HOME_HTML = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<h3>ESP32 Motor</h3>
<p>
  <a href="/forward"><button>Forward</button></a>
  <a href="/backward"><button>Backward</button></a>
  <a href="/stop"><button>Stop</button></a>
</p>
<p>
  <label>Speed:</label>
  <input id="spd" type="range" min="0" max="100" value="70"
    oninput="this.nextElementSibling.textContent=this.value"
    onchange="fetch('/speed?value='+this.value).then(r=>r.text()).then(console.log);">
  <span>70</span>
</p>
"""

def route(path):
    if path == "/" or path.startswith("/index"):
        return HEAD_OK_HTML + HOME_HTML

    if path.startswith("/forward"):
        motor_forward()
        return HEAD_OK_TEXT + "forward"

    if path.startswith("/backward"):
        motor_backward()
        return HEAD_OK_TEXT + "backward"

    if path.startswith("/stop"):
        motor_stop()
        return HEAD_OK_TEXT + "stop"

    if path.startswith("/speed"):
        m = ure.search(r"value=(\d+)", path)
        if m:
            set_speed(int(m.group(1)), log=True)  # Enable logging for slider
            return HEAD_OK_TEXT + "speed=" + m.group(1)
        return HEAD_OK_TEXT + "speed?value=0..100"

    print("Unknown path:", path)
    return HEAD_404

def start_server(ip):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(3)
    print("HTTP:", "http://%s/" % ip)

    while True:
        try:
            cl, _ = s.accept()
            cl.settimeout(2)
            try:
                req = cl.recv(1024)
                if not req:
                    cl.close()
                    continue

                try:
                    text = req.decode("utf-8", "ignore")
                except:
                    text = str(req)

                first = ""
                for ln in text.split("\r\n"):
                    if ln:
                        first = ln
                        break

                parts = first.split(" ")
                path = parts[1] if len(parts) >= 2 else "/"

                response = route(path)
                cl.sendall(response)

            except Exception as e:
                print("Handler error:", e)
            finally:
                try:
                    cl.close()
                except:
                    pass

        except Exception as e:
            print("Accept error:", e)
            time.sleep(0.1)

# ---------------------------------------------------------
#                        Main
# ---------------------------------------------------------
if __name__ == "__main__":
    ip = wifi_connect()       # connect WiFi FIRST
    sync_time()               # sync time with NTP
    motor_stop()              # now safe
    set_speed(_speed_pct)
    start_server(ip)