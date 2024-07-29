#include <ArduinoJson.h>
#include <EEPROM.h>

#define DATA_FLAG 0xAA // Маркер, указывающий наличие сохраненных данных в EEPROM
JsonDocument doc;

float EEPROM_int_read(int addr) {   
  byte raw[4];
	for(byte i = 0; i < 4; i++) raw[i] = EEPROM.read(addr+i);
  int &num = (int&)raw;
	return num;
}

void EEPROM_int_write(int addr, int num) {
	byte raw[4];
	(int&)raw = num;
	for(byte i = 0; i < 4; i++) EEPROM.write(addr+i, raw[i]);
}

String parsjson(String jsondata) {
    DeserializationError err = deserializeJson(doc, jsondata);
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
    String receivedData = Serial.readString();
    serializeJson(doc, receivedData);
  }
  
  if (random(30001) >= 30000) {
    String sendingdata = Serial.readString();
    serializeJson(getkeys(), sendingdata);
    Serial.print(sendingdata);
  }
}

void savekeys(JsonDocument doc) {
  JsonArray array = doc["keys"].as<JsonArray>();
  for (int i = 0; i < array.size(); i++) {
    EEPROM_int_write(i*sizeof(size_t), array[i]);
  }
}

JsonDocument getkeys() {
  JsonDocument array;
  for (int i = 0; i < array.size(); i++) {
    array["keys"][i] = EEPROM_int_read(i*sizeof(size_t));
  }
  return array;
}