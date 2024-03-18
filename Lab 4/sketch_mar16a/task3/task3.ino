#include <Arduino.h>

#include <SPI.h>
#include <Wire.h>
#include <Arduino_LSM6DS3.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiNINA.h>

#define CONVERT_G_TO_MS2 9.80665f
#define FREQUENCY_HZ 104
#define INTERVAL_MS (1000 / (FREQUENCY_HZ + 1))

struct Acc_senseData {
  float acc_x = 0.0F;
  float acc_y = 0.0F;
  float acc_z = 0.0F;
};

struct Gyr_senseData {
  float gyr_x = 0.0F;
  float gyr_y = 0.0F;
  float gyr_z = 0.0F;
};

void setup_wifi();
void reconnect();

static char payload[256];
static Acc_senseData acc_data;
static Gyr_senseData gyr_data;
StaticJsonDocument<256> doc;

#define TOKEN ""
#define DEVICEID ""

const char* ssid = "Venicia";
const char* password = "SwaySway";
const char mqtt_server[] = "mqtt.eclipseprojects.io";
const char publishTopic[] = "ece180da-warmup/venicia/lab4/imu";

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!mqtt.connected()) {
    if (mqtt.connect(DEVICEID, TOKEN, NULL)) {
      Serial.println("Connected to MQTT broker");
      digitalWrite(LED_BUILTIN, HIGH);
    } else {
      Serial.print("failed to connect to MQTT broker, rc=");
      Serial.print(mqtt.state());
      Serial.println("try again in 5 seconds");
      digitalWrite(LED_BUILTIN, LOW);
      delay(5000);
    }
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  setup_wifi();
  mqtt.setServer(mqtt_server, 1883);
}

void loop() {
  unsigned long startTime = millis();
  if (!mqtt.connected()) {
    reconnect();
  }
  mqtt.loop();

  static unsigned long last_interval_ms = 0;
  float a_x, a_y, a_z;
  float g_x, g_y, g_z;

  if (millis() > last_interval_ms + INTERVAL_MS) {
    last_interval_ms = millis();

    IMU.readAcceleration(a_x, a_y, a_z);
    acc_data.acc_x = a_x;
    acc_data.acc_y = a_y;
    acc_data.acc_z = a_z;
    doc["ACC_X"] = acc_data.acc_x * CONVERT_G_TO_MS2;
    doc["ACC_Y"] = acc_data.acc_y * CONVERT_G_TO_MS2;
    doc["ACC_Z"] = acc_data.acc_z * CONVERT_G_TO_MS2;

    IMU.readGyroscope(g_x, g_y, g_z);
    gyr_data.gyr_x = g_x;
    gyr_data.gyr_y = g_y;
    gyr_data.gyr_z = g_z;
    doc["GYR_X"] = gyr_data.gyr_x;
    doc["GYR_Y"] = gyr_data.gyr_y;
    doc["GYR_Z"] = gyr_data.gyr_z;

    serializeJsonPretty(doc, payload);
    mqtt.publish(publishTopic, payload);
    Serial.println(payload);
  }

  unsigned long elapsedTime = millis() - startTime;
  if (elapsedTime < 1000) {
    delay(1000 - elapsedTime);
  }
}
