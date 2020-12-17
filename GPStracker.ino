// Including the Ublox library
#include "Ublox.h"

// Determine which module we need, which is the M8N GPS
Ublox M8_Gps;


// Including the WiFi library for the ESP8266
#include <ESP8266WiFi.h>

// Connection to Hotspot/WiFi with ssid and password
const char* ssid = "ZyXEL3B4113";
const char* password = "4D2C18E2DB5E";


// Including the pubsubclient library so that we can publish messages through MQTT
#include <PubSubClient.h>

// Inserting the MQTT server that we use 
const char* mqtt_server = "test.mosquitto.org";


// Importing DHT library + softwareserial for the temperature sensor
#include "DHTesp.h"
#include <SoftwareSerial.h>
DHTesp dht;

//GPS NEO M8N pins (RX,TX)
SoftwareSerial mySerial(2, 0);


WiFiClient espClient;
PubSubClient client(espClient);


// 3 messages for 3 different data outputs to MQTT
char msg[50];
char msg2[50];
char msg3[50];


void setup_wifi() {
  delay(10);
  // Basic connection to wifi
  WiFi.begin(ssid, password);
  }


// If client isnt connected, then try to reconnect
void reconnect() {
  while (!client.connected()) {
    if (client.connect("thermometer1")) {  //CLIENT ID IS  thermometer1
      Serial.print("succes, rc=");
      Serial.print(client.state());
      delay(1000);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(1000);
    }
  }
}


void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);

  // Calling the wifi setup function
  setup_wifi();

  // Setting the mqtt server up  
  client.setServer(mqtt_server, 1883);

  // Connect DHT sensor to GPIO 5
  dht.setup(5, DHTesp::DHT22); 
}

void loop()
{
    if (!client.connected()) {
    reconnect();
  }

  // making a loop which prints data to mqtt 
  client.loop();
  snprintf (msg, 50, "%f", M8_Gps.latitude);
  snprintf (msg2, 50, "%f", M8_Gps.longitude);
  snprintf (msg3, 50, "%f", dht.getTemperature());
  client.publish("Gpstracker/latitude", msg); 
  client.publish("Gpstracker/longitude", msg2); 
  client.publish("Gpstracker/temperature", msg3); 
  Serial.println(msg);
  // Delay to make sure the messages went through
  delay(500);
  // Going to deepsleep 
  ESP.deepSleep(10e6);
 
  

}
