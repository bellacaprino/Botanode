# Botanode
Biodata sonification using teensy and max!

My instrument will most likely be called Botanode!

Botanode is a biodata sonification device inspired by [this breadboard kit by Electricity for Progress (Sam Cusumano)](https://github.com/electricityforprogress/BiodataSonificationBreadboardKit/blob/master/Arduino%20Shield%20Biodata%20Sonification%20-%20Parts.csv)

With Botanode, two electrodes will be attached to the leaves of a plant. They will both measure electrical signal coming from the plant. By placing electrodes on a plant's surface, I can measure its small voltage changes. These fluctuations represent the plant’s response to environmental factors or physical touch 

To implement this, I will start by setting up a circuit that includes electrodes connected through a 3.5mm jack, an operational amplifier (op-amp) for signal amplification, and the Teensy to read the signals and convert them to musical output. I plan to use an LM358 or TL072 op-amp to amplify the small signals from the electrodes. The amplified signal will then be fed into one of the Teensy's analog inputs, where it will be processed for generating MIDI messages or audio synthesis. The Teensy will be programmed to convert the variations in voltage into musical parameters like pitch, volume, or modulation.


# Outcomes

## Good

No matter what I will find a way to use a plant as an instrument, with the performer performing by touching the plant. Perhaps I will use other elements like potentiometers and buttons to edit the sound. I will process the data I receive through teensy, arduino, and max to create an instrument that allows nature to be a part of the music making process :)

## Better

I will create a circuit that will measure and amplify signals from a plant, create a teensy program that reads the signals, and process it all through Max. The instrument will be playable through touch, through the responsivness of the plant or through a hall effect or ultrasonic sensor, but it will largely be able to generate music on its own. I'll also add LEDs for a visual componant.


## Best!
The plant will be the sole controller. The instrument will be playable through touch through some kind of sensor (possibly piezoelectric) on the leaves to measure when they are touched. Different leaves will trigger different pitches, FX. The plant will generate changes based on its own biorhythms. Design a cute box to store it in. I'll possibly integrate multiple plants to have a whole singing garden :-)

# Next Steps

To get started, I’ll experiment with actual electrodes to measure the signals from the plant. I’ll use a multimeter to check whether the signals are unipolar or bipolar, which is crucial for my circuit design. If the signals are bipolar, I’ll need to apply an offset or rectify them to ensure the Teensy can read them properly, as it can’t process negative voltages. I will also identify the voltage range of the signals to determine how much amplification is needed, which will help me choose the right resistor values for the op-amp circuit.

Next, I’ll gather the necessary components, including the electrodes, a 3.5mm jack, an LM358 or TL072 op-amp, and the Teensy. I’ll build the initial circuit and test the electrode setup with a multimeter to ensure I’m getting accurate readings. I’ll also research how to use operational amplifiers effectively.

Additionally, I’ll look into using a piezo sensor to detect physical contact with the plant. This will allow me to capture the plant's response to touch. I’m also interested in exploring the use of a magnetometer for continuous signal monitoring of the plant’s environment, which could add another layer of interaction.

Bottom line I'm super excited to start!!!!




