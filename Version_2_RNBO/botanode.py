from pythonosc import udp_client
import time
import board
import busio
from adafruit_seesaw.seesaw import Seesaw
import RPi.GPIO as GPIO
from collections import deque
import math

# ----------------------------
# OSC Setup
# ----------------------------
ip = "127.0.0.1"
port = 1234
client = udp_client.SimpleUDPClient(ip, port)

# ----------------------------
# Seesaw Sensor Setup (I2C)
# ----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
seesaw = Seesaw(i2c, addr=0x36)

# ----------------------------
# GPIO Pulse Detection Setup
# ----------------------------
PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

last_state = GPIO.input(PIN)
last_edge_time = time.monotonic()

intervals = deque(maxlen=10)

# Threshold control
default_threshold = 3.5
lowered_threshold = 2.0
threshold = default_threshold

# Timing control
last_output_time = time.monotonic()
min_output_interval = 0.2  # 200 ms
inactivity_duration = 15.0  # Time before threshold lowers

# ----------------------------
# Main Loop
# ----------------------------
last_sensor_time = time.monotonic()

while True:
    try:
        # --- Electrode Pulse Reading ---
        current_state = GPIO.input(PIN)

        if current_state == 1 and last_state == 0:
            now = time.monotonic()
            interval = now - last_edge_time
            last_edge_time = now

            if 0.001 < interval < 0.1:
                intervals.append(interval)

                if len(intervals) == intervals.maxlen:
                    # Check if it's time to lower threshold
                    if now - last_output_time > inactivity_duration:
                        threshold = lowered_threshold
                    else:
                        threshold = default_threshold

                    analysis = list(intervals)[1:]
                    avg = sum(analysis) / len(analysis)
                    stdev = math.sqrt(sum((x - avg) ** 2 for x in analysis) / len(analysis))
                    stdev = max(stdev, 1e-6)
                    delta = max(analysis) - min(analysis)

                    # Only send if both threshold condition and time spacing pass
                    if delta > (stdev * threshold) and (now - last_output_time >= min_output_interval):
                        min_val = min(analysis)
                        max_val = max(analysis)
                        current = intervals[-1]
                        normalized = (current - min_val) / (max_val - min_val)
                        normalized = max(0.0, min(1.0, normalized))

                        client.send_message("/rnbo/inst/0/params/electrode/normalized", normalized)
                        print(f"Electrode interval: {current:.4f}s | Normalized: {normalized:.3f}")
                        last_output_time = now

        last_state = current_state

        # --- Seesaw Sensor Reading (every 75ms) ---
        now = time.monotonic()
        if now - last_sensor_time >= 0.075:
            last_sensor_time = now
            try:
                moisture = seesaw.moisture_read()
                temperature = seesaw.get_temp()

                normalized_moisture = moisture / 1023.0
                normalized_temperature = (temperature - 20) / 40.0

                client.send_message("/rnbo/inst/0/params/soil_moisture/normalized", normalized_moisture)
                client.send_message("/rnbo/inst/0/params/temperature/normalized", normalized_temperature)

                print(f"Sent soil moisture: {normalized_moisture:.3f}")
                print(f"Sent temperature: {normalized_temperature:.3f}")

            except OSError as e:
                print(f"I2C Read Error: {e}")

        time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nExiting cleanly...")
        GPIO.cleanup()
        break

    except Exception as e:
        print(f"Unhandled Error: {e}")
        time.sleep(0.1)
