#include <WiFiClientSecure.h>

const char* ssid = "NETGEAR33";
const char* wifipassword = "fancyzoo762";

WiFiClientSecure wifi;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(115200);
    Serial.print("Connecting to SSID: ");
    Serial.println(ssid);

    WiFi.begin(ssid, wifipassword);

    while( WiFi.status() != WL_CONNECTED ) {
        Serial.print(".");
        delay(1000);
    }

    Serial.print("Connected to ");
    Serial.println(ssid);
}

void loop() {
  // put your main code here, to run repeatedly:
    Serial.print(":");
    delay(1000);
}
