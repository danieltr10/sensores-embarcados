#include <ESP8266WiFi.h>
#include <PubSubClient.h>

//const char* ssid = "GRUPO6";
//const char* password =  "grupo6";
//const char* mqttServer = "172.24.1.1";
//const int mqttPort = 1883;
//const char* mqttUser = "username";
//const char* mqttPassword = "grupo6";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
//  GPIO A SER VERIFICADA
  pinMode(2, INPUT);

  Serial.begin(115200);

// Método para conectar o Wi-Fi
  conectWifi();
  
  client.publish("esp/controle", "switch");
  Serial.println("publish enviado");
}

  
void checkInput(){
  int value = digitalRead(2);
  if(value == 1) {
    client.publish("esp/controle", "switch");
  } else{
    client.publish("esp/controle", "gpio2");
  }
}

void conectWifi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {

      Serial.println("connected");

    } else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}
}

void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  String str((char*)topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  
  Serial.println();
  Serial.println("-----------------------");

}
void loop() {
  client.loop();
  checkInput();
  delay(5000);
}
