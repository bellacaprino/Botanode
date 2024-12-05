

---

# **Getting Started with Botanode**

Here’s everything you need to set up and start playing Botanode!

---

## **What You’ll Need**

### **Software**
- **Arduino IDE**  
  Grab it here: [Arduino IDE](https://www.arduino.cc/en/software). Install it like any other program.
- **Max MSP**  
  Download from [Max MSP](https://cycling74.com/downloads). Make sure it’s installed and working. You’ll be using the **Serial** object to connect.

---

## **Hardware**
- 1 x Arduino or Teensy microcontroller  
- 2 x RGB LEDs (common cathode, no resistors needed)  
- 2 x Electrode jacks (3-pin: tip, sleeve, ground)  
- Jumper wires  
- A USB cable for your board  

---

## **How to Set It Up**

### **Step 1: Wiring**
1. **Electrode Jacks**
   - Each jack has three pins:
     - **Tip** → Positive signal (e.g., pin `1` or `3`).
     - **Sleeve** → Negative signal (e.g., pin `2` or `4`).
     - **Ground** → Connect to GND on the Arduino.

2. **RGB LEDs**
   - LED 1 (Electrode Pair 1):
     - Green to **pin 5**.
     - Blue to **pin 6**.
     - Common cathode to **GND**.
   - LED 2 (Electrode Pair 2):
     - Green to **pin 9**.
     - Blue to **pin 10**.
     - Common cathode to **GND**.

---

### **Step 2: Uploading the Code**
1. Open the Arduino code (`YourSketch.ino`) in the Arduino IDE.
2. Plug in your Arduino or Teensy via USB.
3. Hit **Upload** to load the code. Done.

---

### **Step 3: Max MSP**
1. Open the Max patch file (`YourPatch.maxpat`).
2. Set up the **Serial** object to talk to your Arduino.
3. You’re ready to see the data in Max and start generating sounds.

---

## **How to Play**

1. **Connect the Electrodes**
   - Attach the electrodes to plants, conductive materials, or just touch them directly.
2. **Watch the LEDs**
   - LED 1 (Electrode Pair 1): More blue.
   - LED 2 (Electrode Pair 2): More green.
   - Brightness reacts to changes in the signals.
3. **Explore Sounds in Max**
   - Adjust and experiment with the patch to get different results.

---

## **Diagram**
For reference, check the wiring diagram:  
- [Diagram.fzz](./Diagram.fzz)  
- [Diagram.pdf](./Diagram.pdf)  
- [Diagram.jpg](./Diagram.jpg)  

---


---

That’s it! Have fun creating music with your new instrument. 🌱✨
