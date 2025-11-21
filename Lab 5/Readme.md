# LAB 5 - Mobile App DC Motor Control with Grafana Dashboard

This project will demonstrate design of a mobile application (using MIT App Inventor) to remotely control a DC motor via an ESP32 (MicroPython) web server.
The ESP32 will expose HTTP endpoints (/forward, /backward, /stop, /speed), while the mobile app will send commands over Wi-Fi to control direction and speed.
All control actions and speed updates will be recorded to an IoT dashboard (InfluxDB + Grafana) for real-time monitoring and analysis.

## Features
- ESP32 + L298N, mobile app, and cloud dashboard.
- A custom mobile interface using MIT App Inventor to send REST commands.
- MicroPython to create a lightweight web API for motor control.
- InfluxDB and Grafana to log and visualize actuator data (speed, direction, timestamp).

## Equipment
- ESP32 Dev Board (MicroPython flashed)
- L298N motor driver
- DC motor + power supply (7–12 V)
- Jumper wires + breadboard
- Laptop with Thonny IDE
- Android phone with MIT App Inventor installed
- Wi-Fi access point
- Grafana Cloud account or local InfluxDB server

## Wiring Diagram
| ESP32 Pin | L298N Pin | Function          |
|-----------|-----------|-------------------|
| 25        | ENA       | PWN (Speed)       |
| 26        | IN1       | Motor Direction 1 |
| 27        | IN2       | Motor Direction 2 |
| GND       | GND       | Common Ground     |

<img width="885" height="422" alt="Screenshot 2025-11-21 100222" src="https://github.com/user-attachments/assets/23d0fea0-fc5d-4f39-89d4-85e02b25ea55" />

## App Layout and URL Used

![photo_2025-11-20_11-20-41](https://github.com/user-attachments/assets/d5133df7-a6c1-4a7f-bbf3-357262aab008)

### URL Used

![photo_2025-11-20_11-19-42](https://github.com/user-attachments/assets/7c49a489-a114-41fd-bd01-40a7851c60c3)

## Reflection on Latency and Data Logging

This report summarizes the development of a real-time data logging system for an ESP32 motor control application. It highlights key challenges—timestamp errors, network configuration issues, and logging latency—and the implemented solutions that resulted in accurate, reliable, and efficient motor data monitoring.

### System Overview
+ Components
- ESP32 – Motor control (L298N) + Web UI
- InfluxDB – Time-series logging
- Grafana – Real-time visualization

## Key Challenges & Solutions

1. Timestamp Accuracy

Problem: Logged timestamps appeared as 1995 instead of 2025.
Cause: MicroPython’s time.time() uses the year 2000 epoch and counts from system boot.
Solution:  ntptime.settime()           
           EPOCH_OFFSET = 946684800     
           ts = int(time.time()) + EPOCH_OFFSET
Outcome: Accurate timestamps compatible with InfluxDB.

2. Network Configuration Issues

Problem: Data failed to log when switching WiFi networks.
Cause: Hardcoded InfluxDB IP changed across networks (hotspot vs router).
Solution: Update host IP and plan for:
- mDNS auto-discovery
- Multiple network profiles
- Server reachability checks

3. Logging Latency & Missing Data

Problems Identified
Slider oninput fired 10–20 requests/sec
ESP32 overwhelmed by HTTP requests
Some speed values never reached the database
Missing directional context
Solutions Implemented
1. UI Debounce
Replaced oninput with onchange:
<input onchange="fetch('/speed?value='+this.value)">
2. Server-Side Throttling
LOG_THROTTLE = 0.5   # 500ms minimum interval
3. State Tracking (direction + signed speed)
Positive = forward, negative = backward.

Performance Improvement

| Metric               | Before   | After   |
| -------------------- | -------- | ------- |
| Logs per slider move | 15–25    | 1       |
| Write latency        | 50–200ms | 20–30ms |
| Data accuracy        | ~40%     | ~100%   |
| UI responsiveness    | Laggy    | Smooth  |

### System Insights

+ Latency Sources

- WiFi RTT: 10–15ms
- HTTP overhead
- InfluxDB write time: 15–25ms
- ESP32 single-thread event loop

+ Data Resolution Trade-offs

- High-frequency logging = congestion + duplicates
- Throttled logging = fewer requests, more accurate data
500ms resolution is sufficient due to motor inertia.

+ Grafana Visualization Design

- Speed Time-Series Graph (signed values)
- State Indicator (Forward/Backward/Stop)
- Event Log Table (Chronological commands)

### Lessons Learned

+ System Design

- Start simple, optimize after observing bottlenecks
- Match logging rate to actual physical needs

+ Embedded Constraints

- ESP32 event loop limits concurrency
- HTTP requests are expensive—minimize where possible

+ External time sync (NTP) is essential

- Data Quality
- Context > quantity (speed + direction is more meaningful)
- Client-side intelligence (debounce) reduces load
- Throttling improved accuracy

### Future Improvements

- Buffered offline logging
- Batch InfluxDB writes
- Connection health monitoring
- MQTT for lightweight communication
- Multi-device scalability
- On-device edge processing

### Technical Specifications

Hardware: ESP32, L298N, WiFi 802.11 b/g/n
Software: MicroPython, InfluxDB 1.x, Grafana, NTP
Performance:
- Avg latency: ~25ms
- Max throughput: 2 logs/sec
- Write success rate: >99%
- NTP accuracy: ±50ms 
- UI responsiveness: <100ms
