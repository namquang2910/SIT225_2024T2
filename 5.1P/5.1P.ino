#include <Arduino_LSM6DS3.h>

float x, y, z;

void setup() {
  Serial.begin(9600); // set baud rate
  while (!Serial);  // wait for port to init
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  // read accelero data
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);
  }
  String data = "{\"x\":" + String(x, 4) + ",\"y\":" + String(y, 4) + ",\"z\":" + String(z, 4) + "}";
  Serial.println(data);
  delay(100);
}