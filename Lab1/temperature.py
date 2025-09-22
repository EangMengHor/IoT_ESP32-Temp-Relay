import network, time, urequests, json
from machine import Pin, reset
import dht

# ---------- USER CONFIG ----------
WIFI_SSID = "Robotic WIFI"
WIFI_PASSWORD = "rbtWIFI@2025"

BOT_TOKEN     = "8411242688:AAGQNzzfAIlyrqGGAdTTmG7coVMBIjag1Ro"
ALLOWED_CHAT_IDS = {"933667621"}

RELAY_PIN = 2
DHT_PIN = 4  # GPIO4 for DHT22 sensor
RELAY_ACTIVE_LOW = False
POLL_TIMEOUT_S = 25
TEMP_THRESHOLD = 30  # Temperature threshold in °C
ALERT_INTERVAL = 2   # Alert interval in seconds
DEBUG = True
# ---------------------------------

API = "https://api.telegram.org/bot" + BOT_TOKEN
relay = Pin(RELAY_PIN, Pin.OUT)
sensor = dht.DHT11(Pin(DHT_PIN))  # Initialize DHT22 sensor

# State variables
last_alert_time = 0
alert_active = False
auto_off_notified = False

def _urlencode(d):
    parts = []
    for k, v in d.items():
        if isinstance(v, int):
            v = str(v)
        s = str(v)
        s = s.replace("%", "%25").replace(" ", "%20").replace("\n", "%0A")
        s = s.replace("&", "%26").replace("?", "%3F").replace("=", "%3D")
        parts.append(str(k) + "=" + s)
    return "&".join(parts)

def log(*args):
    if DEBUG:
        print(*args)

# ---- relay control ----
def relay_on():  
    relay.value(0 if RELAY_ACTIVE_LOW else 1)
    global alert_active, auto_off_notified
    alert_active = False  # Stop alerts when relay is turned on
    auto_off_notified = False  # Reset notification flag

def relay_off(): 
    relay.value(1 if RELAY_ACTIVE_LOW else 0)

def relay_is_on(): 
    return (relay.value() == 0) if RELAY_ACTIVE_LOW else (relay.value() == 1)

# ---- DHT22 sensor functions ----
def read_dht_sensor():
    try:
        sensor.measure()  # Trigger measurement
        temp = sensor.temperature()  # Celsius
        hum = sensor.humidity()      # %
        return temp, hum
    except OSError as e:
        log("DHT22 read error:", e)
        return None, None

# ---- Temperature monitoring and alert system ----
def check_temperature_and_alert():
    global last_alert_time, alert_active, auto_off_notified
    
    temp, hum = read_dht_sensor()
    current_time = time.time()
    
    if temp is None:
        return  # Skip if sensor read failed
    
    log(f"Temperature: {temp}°C, Relay: {'ON' if relay_is_on() else 'OFF'}")
    
    # Check if temperature is above threshold and relay is OFF
    if temp >= TEMP_THRESHOLD and not relay_is_on():
        # Send alert every ALERT_INTERVAL seconds
        if current_time - last_alert_time >= ALERT_INTERVAL:
            for chat_id in ALLOWED_CHAT_IDS:
                send_message(chat_id, f"HIGH TEMPERATURE ALERT: {temp:.1f}°C\n Send /on")
            last_alert_time = current_time
            alert_active = True
    
    # Check if temperature dropped below threshold and relay is ON (auto-OFF condition)
    elif temp < TEMP_THRESHOLD and relay_is_on():
        if not auto_off_notified:
            relay_off()
            for chat_id in ALLOWED_CHAT_IDS:
                send_message(chat_id, f"Temperature normalized: {temp:.1f}°C\nRelay automatically turned OFF")
            auto_off_notified = True
            alert_active = False
    
    # Reset auto_off_notified flag when temperature goes above threshold again
    elif temp >= TEMP_THRESHOLD:
        auto_off_notified = False

# ---- Wi-Fi ----
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        t0 = time.time()
        while not wlan.isconnected():
            if time.time() - t0 > 25:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.25)
    print("Wi-Fi OK:", wlan.ifconfig())
    return wlan

# ---- Telegram API ----
def send_message(chat_id, text):
    try:
        url = API + "/sendMessage?" + _urlencode({"chat_id": chat_id, "text": text})
        r = urequests.get(url)
        _ = r.text  # drain
        r.close()
        log("send_message OK to", chat_id)
    except Exception as e:
        print("send_message error:", e)

def get_updates(offset=None, timeout=POLL_TIMEOUT_S):
    qs = {"timeout": timeout}
    if offset is not None:
        qs["offset"] = offset
    url = API + "/getUpdates?" + _urlencode(qs)
    try:
        r = urequests.get(url)
        data = r.json()
        r.close()
        if not data.get("ok"):
            print("getUpdates not ok:", data)
            return []
        return data.get("result", [])
    except Exception as e:
        print("get_updates error:", e)
        return []

def handle_cmd(chat_id, text):
    t = (text or "").strip().lower()
    if t in ("/on", "on"):
        relay_on()
        send_message(chat_id, "Relay: ON")
    elif t in ("/off", "off"):
        relay_off()
        send_message(chat_id, "Relay: OFF")
    elif t in ("/status", "status"):
        temp, hum = read_dht_sensor()
        status_msg = f"Relay: {'ON' if relay_is_on() else 'OFF'}"
        if temp is not None:
            status_msg += f"\nTemperature: {temp:.1f}°C\nHumidity: {hum:.1f}%"
        if alert_active:
            status_msg += "ALERT ACTIVE: High temperature detected!"
        send_message(chat_id, status_msg)
    elif t in ("/temp", "temp", "/temperature", "temperature"):
        temp, hum = read_dht_sensor()
        if temp is not None and hum is not None:
            send_message(chat_id, f"Temperature: {temp:.1f}°C\nHumidity: {hum:.1f}%")
        else:
            send_message(chat_id, "Failed to read sensor data. Please try again.")
    elif t in ("/whoami", "whoami"):
        send_message(chat_id, "Your chat id is: {}".format(chat_id))
    elif t in ("/start", "/help", "help"):
        help_text = """🤖 Temperature Control Bot Commands:
/on - Turn relay ON (cooling)
/off - Turn relay OFF
/status - Check relay status & temperature
/temp - Read temperature & humidity
/whoami - Get your chat ID

Auto Features:
- Alerts when T ≥ 30°C
- Auto-OFF when T < 30°C"""
        send_message(chat_id, help_text)
    else:
        send_message(chat_id, "Unknown command. Try /help for available commands.")

def main():
    connect_wifi()
    relay_off()

    last_id = None
    old = get_updates(timeout=1)
    if old:
        last_id = old[-1]["update_id"]

    print("Bot running. Waiting for commands…")
    print("DHT22 sensor initialized on GPIO", DHT_PIN)
    print(f"Temperature threshold: {TEMP_THRESHOLD}°C")
    print(f"Alert interval: {ALERT_INTERVAL}s")

    while True:
        try:
            if not network.WLAN(network.STA_IF).isconnected():
                connect_wifi()
        except:
            pass

        # Check temperature and send alerts if needed
        check_temperature_and_alert()

        # Check for Telegram commands
        updates = get_updates(offset=(last_id + 1) if last_id is not None else None)
        for u in updates:
            last_id = u["update_id"]
            msg = u.get("message") or u.get("edited_message")
            if not msg:
                continue
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")
            log("From", chat_id, ":", text)

            # Check if chat is authorized
#             if chat_id not in ALLOWED_CHAT_IDS:
#                 send_message(chat_id, "Not authorized.")
#                 continue

            handle_cmd(chat_id, text)

        time.sleep(0.4)

try:
    main()
except Exception as e:
    print("Fatal error:", e)
    time.sleep(5)

    reset()
