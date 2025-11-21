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
