#include <ArduinoJson.h>

JsonDocument doc;

void setup() {
  // Начинаем работу с Serial портом на скорости 9600 бит/с
  Serial.begin(9600);

  doc["sensor"] = "gps";
  doc["time"]   = 1351824120;
  doc["data"][0] = 48.756080;
  doc["data"][1] = 2.302038;

}

void loop() {
  // Проверяем, есть ли данные из Serial порта
  if (Serial.available() > 0) {
    String receivedData = Serial.readString();
    serializeJson(doc, receivedData);
    Serial.println("Получено: dd" + receivedData);
  }
}