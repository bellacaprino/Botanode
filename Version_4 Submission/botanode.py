import time
import math
import board
import busio
import mido
import RPi.GPIO as GPIO
from collections import deque
from gpiozero import RotaryEncoder, Button
from adafruit_seesaw.seesaw import Seesaw
from pythonosc import udp_client
import threading
import statistics

# ----------------------------
# OSC Setup
# ----------------------------
ip = "127.0.0.1"
port = 1234
client = udp_client.SimpleUDPClient(ip, port)

# ----------------------------
# GPIO Mode
# ----------------------------
GPIO.setmode(GPIO.BCM)

# ----------------------------
# Seesaw Sensor Setup (I2C)
# ----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
seesaw = Seesaw(i2c, addr=0x36)

# ----------------------------
# Electrode Sensor
# ----------------------------
ELECTRODE_PIN = 17
GPIO.setup(ELECTRODE_PIN, GPIO.IN)

# ----------------------------
# LDR Sensor Setup
# ----------------------------
LDR_PIN = 4
GPIO.setup(LDR_PIN, GPIO.IN)
LDR_MIN = 4000
LDR_MAX = 5496227
LDR_SCALE_FACTOR = 1.5

def rc_time(pin):
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
    return count

# ----------------------------
# Rotary Encoder Setup
# ----------------------------
encoder = RotaryEncoder(a=16, b=20, wrap=True, max_steps=16)
encoder_button = Button(21)
last_rotary_value = 0

# ----------------------------
# Pushbuttons Setup (with internal pull-up)
# ----------------------------
button_pins = [19, 21, 20]
last_button_states = [1, 1, 1]
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ----------------------------
# MIDI Setup
# ----------------------------
midi_input = mido.open_input()

# ----------------------------
# Threaded Functions
# ----------------------------
def encoder_loop():
    global last_rotary_value
    while True:
        val = encoder.steps
        wrapped_val = (val % 8) + 1
        normalized = wrapped_val / 10.0
        if val != last_rotary_value:
            print(f"Encoder: {wrapped_val} -> {normalized:.1f}")
            client.send_message("/rnbo/inst/0/params/encoder_value", normalized)
            last_rotary_value = val

        client.send_message("/rnbo/inst/0/params/encoder_button", 1 if encoder_button.is_pressed else 0)
        time.sleep(0.1)

def buttons_loop():
    global last_button_states
    while True:
        for i, pin in enumerate(button_pins):
            current_state = GPIO.input(pin)
            if current_state != last_button_states[i]:
                client.send_message(f"/rnbo/inst/0/params/button_{i+1}", current_state)
                print(f"Button {i+1} (GPIO {pin}) changed to {current_state}")
                last_button_states[i] = current_state
        time.sleep(0.01)

def pulse_detection_loop():
    SAMPLE_DURATION = 0.12  # 100ms
    SAMPLE_RATE = 0.001    # 1ms
    PIN = ELECTRODE_PIN

    while True:
        try:
            readings = []
            start_time = time.monotonic()

            while time.monotonic() - start_time < SAMPLE_DURATION:
                val = GPIO.input(PIN)
                readings.append(val)
                time.sleep(SAMPLE_RATE)

            if len(set(readings)) == 1:
                activity = 0.0
            else:
                activity = statistics.stdev(readings)

            boosted = activity ** 2 * 10
            boosted = max(0.0, min(boosted, 1.0))

            client.send_message("/rnbo/inst/0/params/electrode/normalized", boosted)
            print(f"Electrode activity: {boosted:.3f}")

        except Exception as e:
            print(f"Electrode Error: {e}")
            time.sleep(0.1)

def sensor_loop():
    global LDR_MIN, LDR_MAX
    last_sensor_time = time.monotonic()

    while True:
        try:
            raw_ldr = rc_time(LDR_PIN)
            LDR_MIN = min(LDR_MIN, raw_ldr)
            LDR_MAX = max(LDR_MAX, raw_ldr)

            log_val = math.log(raw_ldr + 1)
            log_min = math.log(LDR_MIN + 1)
            log_max = math.log(LDR_MAX + 1)
            norm_ldr = min((log_val - log_min) / (log_max - log_min) * LDR_SCALE_FACTOR, 1.0)

            client.send_message("/rnbo/inst/0/params/ldr/normalized", norm_ldr)
            print(f"LDR: {raw_ldr} -> {norm_ldr:.3f}")

            now = time.monotonic()
            if now - last_sensor_time > 0.075:
                last_sensor_time = now
                moisture = seesaw.moisture_read()
                temp = seesaw.get_temp()
                norm_moisture = moisture / 1023.0
                norm_temp = (temp - 20) / 40.0
                client.send_message("/rnbo/inst/0/params/soil_moisture/normalized", norm_moisture)
                client.send_message("/rnbo/inst/0/params/temperature/normalized", norm_temp)
                print(f"Soil: {norm_moisture:.3f}, Temp: {norm_temp:.3f}")

            time.sleep(0.001)

        except Exception as e:
            print(f"Sensor Error: {e}")
            time.sleep(0.1)

def midi_loop():
    while True:
        for msg in midi_input.iter_pending():
            if msg.type == 'note_on':
                client.send_message("/rnbo/inst/0/params/midi/note_on", [msg.note, msg.velocity])
                print(f"MIDI Note On: {msg.note}, Velocity: {msg.velocity}")
            elif msg.type == 'note_off':
                client.send_message("/rnbo/inst/0/params/midi/note_off", [msg.note])
                print(f"MIDI Note Off: {msg.note}")
        time.sleep(0.01)

# ----------------------------
# Start Threads
# ----------------------------
threading.Thread(target=encoder_loop, daemon=True).start()
threading.Thread(target=buttons_loop, daemon=True).start()
threading.Thread(target=pulse_detection_loop, daemon=True).start()
threading.Thread(target=sensor_loop, daemon=True).start()

# Run MIDI on main thread
midi_loop()
