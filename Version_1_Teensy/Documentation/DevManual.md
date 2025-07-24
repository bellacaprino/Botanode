### DeveloperManual.md

---

# **Botanode Developer Manual**

## **Bill of Materials**

| **Item**          | **Description**                | **Distributor**   | **Price (USD)** | **Quantity** |
|--------------------|--------------------------------|-------------------|-----------------|--------------|
| **Arduino Uno** OR **Teensy 4.1** | Microcontroller – choose one depending on your needs | Arduino.cc / PJRC | $25.00 / $29.25 | 1 |
| RGB LEDs           | Common cathode RGB LEDs       | Adafruit          | $2.50           | 2            |
| Electrode Jacks    | 3-pin (tip/sleeve/ground)     | SparkFun          | $3.95           | 2            |
| Jumper Wires       | Male-to-male & male-to-female | Amazon            | $5.00           | 20           |
| USB Cable          | Micro-USB (Teensy) or USB-B (Uno) cable | Any Electronics | $4.00           | 1            |


---

## **Implementation Details**

### **1. Gestures Captured**
Botanode interprets subtle interactions and environmental changes into data:
- **Touch Gestures:**
  - Touching or holding electrodes alters the signal based on human conductivity and proximity.
- **Environmental Fluctuations:**
  - Plants respond to changes in light, humidity, air currents, and vibration, all of which are reflected in the signals.
- **Proximity Effects:**
  - The electrodes also pick up ambient electromagnetic fields, with plants acting as antennas rather than pure signal sources.

---

### **2. Sensors Considered**
#### **Options Explored:**
1. **Electrodes (Chosen):**
   - **Why Chosen:**
     - Electrodes align with the biological aspect of the project, capable of detecting small electrical signals from the plant.
     - They offer the potential to capture the plant’s natural activity, even if overshadowed by environmental noise.
   - **Limitations:**
     - Plant-generated signals are very small and often lost in ambient electrical noise.
     - Without an op-amp for signal amplification, the plant’s natural signals are hard to isolate.

2. **Hall Effect Sensors:**
   - **Advantages:**
     - Sensitive to magnetic field changes, making them great for proximity detection.
   - **Why Not Chosen:**
     - Less relevant to biological signals or the concept of interacting with plants directly.

3. **Makey Makey Board:**
   - **Advantages:**
     - Extremely beginner-friendly and versatile.
   - **Why Not Chosen:**
     - Limited ability to process raw electrical signals; designed more for straightforward digital inputs.

---

### **3. Data Processing and Interpolation**

#### **Why Process the Data?**
Raw signals from the electrodes are noisy, inconsistent, and difficult to interpret directly. Processing ensures stable and meaningful outputs for sound synthesis and LED visualization.

#### **Steps in Data Processing:**
1. **Signal Difference Calculation:**
   - Read the voltage difference between the tip and sleeve of each electrode jack.
   - This isolates changes caused by touch, environment, or proximity effects.

2. **Smoothing with Moving Averages:**
   - Averages out signal fluctuations over time, reducing noise and stabilizing outputs.

3. **Standard Deviation Calculation:**
   - Measures the variability of the signal over a window of samples, mapping it to changes in brightness or sound.

4. **Mapping to Outputs:**
   - Data is linearly mapped to control LED brightness and sound synthesis, ensuring smooth, predictable interactions.

---

### **4. Successes and Challenges**

#### **Successes:**
- **Gestural Interaction:**  
  Touching or moving near the electrodes creates clear, dynamic changes in the output.
- **Real-Time Feedback:**  
  The LEDs and Max MSP patch respond effectively to signal fluctuations.
- **Intuitive Design:**  
  Electrode-based interaction feels natural and aligns with the biological focus of the project.

#### **Challenges:**
- **Small Signals from Plants:**
  - The plant’s electrical signals are very faint and often overwhelmed by environmental noise.
  - Without amplification (e.g., using an op-amp), isolating the plant’s activity was not feasible in this iteration.
- **Data Processing Issues:**
  - Observing meaningful signal changes was difficult without standard deviation-based calculations, as raw data was too erratic.

---

### **5. Future Plans**

#### **Hardware Improvements:**
1. **Signal Amplification:**
   - Incorporate an op-amp to amplify the plant’s natural signals, making them more detectable and meaningful.
2. **Multiple Electrode Pairs:**
   - Add more electrode pairs for richer, multi-layered soundscapes.

#### **Software Enhancements:**
1. **Advanced Filtering:**
   - Use digital filters (e.g., low-pass, high-pass) to isolate meaningful signal changes and remove noise.
2. **Dynamic Color Mapping:**
   - Expand LED output to reflect frequency or amplitude shifts dynamically.

#### **Features to Explore:**
1. **MIDI Output:**
   - Use the processed signals to control external MIDI devices or software instruments.
2. **Standalone Functionality:**
   - Add onboard sound generation for a fully self-contained instrument.
