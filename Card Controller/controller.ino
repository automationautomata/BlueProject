#include <ArduinoJson.h>


///* Формат отправки данных - массив из структур с полями card и time
/// Пример:   { [{"card" = 25, "time" = 0;}, {"card" = 25, "time" = 1;}] }
/// Формат принятых данных - массив из номеров карт
/// Пример:   {[25, 134, 16]}
JsonDocument send_doc;
    JsonDocument recieve_doc;

String parsjson(String jsondata) {
    DeserializationError err = deserializeJson(recieve_doc, jsondata);
    return err.c_str();
}

void setup() {
  // Начинаем работу с Serial портом на скорости 9600 бит/с
  Serial.begin(9600);
  // // Пример заполнения
  // doc["sensor"] = "gps";
  // doc["time"]   = 1351824120;
  // doc["data"][0] = 48.756080;
  // doc["data"][1] = 2.302038;
  // send_doc[0]["card"] = 25;
  // send_doc[0]["time"] = 0;
}
// При работе НЕ с ардуино леонардо можно использовать SerialEvent, 
// а в loop просто проверять данные с датчика
void loop() {
  // Проверяем, есть ли данные из Serial порта
  if (Serial.available() > 0) {
    String receivedData = Serial.readString();
    Serial.print("Получено: dd " + parsjson(receivedData));
  }
  // int randNumber = random(300);
  // if (randNumber >= 200) {
  //   Serial.println("Отправка: " + randNumber);
  // }
}