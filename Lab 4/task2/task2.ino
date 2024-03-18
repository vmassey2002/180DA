#include <SPI.h>
#include <WiFiNINA.h>

char networkSSID[] = "";
char networkPassword[] = "";

void setup() {
  SerialUSB.begin(9600);
  while (!Serial) {
    ;
  }

  if (WiFi.status() == WL_NO_MODULE) {
    SerialUSB.println("Communication with WiFi module failed!");
    while (true);
  }

  int status = WiFi.begin(networkSSID, networkPassword);
  while (status != WL_CONNECTED) {
    SerialUSB.println(networkSSID);
    status = WiFi.begin(networkSSID, networkPassword);
    delay(10000);
  }

  SerialUSB.print("You're connected to the network");
  printCurrentNetwork();
  printWiFiData();
}

void loop() {
  // Nothing to do
}

void printWiFiData() {
  IPAddress ipAddress = WiFi.localIP();
  SerialUSB.print("IP Address: ");
  SerialUSB.println(ipAddress);
  SerialUSB.println(ipAddress);

  byte macAddress[6];
  WiFi.macAddress(macAddress);
  SerialUSB.print("MAC address: ");
  printMacAddress(macAddress);
}

void printCurrentNetwork() {
  SerialUSB.print("SSID: ");
  SerialUSB.println(WiFi.SSID());

  byte bssid[6];
  WiFi.BSSID(bssid);
  SerialUSB.print("BSSID: ");
  printMacAddress(bssid);

  long signalStrength = WiFi.RSSI();
  SerialUSB.print("Signal strength (RSSI): ");
  SerialUSB.println(signalStrength);

  byte encryptionType = WiFi.encryptionType();
  SerialUSB.print("Encryption Type: ");
  SerialUSB.println(encryptionType, HEX);
  SerialUSB.println();
}

void printMacAddress(byte mac[]) {
  for (int i = 5; i >= 0; i--) {
    if (mac[i] < 16) {
      SerialUSB.print("0");
    }
    SerialUSB.print(mac[i], HEX);
    if (i > 0) {
      SerialUSB.print(":");
    }
  }
  SerialUSB.println();
}
