// the Matrix indexes:
// [11 12 21 22]
// [13 14 23 24]
// [31 32 41 42]
// [33 34 43 44]

void setup() {
  // Begin serial communication
  Serial.begin(9600);
}

void loop() {
  for (int pin = A0; pin <= A15; pin++) {
    // Read the value from the pin
    int sensorValue = analogRead(pin);
    Serial.println(sensorValue);
  }
  
  // separator for easier parsing
  Serial.println("---");

  // delay for each data message
  delay(100);
}
