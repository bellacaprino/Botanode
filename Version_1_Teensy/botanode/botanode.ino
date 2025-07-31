const int e11 = 1; // Electrode pair 1, pin 1
const int e12 = 2; // Electrode pair 1, pin 2
const int e21 = 3; // Electrode pair 2, pin 1
const int e22 = 4; // Electrode pair 2, pin 2

const int numSamples = 100; // Number of samples for the moving average and standard deviation
const int printInterval = 50; // Calculate and print results once every 50 samples

int diffSamples1[numSamples] = {0}; // Array for electrode pair 1 differences
int diffSamples2[numSamples] = {0}; // Array for electrode pair 2 differences
int sampleIndex = 0; // Index for the circular buffer
int sampleCounter = 0; // Counter to track how many samples have been read

// LED PWM pins
const int led1Green = 5;
const int led1Blue = 6;
const int led2Green = 9;
const int led2Blue = 10;

void setup() {
  Serial.begin(9600);
  pinMode(e11, INPUT);
  pinMode(e12, INPUT);
  pinMode(e21, INPUT);
  pinMode(e22, INPUT);

  // Set LED pins as outputs
  pinMode(led1Green, OUTPUT);
  pinMode(led1Blue, OUTPUT);
  pinMode(led2Green, OUTPUT);
  pinMode(led2Blue, OUTPUT);
}

void loop() {
  int e11Reading = analogRead(e11);
  int e12Reading = analogRead(e12);
  int e21Reading = analogRead(e21);
  int e22Reading = analogRead(e22);

  // Calculate the differences for both electrode pairs
  int diff1 = e11Reading - e12Reading;
  int diff2 = e21Reading - e22Reading;

  // Store the differences in their respective arrays
  diffSamples1[sampleIndex] = diff1;
  diffSamples2[sampleIndex] = diff2;

  // Increment sampleIndex and wrap it around using modulo
  sampleIndex = (sampleIndex + 1) % numSamples;

  // Increment sample counter
  sampleCounter++;

  // Calculate and print results only at the specified interval
  if (sampleCounter >= printInterval) {
    // Reset the counter
    sampleCounter = 0;

    // Calculate the moving average and standard deviation for both pairs
    float diffAvg1 = movingAverage(diffSamples1, numSamples);
    float diffStdDev1 = movingStandardDeviation(diffSamples1, numSamples, diffAvg1);

    float diffAvg2 = movingAverage(diffSamples2, numSamples);
    float diffStdDev2 = movingStandardDeviation(diffSamples2, numSamples, diffAvg2);

    // Map the standard deviations to PWM values for dramatic changes
    int brightness1 = constrain(map(diffStdDev1, 0, 100, 0, 255), 0, 255); // Full range
    int brightness2 = constrain(map(diffStdDev2, 0, 100, 0, 255), 0, 255); // Full range

    // Control LED brightness with more green and less blue
    analogWrite(led1Green, brightness1);     // Strong green
    analogWrite(led1Blue, brightness1 / 4); // Subtle blue
    analogWrite(led2Green, brightness2);     // Strong green
    analogWrite(led2Blue, brightness2 / 4); // Subtle blue

    // Print results as a single line of numbers separated by spaces
    Serial.print(diffStdDev1); // Electrode pair 1 standard deviation
    Serial.print(" ");
    Serial.println(diffStdDev2); // Electrode pair 2 standard deviation
  }

  delay(1); // Adjust sampling frequency
}

// Function to calculate the moving average of an array
float movingAverage(int samples[], int size) {
  long sum = 0; // Use long to avoid overflow for large sums
  for (int i = 0; i < size; i++) {
    sum += samples[i];
  }
  return (float)sum / size;
}

// Function to calculate the moving standard deviation of an array
float movingStandardDeviation(int samples[], int size, float mean) {
  float sumSquaredDifferences = 0.0;
  for (int i = 0; i < size; i++) {
    float diff = samples[i] - mean;
    sumSquaredDifferences += diff * diff;
  }
  return sqrt(sumSquaredDifferences / size);
}
