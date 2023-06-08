#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <analogWrite.h>
#include <Adafruit_NeoPixel.h>
#include <LiquidCrystal_I2C.h>
#include <ESP32Tone.h>
#include "xht11.h"
#include <map>
#include <functional>

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);


class Property {
public:
  std::function<void(String)> setter;
  std::function<String(void)> getter;

  Property(std::function<void(String)> set, std::function<String(void)> get)
    : setter(set), getter(get) {}

  Property(std::function<String(void)> get)
    : setter(nullptr), getter(get) {}

  Property() : setter(nullptr), getter(nullptr) {}
};


class Device {
public:
  String macAddress;
  std::map<String, Property> properties;  
  
  Device() {
    macAddress = WiFi.macAddress(); // Every device has a MAC Address (for now)
  }

  void registerProperty(String name, std::function<void(String)> setter, std::function<String(void)> getter) {
    properties[name] = Property(setter, getter);
  }

  void registerCommand(String command, std::function<void(const char*)> callback) {
    commandCallbacks[command] = callback;
  }

  void callCommand(String command, const char* payload) {
    if (commandCallbacks.count(command) > 0) {
      commandCallbacks[command](payload);
    } else {
      Serial.println("Error: Command not found");
    }
  }

  void setProperty(String name, String value) {
    if (properties.count(name) > 0) {
      if (properties[name].setter)
        properties[name].setter(value);
      else
        Serial.println("Error: property does not support setting");
    } else {
      Serial.println("Error: property not found");
    }
  }

  String getProperty(String name) {
    if (properties.count(name) > 0) {
      if (properties[name].getter)
        return properties[name].getter();
      else
        Serial.println("Error: property does not support getting");
    } else {
      Serial.println("Error: property not found");
    }
    return String();
  }
  
  void handleCommand(const char* command, const char* payload) {
    if (commandCallbacks.count(command) > 0) {
      commandCallbacks[command](payload);
    } else {
      Serial.println("Error: command not found");
    }
  }

  String getMacAddress() {
    // return the MAC address in string format
    return macAddress;
  }

private:
  std::map<String, std::function<void(const char*)>> commandCallbacks;
};


String removeSpecialChars(String str) {
  String sanitizedStr = "";
  for (int i = 0; i < str.length(); i++) {
    char c = str.charAt(i);
    if (isAlphaNumeric(c) || c == '.' || c == '-') {
      sanitizedStr += c;
    }
  }
  return sanitizedStr;
}

class XHT11Sensor {
private:
  xht11 xht;
  unsigned char dht[4] = {0, 0, 0, 0}; // Only the first 32 bits of data are received, not the parity bits
  float temperature;
  float humidity;
  unsigned long timestamp;

public:
  XHT11Sensor(int pin) : temperature(0), humidity(0), timestamp(0), xht(pin) {}

  void readData() {
    if (xht.receive(dht)) {
      temperature = dht[2];
      humidity = dht[3];
    }
    timestamp = millis();
  }

  float getTemperature() const {
    return temperature;
  }

  float getHumidity() const {
    return humidity;
  }

  unsigned long getTimestamp() const {
    return timestamp;
  }

};


//LCD Manager class
class LCDManager {
  private:
    LiquidCrystal_I2C lcd;  // LCD object

  public:
    LCDManager(uint8_t lcd_addr, uint8_t lcd_cols, uint8_t lcd_rows) : lcd(lcd_addr, lcd_cols, lcd_rows) {
      lcd.init();
      lcd.begin(lcd_cols, lcd_rows);
      lcd.backlight();
    }

    void clear() {
      lcd.clear();
    }

    void setText(uint8_t line, uint8_t pos, String text) {
      lcd.setCursor(pos, line);
      lcd.print(text);
    }
};

class LEDManager {
private:
  int pin;
  bool isOn;  // Variable to track the LED state

public:
  LEDManager(int ledPin) : pin(ledPin), isOn(false) {
    pinMode(pin, OUTPUT);
  }

  void turnOn() {
    digitalWrite(pin, HIGH);
    isOn = true;
  }

  void turnOff() {
    digitalWrite(pin, LOW);
    isOn = false;
  }

  bool getState() const {
    return isOn;
  }

  void setState(bool state) {
    if (state) {
      turnOn();
    } else {
      turnOff();
    }
  }

  String getStringState() const {
    return isOn ? "1" : "0";
  }

  void setStringState(String state) {
    if (state == "1") {
      setState(true);
    } else if (state == "0") {
      setState(false);
    } else {
      Serial.println("Error: Invalid value for ledState");
    }
  }

};

class FanManager {
private:
  int pin1;
  int pin2;
  bool isRunning;  // Variable to track the fan state

public:
  FanManager(int fanPin1, int fanPin2) : pin1(fanPin1), pin2(fanPin2), isRunning(false) {
    pinMode(pin1, OUTPUT);
    pinMode(pin2, OUTPUT);
  }

  void startFan() {
    digitalWrite(pin1, HIGH);
    digitalWrite(pin2, LOW);
    isRunning = true;
  }

  void stopFan() {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);
    isRunning = false;
  }

  bool getState() const {
    return isRunning;
  }

  void setState(bool state) {
    if (state) {
      startFan();
    } else {
      stopFan();
    }
  }

  String getStringState() const {
    return isRunning ? "1" : "0";
  }

  void setStringState(String state) {
    if (state == "1") {
      setState(true);
    } else if (state == "0") {
      setState(false);
    } else {
      Serial.println("Error: Invalid value for fanState");
    }
  }
};

class BuzzerManager {
private:
  int pin;

public:
  BuzzerManager(int buzzerPin) : pin(buzzerPin) {
    Serial.print("buzzerPin:");
    Serial.println(pin);

    pinMode(pin, OUTPUT);
  }

  void tonePlay(int frequency, int duration) {
    tone(pin, frequency, duration, 0);
    //delay(duration + 50); // The 50 is the pause between notes
  }

  void toneStop() {
    noTone(pin);
  }

  void buzzer(const char* payload) {
    Serial.println("buzzer start");
    tonePlay(500, 1000);
    Serial.println("buzzer end");
    toneStop();
  }

  void birthday(const char* payload) {
    Serial.println("birthday start");

    tonePlay(294, 250);
    tonePlay(440, 250);
    tonePlay(392, 250);
    tonePlay(532, 250);
    tonePlay(494, 250);
    tonePlay(392, 250);
    tonePlay(440, 250);
    tonePlay(392, 250);
    tonePlay(587, 250);
    tonePlay(532, 250);
    tonePlay(392, 250);
    tonePlay(784, 250);
    tonePlay(659, 250);
    tonePlay(532, 250);
    tonePlay(494, 250);
    tonePlay(440, 250);
    tonePlay(698, 250);
    tonePlay(659, 250);
    tonePlay(532, 250);
    tonePlay(587, 250);
    tonePlay(532, 500);

    toneStop();

    Serial.println("birthday end");
  }
};


#define fanPin1 19
#define fanPin2 18
#define led_y 12  //Define the yellow led pin to 12
#define buzzer_pin 25

class SmartHouse : public Device {
public:
    XHT11Sensor xht11Sensor;
    LCDManager lcdManager;
    LEDManager ledManager;
    FanManager fanManager;
    BuzzerManager buzzerManager;

    SmartHouse() : xht11Sensor(17), 
                   lcdManager(0x27, 16, 2), 
                   ledManager(led_y), 
                   fanManager(fanPin1, fanPin2), 
                   buzzerManager(buzzer_pin) 
    {
        registerProperty("serialNumber", nullptr, [this]{ return String(this->getMacAddress()); });
        registerProperty("macAddress", nullptr, [this]{ return String(this->getMacAddress()); });
        registerProperty("temperature", nullptr, [this]{ return String(this->xht11Sensor.getTemperature()); });
        registerProperty("humidity", nullptr, [this]{ return String(this->xht11Sensor.getHumidity()); });                
        registerProperty("led", 
                        [this](String value){ ledManager.setStringState(value); },
                        [this]{ return String(ledManager.getState()); });        
        registerProperty("fan",
                        [this](String value) { fanManager.setStringState(value); },
                        [this]{ return String(fanManager.getState()); });        
        
        // registerProperty("buzzer",
        //              [this](String value) { buzzerManager.setStringState(value); },
        //              [this]() { return String(buzzerManager.getState()); });                                        

        registerCommand("birthday", [this](const char* payload) {
            buzzerManager.birthday(payload);
        });

        registerCommand("buzzer", [this](const char* payload) {
            buzzerManager.buzzer(payload);
        });

    }

    void addProperty(String property, Property p) {
      properties.emplace(property, p);
    }

    void displayIPandMQTT(IPAddress localIP, String mqttServer) {
        Serial.print("Local IP:");
        Serial.println(localIP);
        Serial.print("MQTT Broker: [");
        Serial.print(mqttServer);
        Serial.println("]");

        lcdManager.clear();
        lcdManager.setText(0, 0, "IP: " + localIP.toString());
        lcdManager.setText(1, 0, "MQTT: " + mqttServer);
    }

};

SmartHouse smarthouse;

// MQTT client
char *mqttServer = "10.0.0.4";
int mqttPort = 1883;

const char *SSID = "NETGEAR95";
const char *PWD = "heavymango777";
long last_time = 0;
char data[50];

// MQTT Handling
typedef void (*MqttCallback)(const char* topic, const char* payload);

// Define a structure to hold the topic and its corresponding callback function
struct TopicCallback {
  const char* topic;
  MqttCallback callback;
};

void handleXHT11(const char* topic, const char* payload) {  
  smarthouse.xht11Sensor.readData();

  // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  // Populate the JSON document
  doc["macAddress"] = smarthouse.getMacAddress();
  doc["temperature"] = smarthouse.xht11Sensor.getTemperature();
  doc["humidity"] = smarthouse.xht11Sensor.getHumidity();
  doc["timestamp"] = smarthouse.xht11Sensor.getTimestamp();

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/xht11", response.c_str());
}

void handleLedOn(const char* topic, const char* payload) {
  // Turn on the LED
  smarthouse.setProperty("led", "1");

  // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  // Populate the JSON document
  doc["macAddress"] = smarthouse.getMacAddress();
  doc["led"] = smarthouse.ledManager.getStringState();  

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/led/report", response.c_str());
}

void handleLedOff(const char* topic, const char* payload) {
  // Turn off the LED
  smarthouse.setProperty("led", "0");

    // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  // Populate the JSON document
  doc["macAddress"] = smarthouse.getMacAddress();
  doc["led"] = smarthouse.ledManager.getStringState();  

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/led/report", response.c_str());
}

void handleFanOn(const char* topic, const char* payload) {
  // Turn on the fan
  smarthouse.setProperty("fan", "1");

  // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  // Populate the JSON document
  doc["macAddress"] = smarthouse.getMacAddress();
  doc["fan"] = smarthouse.fanManager.getStringState();

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/fan/report", response.c_str());
}

void handleFanOff(const char* topic, const char* payload) {
  // Turn off the fan
  smarthouse.setProperty("fan", "0");

  // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  doc["fan"] = smarthouse.fanManager.getStringState();

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/fan/report", response.c_str());
}

void handlePlayBirthday(const char* topic, const char* payload) {
  // Turn off the fan
  //smarthouse.callCommand("birthday", payload);
  smarthouse.buzzerManager.birthday(payload);

  // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  // Populate the JSON document
  doc["macAddress"] = smarthouse.getMacAddress();
  doc["birthday"] = true;

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/birthday/ack", response.c_str());
}

void handleBuzzer(const char* topic, const char* payload) {
  // Turn off the fan
  //smarthouse.callCommand("buzzer", payload);
  smarthouse.buzzerManager.buzzer(payload);

  // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  // Populate the JSON document
  doc["buzzer"] = true;

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/buzzer/ack", response.c_str());
}


// Create a mapping of topics to callback functions
TopicCallback topicCallbacks[] = {
  {"/swa/commands/xht11", handleXHT11},
  {"/swa/commands/led/on", handleLedOn },
  {"/swa/commands/led/off", handleLedOff },
  {"/swa/commands/fan/on", handleFanOn },
  {"/swa/commands/fan/off", handleFanOff },
  {"/swa/commands/birthday", handlePlayBirthday },
  {"/swa/commands/buzzer", handleBuzzer }
};

const int numTopicCallbacks = sizeof(topicCallbacks) / sizeof(topicCallbacks[0]);

void callback(char* topic, byte* payload, unsigned int length) {
  
  Serial.print("Callback - Topic: ");
  Serial.println(topic);

  Serial.print("Callback - Message: ");

  // Convert the payload bytes to a string
  char payloadStr[length + 1];
  memcpy(payloadStr, payload, length);
  payloadStr[length] = '\0';

  Serial.println(payloadStr);

  // Find the corresponding callback function for the topic
  for (int i = 0; i < numTopicCallbacks; i++) {
    if (strcmp(topicCallbacks[i].topic, topic) == 0) {
      // Call the callback function with the topic and payload
      topicCallbacks[i].callback(topic, payloadStr);
      break;
    }
  }
}

void connectToWiFi() {
  Serial.println("Connecting to WIFI");
 
  WiFi.begin(SSID, PWD);
  Serial.println(SSID);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }  
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(SSID);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());      
}

void setupMQTT() {
  mqttClient.setServer(mqttServer, mqttPort);
  // set the callback function
  mqttClient.setCallback(callback);
}

long lastReconnectAttempt = 0;


void setup() {
  Serial.begin(115200);
  
  connectToWiFi();
  setupMQTT();
  Serial.println(ESP.getFreeHeap());
  lastReconnectAttempt = 0;
}

void reconnect() {
  
  Serial.println("Connecting to MQTT Broker...");
  
  while (!mqttClient.connected()) {
      Serial.println("Reconnecting to MQTT Broker..");
      
      String clientId = "ESP32Client-" + smarthouse.getProperty("serialNumber");
      clientId += String(random(0xffff), HEX);
      
      if (mqttClient.connect(clientId.c_str())) {
        Serial.println("Connected.");
        // subscribe to topic
        mqttClient.subscribe("/swa/commands/#");
      }      
  }

  smarthouse.displayIPandMQTT(WiFi.localIP(), String(mqttServer));
}

void loop() {
  unsigned long timestamp = millis();
  //Serial.print("loop()");
  //Serial.println(timestamp);

  if (!mqttClient.connected()) {
    reconnect();    
  }  
  mqttClient.loop();  
  //delay(5000); // Wait for 1 second before looping again
}


// void loop() {
//   unsigned long timestamp = millis();
//   Serial.print("loop()");
//   Serial.println(timestamp);

//   if (!mqttClient.connected()) {
//     long now = millis();
//     if (now - lastReconnectAttempt > 5000) {
//       lastReconnectAttempt = now;
//       // Attempt to reconnect
//       if (reconnect()) {
//         lastReconnectAttempt = 0;
//       }
//     }
//   } else {
//     // Client connected

//     mqttClient.loop();
//   }

// }

