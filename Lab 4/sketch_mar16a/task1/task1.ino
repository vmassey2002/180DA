#include <Arduino_LSM6DS3.h>

#define  PRINT_INTERVAL 5000
void setup_accelerometer() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in g's");
  Serial.println("X\tY\tZ");
}

void read_and_print_acceleration() {
  float x, y, z;
  
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
  }
}

void setup() {
  setup_accelerometer();
}

void loop() {
  unsigned long startTime = millis();

  read_and_print_acceleration();

  unsigned long elapsedTime = millis() - startTime;

  if(elapsedTime < PRINT_INTERVAL){
    delay(PRINT_INTERVAL - elapsedTime);
  }
}
