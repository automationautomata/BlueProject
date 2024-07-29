#include <ArduinoJson.h>

String parsjson(String jsondata) {
    DeserializationError err = deserializeJson(recieve_doc, jsondata);
    return err.c_str();
}

void setup() {
  Serial.begin(9600);
}
// При работе НЕ с ардуино леонардо можно использовать SerialEvent, 
// а в loop просто проверять данные с датчика
void loop() {
  // Проверяем, есть ли данные из Serial порта
  if (Serial.available() > 0) {
    JsonDocument doc;
    String receivedData = Serial.readString();
    serializeJson(doc, receivedData);
  }
  
  if (random(30001) >= 30000) {
    String sendingdata = Serial.readString();
    serializeJson(getkeys(), sendingdata);
    Serial.print(sendingdata)
  }
}

void savekeys(JsonDocument doc) {
  JsonArray array = doc["keys"].as<JsonArray>();
  for (int i = 0; i < array.size(); i++) {
    EEPROM.write(i*sizeof(size_t), array[i]);
  }
}

JsonDocument getkeys() {
  JsonDocument array;
  for (int i = 0; i < array.size(); i++) {
    EEPROM.read(i*sizeof(size_t), array["keys"][i]);
  }
  return array
}