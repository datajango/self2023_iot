#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>


// MQTT client
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 

char *mqttServer = "10.0.0.4";
int mqttPort = 1883;

const char *SSID = "NETGEAR95";
const char *PWD = "heavymango777";
long last_time = 0;
char data[50];

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Callback - ");
  Serial.println("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println("");
  sprintf(data, "{\"response\" : \"ACK\"}");
  mqttClient.publish("/swa/response", data);
}


void connectToWiFi() {
  Serial.println("Connecting to WIFI");
 
  WiFi.begin(SSID, PWD);
  Serial.println(SSID);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.print("Connected.");
  
}

void setupMQTT() {
  mqttClient.setServer(mqttServer, mqttPort);
  // set the callback function
  mqttClient.setCallback(callback);
}

void setup() {
  Serial.begin(115200);

  Serial.println("setup()");

  connectToWiFi();

  setupMQTT();
}

void reconnect() {
  Serial.println("Connecting to MQTT Broker...");
  while (!mqttClient.connected()) {
      Serial.println("Reconnecting to MQTT Broker..");
      String clientId = "ESP32Client-";
      clientId += String(random(0xffff), HEX);
      
      if (mqttClient.connect(clientId.c_str())) {
        Serial.println("Connected.");
        // subscribe to topic
        mqttClient.subscribe("/swa/commands");
      }
      
  }
}
void loop() {
  if (!mqttClient.connected())
    reconnect();
    mqttClient.loop();
    long now = millis();

    if (now - last_time > 60000) {
    // Send data
    float temp = 33.5;
    float hum = 45.68;
    float pres = 23 / 100;
    // Publishing data throgh MQTT
    sprintf(data, "%f", temp);
    //Serial.println(data);
    mqttClient.publish("/swa/temperature", data);
    sprintf(data, "%f", hum);
    //Serial.println(hum);
    mqttClient.publish("/swa/humidity", data);
    sprintf(data, "%f", pres);
    //Serial.println(pres);
    mqttClient.publish("/swa/pressure", data);
    last_time = now;
  }
}


