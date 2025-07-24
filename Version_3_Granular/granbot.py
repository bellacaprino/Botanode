import time
import board
import busio
from adafruit_seesaw.seesaw import Seesaw
import RPi.GPIO as GPIO
import mido
from pythonosc import udp_client
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
# GPIO Setup
# ----------------------------
PIN = 4
LDR_PIN = 14
ENC_A = 16
ENC_B = 20
ENC_SW = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ----------------------------
# Encoder State
# ----------------------------
last_clk_state = GPIO.input(ENC_A)
last_button_state = GPIO.input(ENC_SW)
encoder_position = 1  # Start at 1
min_position = 1
max_position = 8

# ----------------------------
# MIDI Setup
# ----------------------------
midi_input = mido.open_input()

# ----------------------------
# Pulse Detection Setup
# ----------------------------
last_state = GPIO.input(PIN)
last_edge_time = time.monotonic()
intervals = deque(maxlen=10)

default_threshold = 3.5
lowered_threshold = 2.0
threshold = default_threshold

last_output_time = time.monotonic()
min_output_interval = 0.2
inactivity_duration = 15.0

# ----------------------------
# Main Loop
# ----------------------------
last_sensor_time = time.monotonic()

try:
    while True:
        # --- Electrode Pulse ---
        current_state = GPIO.input(PIN)
        if current_state == 1 and last_state == 0:
            now = time.monotonic()
            interval = now - last_edge_time
            last_edge_time = now
            if 0.001 < interval < 0.1:
                intervals.append(interval)
                if len(intervals) == intervals.maxlen:
                    if now - last_output_time > inactivity_duration:
 threshold = lowered_threshold
                    else:
                        threshold = default_threshold

                    analysis = list(intervals)[1:]
                    avg = sum(analysis) / len(analysis)
                    stdev = math.sqrt(sum((x - avg) ** 2 for x in analysis) / len(analysis))
                    stdev = max(stdev, 1e-6)
                    delta = max(analysis) - min(analysis)

                    if delta > (stdev * threshold) and (now - last_output_time > min_output_interval):
                        min_val = min(analysis)
                        max_val = max(analysis)
                        current = intervals[-1]
                        normalized = (current - min_val) / (max_val - min_val)
                        normalized = max(0.0, min(1.0, normalized))
                        client.send_message("/rnbo/inst/0/params/electrode/normalized", normalized)
                        print(f"Electrode interval: {current:.4f}s | Normalized: {normalized:.3f}")
                        last_output_time = now
        last_state = current_state

        # --- Seesaw Readings ---
        now = time.monotonic()
        if now - last_sensor_time >= 0.075:
            last_sensor_time = now
            try:
                moisture = seesaw.moisture_read()
                temperature = seesaw.get_temp()
                norm_moisture = moisture / 1023.0
                norm_temp = (temperature - 20) / 40.0
                client.send_message("/rnbo/inst/0/params/soil_moisture/normalized", norm_moisture)
                client.send_message("/rnbo/inst/0/params/temperature/normalized", norm_temp)
                print(f"Sent soil moisture: {norm_moisture:.3f}")
                print(f"Sent temperature: {norm_temp:.3f}")
            except OSError as e:
                print(f"I2C Read Error: {e}")

        # --- LDR Reading ---
        ldr_value = GPIO.input(LDR_PIN)
        ldr_normalized = float(ldr_value)
        client.send_message("/rnbo/inst/0/params/ldr/normalized", ldr_normalized)
        print(f"LDR Value: {ldr_value}")


        # --- MIDI Handling ---
        for msg in midi_input.iter_pending():
            if msg.type == 'note_on':
                client.send_message("/rnbo/inst/0/params/midi/note_on", [msg.note, msg.velocity])
                print(f"MIDI Note On: {msg.note} Velocity: {msg.velocity}")
            elif msg.type == 'note_off':
                client.send_message("/rnbo/inst/0/params/midi/note_off", [msg.note])
                print(f"MIDI Note Off: {msg.note}")

        # --- Encoder Rotation ---
        clk_state = GPIO.input(ENC_A)
        if clk_state != last_clk_state:
            if GPIO.input(ENC_B) != clk_state:
                encoder_position += 1
            else:
                encoder_position -= 1

            # Wrap between 1 and 8
            if encoder_position > max_position:
                encoder_position = min_position
            elif encoder_position < min_position:
                encoder_position = max_position

            client.send_message("/rnbo/inst/0/params/sample/normalized", encoder_position)
            print(f"Encoder sample index: {encoder_position}")

        last_clk_state = clk_state

        # --- Encoder Button ---
        button_state = GPIO.input(ENC_SW)
        if button_state != last_button_state:
            if button_state == GPIO.LOW:
                client.send_message("/rnbo/inst/0/params/encoder_button", 1)
                print("Encoder button pressed")
            else:
                client.send_message("/rnbo/inst/0/params/encoder_button", 0)
                print("Encoder button released")
            last_button_state = button_state

        time.sleep(0.001)

except KeyboardInterrupt:
 print("\nExiting cleanly...")
    GPIO.cleanup()
