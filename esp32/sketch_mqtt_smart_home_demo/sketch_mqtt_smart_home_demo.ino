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

void publish(PubSubClient &mqttClient, const String &topic, DynamicJsonDocument &doc) {
  String payload;
  serializeJson(doc, payload);
  mqttClient.publish(topic.c_str(), payload.c_str());

  Serial.println(topic);
  Serial.println(payload);
}


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

  void update() {
    // Here you can call other update-like methods of other components.
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

class ButtonManager {
private:
  int btn1;
  int btn2;
  bool btn1State;
  bool btn2State;
  bool lastBtn1State;
  bool lastBtn2State;

public:
  ButtonManager(int button1Pin, int button2Pin) : 
    btn1(button1Pin), btn2(button2Pin), 
    btn1State(true), btn2State(true),
    lastBtn1State(true), lastBtn2State(true) 
  {
    pinMode(btn1, INPUT);
    pinMode(btn2, INPUT);
  }

  void updateButtonStates(PubSubClient &mqttClient, const String &topic) {
    bool currentBtn1State = digitalRead(btn1);
    bool currentBtn2State = digitalRead(btn2);
    
    if (currentBtn1State != lastBtn1State) {
      DynamicJsonDocument doc(1024);
      doc["button"] = "1";
      
      if (!currentBtn1State) { // Button was just pressed
        doc["action"] = "pressed";
      } else { // Button was just released
        doc["action"] = "released";
      }
      publish(mqttClient, topic, doc);

      lastBtn1State = currentBtn1State;
    }
    
    if (currentBtn2State != lastBtn2State) {
      DynamicJsonDocument doc(1024);
      doc["button"] = "2";

      if (!currentBtn2State) { // Button was just pressed
        doc["action"] = "pressed";
      } else { // Button was just released
        doc["action"] = "released";
      }
      publish(mqttClient, topic, doc);

      lastBtn2State = currentBtn2State;
    }

    btn1State = currentBtn1State;
    btn2State = currentBtn2State;
  }


  bool getButtonState(int buttonPin) const {
    if (buttonPin == btn1) {
      return btn1State;
    } else if (buttonPin == btn2) {
      return btn2State;
    } else {
      Serial.println("Error: Invalid button pin");
      return false;
    }
  }

  String getStringButtonState(int buttonPin) const {
    return getButtonState(buttonPin) ? "1" : "0";
  }
};


class PIRManager {
private:
  const int pirPin;
  bool lastState;

public:
  PIRManager(int pirPin) : pirPin(pirPin), lastState(false) {
    pinMode(pirPin, INPUT);
  }

  void update(PubSubClient &mqttClient, const String &topic) {
    bool currentState = digitalRead(pirPin);

    if (currentState != lastState) {
      DynamicJsonDocument doc(1024);
      doc["sensor"] = "pir";

      if (currentState) {
        doc["state"] = "occupancy";
      } else {
        doc["state"] = "vacancy";
      }

      publish(mqttClient, topic, doc);

      lastState = currentState;
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

  /*
  [
    { "note": 440, "duration": 500, "pause": 500 },
    { "note": 494, "duration": 500, "pause": 500 },
    { "note": 523, "duration": 500, "pause": 500 },
    { "note": 587, "duration": 500, "pause": 500 }
  ]
  */
  void play_notes(const char* payload) {
    const size_t capacity = JSON_ARRAY_SIZE(20) + 20*JSON_OBJECT_SIZE(3);
    DynamicJsonDocument doc(capacity);

    // Parse the input payload
    DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
    }

    JsonArray array = doc.as<JsonArray>();
    for(JsonVariant v : array) {
      JsonObject obj = v.as<JsonObject>();
      int note = obj["note"];
      int duration = obj["duration"];
      int pause = obj["pause"];

      tonePlay(note, duration);
      delay(pause);
    }

    toneStop();
  }
};

class ServoManager {
private:
  int channel1;
  int channel2;
  int freq;
  int resolution;
  int pin1;
  int pin2;

public:
  ServoManager(int channel_PWM, int channel_PWM2, int freq_PWM, int resolution_PWM, int PWM_Pin1, int PWM_Pin2) : 
    channel1(channel_PWM), 
    channel2(channel_PWM2), 
    freq(freq_PWM), 
    resolution(resolution_PWM), 
    pin1(PWM_Pin1), 
    pin2(PWM_Pin2)
  {
    ledcSetup(channel1, freq, resolution); 
    ledcSetup(channel2, freq, resolution); 
    ledcAttachPin(pin1, channel1); 
    ledcAttachPin(pin2, channel2); 
  }

  void openWindow() {
    Serial.println("open the window");
    // Adjust the value as necessary to open the window
    ledcWrite(channel1, 90);
  }

  void closeWindow() {
    Serial.println("close the window");
    ledcWrite(channel1, 60);
  }

  void openDoor() {
    Serial.println("open the door");
    // Adjust the value as necessary to open the door
    ledcWrite(channel2, 40);
  }

  void closeDoor() {
    Serial.println("close the door");
    ledcWrite(channel2, 20);
  }
};

#define LED_PIN    26
#define LED_COUNT 4
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

class NeoPixelManager {
private:
  Adafruit_NeoPixel strip;
  int brightness;

public:
  NeoPixelManager(int pin, int ledCount, int brightness = 50)
    : strip(ledCount, pin, NEO_GRB + NEO_KHZ800), brightness(brightness)
  {
    //strip.begin();
    //strip.show();
    //strip.setBrightness(brightness);
  }

  // Define the accessors here:
  Adafruit_NeoPixel& getStrip() { return strip; }
  int getBrightness() { return brightness; }
  
  void setBrightness(int brightness) {
    strip.setBrightness(brightness);
  }

  void turnOnColor(const char* color) {
    if (strcmp(color, "red") == 0) {
      colorWipe(strip.Color(255,   0,   0), 50);
    } else if (strcmp(color, "orange") == 0) {
      colorWipe(strip.Color(200,   100,   0), 50);
    }
    // Add other color conditions here...
  }

  void turnOffColor() {
    colorWipe(strip.Color(0,   0,   0), 50);
  }

  void activateEffect(const char* effect) {
    if (strcmp(effect, "rainbow") == 0) {
      rainbow(10);
    } else if (strcmp(effect, "theaterChaseRainbow") == 0) {
      theaterChaseRainbow(50);
    }
    // Add other effects conditions here...
  }

  void deactivateEffect() {
    colorWipe(strip.Color(0,   0,   0), 50);
  }
  
  // Fill strip pixels one after another with a color. Strip is NOT cleared
  // first; anything there will be covered pixel by pixel. Pass in color
  // (as a single 'packed' 32-bit value, which you can get by calling
  // strip.Color(red, green, blue) as shown in the loop() function above),
  // and a delay time (in milliseconds) between pixels.
  void colorWipe(uint32_t color, int wait) {
    for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
      strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
      strip.show();                          //  Update strip to match
      delay(wait);                           //  Pause for a moment
    }
  }

  // Theater-marquee-style chasing lights. Pass in a color (32-bit value,
  // a la strip.Color(r,g,b) as mentioned above), and a delay time (in ms)
  // between frames.
  void theaterChase(uint32_t color, int wait) {
    for(int a=0; a<10; a++) {  // Repeat 10 times...
      for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
        strip.clear();         //   Set all pixels in RAM to 0 (off)
        // 'c' counts up from 'b' to end of strip in steps of 3...
        for(int c=b; c<strip.numPixels(); c += 3) {
          strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
        }
        strip.show(); // Update strip with new contents
        delay(wait);  // Pause for a moment
      }
    }
  }

  // Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
  void rainbow(int wait) {
    // Hue of first pixel runs 5 complete loops through the color wheel.
    // Color wheel has a range of 65536 but it's OK if we roll over, so
    // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
    // means we'll make 5*65536/256 = 1280 passes through this outer loop:
    for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
      for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
        // Offset pixel hue by an amount to make one full revolution of the
        // color wheel (range of 65536) along the length of the strip
        // (strip.numPixels() steps):
        int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
        // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
        // optionally add saturation and value (brightness) (each 0 to 255).
        // Here we're using just the single-argument hue variant. The result
        // is passed through strip.gamma32() to provide 'truer' colors
        // before assigning to each pixel:
        strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
      }
      strip.show(); // Update strip with new contents
      delay(wait);  // Pause for a moment
    }
  }

  // Rainbow-enhanced theater marquee. Pass delay time (in ms) between frames.
  void theaterChaseRainbow(int wait) {
    int firstPixelHue = 0;     // First pixel starts at red (hue 0)
    for(int a=0; a<30; a++) {  // Repeat 30 times...
      for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
        strip.clear();         //   Set all pixels in RAM to 0 (off)
        // 'c' counts up from 'b' to end of strip in increments of 3...
        for(int c=b; c<strip.numPixels(); c += 3) {
          // hue of pixel 'c' is offset by an amount to make one full
          // revolution of the color wheel (range 65536) along the length
          // of the strip (strip.numPixels() steps):
          int      hue   = firstPixelHue + c * 65536L / strip.numPixels();
          uint32_t color = strip.gamma32(strip.ColorHSV(hue)); // hue -> RGB
          strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
        }
        strip.show();                // Update strip with new contents
        delay(wait);                 // Pause for a moment
        firstPixelHue += 65536 / 90; // One cycle of color wheel over 90 frames
      }
    }
  }
};



#define fanPin1 19
#define fanPin2 18
#define led_y 12  //Define the yellow led pin to 12
#define buzzer_pin 25
#define btn1 16
#define btn2 27
#define pir 14

//Servo channel
int channel_PWM = 13;
int channel_PWM2 = 10;
int freq_PWM = 50; 
int resolution_PWM = 10;
const int PWM_Pin1 = 5;
const int PWM_Pin2 = 13;

#define LED_PIN    26
#define LED_COUNT 4



class SmartHouse : public Device {
public:
    XHT11Sensor xht11Sensor;
    LCDManager lcdManager;
    LEDManager ledManager;
    FanManager fanManager;
    BuzzerManager buzzerManager;
    ButtonManager buttonManager;
    PIRManager pirmanager;
    ServoManager servoManager;
    NeoPixelManager pixelManager;



    SmartHouse() : xht11Sensor(17), 
                   lcdManager(0x27, 16, 2), 
                   ledManager(led_y), 
                   fanManager(fanPin1, fanPin2), 
                   buzzerManager(buzzer_pin),
                   buttonManager(btn1, btn2),
                   pirmanager(pir),
                   servoManager(channel_PWM, channel_PWM2, freq_PWM, resolution_PWM, PWM_Pin1, PWM_Pin2),
                   pixelManager(LED_PIN, LED_COUNT)
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

        // Add properties for the buttons.
        registerProperty("button1", 
                 nullptr, 
                 [this]{ return buttonManager.getStringButtonState(btn1); });

        registerProperty("button2", 
                 nullptr, 
                 [this]{ return buttonManager.getStringButtonState(btn2); });



        registerCommand("birthday", [this](const char* payload) {
            buzzerManager.birthday(payload);
        });

        registerCommand("buzzer", [this](const char* payload) {
            buzzerManager.buzzer(payload);
        });

        registerCommand("play_notes", [this](const char* payload) {
          buzzerManager.play_notes(payload);
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

     void update() {
        buttonManager.updateButtonStates(mqttClient, "buttons"); // Update button states
        pirmanager.update(mqttClient, "motion"); 
        Device::update();

        // if (buttonManager.getButtonState(btn1)==false) {
        //    Serial.println("Button1");
        // }

        // if (buttonManager.getButtonState(btn2)==false) {
        //    Serial.println("Button2");
        // }

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

void handlePlayNotes(const char* topic, const char* payload) {

  smarthouse.buzzerManager.play_notes(payload);

  // Create a DynamicJsonDocument
  DynamicJsonDocument doc(128);

  // Populate the JSON document
  doc["play_notes"] = true;

  // Serialize the JSON document to a string
  String response;
  serializeJson(doc, response);

  mqttClient.publish("/swa/buzzer/ack", response.c_str());
}

void handleServoWindow(const char* topic, const char* payload) {
  // Parse JSON payload
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, payload);

  // Get state from JSON
  int state = doc["state"];

  // Perform action based on the payload
  if (state == 1) { 
    smarthouse.servoManager.openWindow();
  } else if (state == 0) {
    smarthouse.servoManager.closeWindow();
  }

  String response;
  serializeJson(doc, response);
  mqttClient.publish("/swa/servo/window/ack", response.c_str());
}

void handleServoDoor(const char* topic, const char* payload) {
  // Parse JSON payload
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, payload);

  // Get state from JSON
  int state = doc["state"];

  // Perform action based on the payload
  if (state == 1) {     
    smarthouse.servoManager.openDoor();
  } else if (state == 0) {
    smarthouse.servoManager.closeDoor();
  }

  String response;
  serializeJson(doc, response);
  mqttClient.publish("/swa/servo/door/ack", response.c_str());
}

void handleNeopixel(const char* topic, const char* payload) {
  // Parse JSON payload
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, payload);
  
  Serial.println("handleNeopixel");

  // Get color or effect and state from JSON
  JsonArray rgb = doc["rgb"] ;
  String color = doc["color"] | ""; // this will be empty if "effect" is used
  String effect = doc["effect"] | ""; // this will be empty if "color" is used
  String state = doc["state"] | "";
  int brightness = doc["brightness"] | 50; // default brightness is set to 50 if not specified

  // Perform null checks
  if (state == "") {
    // If "state" is empty, send an error message to MQTT topic
    String errorMsg = "{\"error\": \"Missing 'state' in payload.\"}";
    mqttClient.publish("/swa/errors/neopixel", errorMsg.c_str());
    return;
  }

  if (color == "" && effect == "") {
    // If both "color" and "effect" are empty, send an error message to MQTT topic
    String errorMsg = "{\"error\": \"Either 'color' or 'effect' must be specified in payload.\"}";
    mqttClient.publish("/swa/errors/neopixel", errorMsg.c_str());
    return;
  }


  if (!rgb.isNull() && (rgb.size() != 3 || rgb[0].is<int>() == false || rgb[1].is<int>() == false || rgb[2].is<int>() == false)) {
    // If "rgb" is specified but it's not an array of 3 integers, send an error message to MQTT topic
    String errorMsg = "{\"error\": \"'rgb' must be an array of 3 integers.\"}";
    mqttClient.publish("/swa/errors/neopixel", errorMsg.c_str());
    return;
  }


  if (brightness < 0 || brightness > 255) {
    // If brightness is not in range 0-255, send an error message to MQTT topic
    String errorMsg = "{\"error\": \"Brightness must be in range 0-255.\"}";
    mqttClient.publish("/swa/errors/neopixel", errorMsg.c_str());
    return;
  }

  // Apply brightness
  smarthouse.pixelManager.setBrightness(brightness);

  // Perform action based on the payload  
  if (state == "on") {
    if (!color.isEmpty()) {
      // Convert color name to RGB value and call colorWipe()
      if (color == "red") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(255,   0,   0), 50);
      } else if (color == "orange") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(200, 100,   0), 50);
      } else if (color == "yellow") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(200, 200,   0), 50);
      } else if (color == "green") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(200, 255,   0), 50);
      } else if (color == "cyan") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(0, 100,  255), 50);
      } else if (color == "blue") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(0, 0, 255), 50);
      } else if (color == "purple") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(100, 0, 255), 50);
      } else if (color == "white") {
        smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(255, 255, 255), 50);
      } 
      // Add other colors here...
    } else if (!effect.isEmpty()) {
      // Perform the specified effect
      if ((effect == "sfx1") || (effect == "rainbow")) {
        Serial.println("sfx1 on (rainbow)");
        smarthouse.pixelManager.rainbow(10);
      } else if ((effect == "sfx2") || (effect == "theaterChaseRainbow")) {
        Serial.println("sfx2 on (theaterChaseRainbow)");
        smarthouse.pixelManager.theaterChaseRainbow(50);
      } else if ((effect == "sfx3") || (effect == "theaterChase")) {
        Serial.println("sfx3 on (theaterChase)");        
        smarthouse.pixelManager.theaterChase(strip.Color(127, 127, 127), 50); // White, half brightness
        smarthouse.pixelManager.theaterChase(strip.Color(127,   0,   0), 50); // Red, half brightness
        smarthouse.pixelManager.theaterChase(strip.Color(  0,   0, 127), 50); // Blue, half brightness
      } 
      // Add other effects here...
    } else if (!rgb.isNull()) {
      // Set the color using the specified RGB values
      smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(rgb[0], rgb[1], rgb[2]), 50);
    }
  } else if (state == "off") {
    // Turn off the NeoPixel strip
    smarthouse.pixelManager.colorWipe(smarthouse.pixelManager.getStrip().Color(0, 0, 0), 50);
  }

  String response;
  serializeJson(doc, response);
  mqttClient.publish("/swa/neopixel/ack", response.c_str());
}


void publishNeopixelCapabilities(const char* topic, const char* payload) {
  // Create a JSON object
  DynamicJsonDocument doc(1024);

  // Add states
  JsonArray state = doc.createNestedArray("state");
  state.add("on");
  state.add("off");

  // Add brightness  
  doc["brightness"] = "0 to 255";

  // Add colors
  JsonArray color = doc.createNestedArray("color");
  color.add("red");
  color.add("orange");
  color.add("yellow");
  color.add("green");
  color.add("cyan");
  color.add("blue");
  color.add("purple");
  color.add("white");

  // Add effects
  JsonArray effect = doc.createNestedArray("effect");
  effect.add("sfx1");
  effect.add("sfx2");
  effect.add("sfx3");
  
  // RGB color
  doc["rgb"] = "Array of 3 integers from 0 to 255, in order [red, green, blue]";

  // Convert JSON object to a String
  String capabilities;
  serializeJson(doc, capabilities);

  // Publish the capabilities to the MQTT topic
  mqttClient.publish("/swa/commands/neopixel/capabilities", capabilities.c_str());
}

void publishDeviceTopicsAndPayloads(const char* topic, const char* payload) {
  // Create a JSON object
  DynamicJsonDocument doc(1024);

  // Add topics and their respective payloads

  // Door Sensor Topic
  JsonObject doorSensor = doc.createNestedObject("/swa/commands/door");
  doorSensor["payload"] = "{'state': '<open or close>'}";

  // Temperature Sensor Topic
  JsonObject tempSensor = doc.createNestedObject("/swa/commands/temp");
  tempSensor["payload"] = "{'state': '<temperature in Celsius>'}";

  // Humidity Sensor Topic
  JsonObject humiditySensor = doc.createNestedObject("/swa/commands/humidity");
  humiditySensor["payload"] = "{'state': '<humidity in percentage>'}";

  // Neopixel Topic
  JsonObject neopixel = doc.createNestedObject("/swa/commands/neopixel");
  neopixel["payload"] = "{'state': '<on or off>', 'color': '<color name>', 'effect': '<effect name>', 'rgb': '[R, G, B]'}";

  // Device Capabilities Topic
  JsonObject capabilities = doc.createNestedObject("/swa/commands/neopixel/capabilities");
  capabilities["payload"] = "{'state': ['on', 'off'], 'color': ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'white'], 'effect': ['sfx1', 'sfx2', 'sfx3'], 'rgb': 'Array of 3 integers from 0 to 255, in order [red, green, blue]'}";

  // Convert JSON object to a String
  String topicsAndPayloads;
  serializeJson(doc, topicsAndPayloads);

  // Publish the topics and their payloads to the MQTT topic
  mqttClient.publish("/swa/device/topics", topicsAndPayloads.c_str());
}


// Create a mapping of topics to callback functions
TopicCallback topicCallbacks[] = {
  {"/swa/commands/help", publishDeviceTopicsAndPayloads},
  {"/swa/commands/xht11", handleXHT11},
  {"/swa/commands/led/on", handleLedOn },
  {"/swa/commands/led/off", handleLedOff },
  {"/swa/commands/fan/on", handleFanOn },
  {"/swa/commands/fan/off", handleFanOff },
  {"/swa/commands/birthday", handlePlayBirthday },
  {"/swa/commands/buzzer", handleBuzzer },
  {"/swa/commands/play_notes", handlePlayNotes },
  {"/swa/commands/servo/window", handleServoWindow },  
  {"/swa/commands/servo/door", handleServoDoor },
  {"/swa/commands/neopixel", handleNeopixel},
  {"/swa/commands/neopixel/help", publishNeopixelCapabilities}  
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

  smarthouse.update();
}


