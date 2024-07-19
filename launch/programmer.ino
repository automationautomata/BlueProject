    // даём разумное имя для пина
    // который будет выполнять сброс микроконтоллера
    #define RESET 4
     
    char buff[4];
     
    // переменная состояния режима программирования
    bool programming = false;
     
    void setup()
    {
      // открываем последовательный порт
      // для приёма и отправки данных в USB
      Serial.begin(115200);
//Serial.begin(9600);
      // открываем последовательный порт
      // для приёма и отправки данных в плату Iskra Mini
      Serial1.begin(115200);
//Serial1.begin(9600);
    }
     
    void loop()
    {
      // если программа в режиме программирования
      if (programming) {
        // читаем данные с USB и записываем в плату Iskra Mini
        progUSBRead();
        // читаем данные с платы Iskra Mini и записываем в USB
        progMiniRead();        
//Serial.println("programming=true");
      } else if (Serial.available()) {
        // если приходят данные с USB
        pinMode(RESET, OUTPUT);
        digitalWrite(RESET, LOW);
        delay(50);
        digitalWrite(RESET, HIGH);
        delay(50);
        programming = true;
//Serial.println("Serial.available");
      } else if (Serial1.available()) {
        // если приходят данные с платы Iskra Mini
        // читаем данные с USB и записываем в плату Iskra Mini
        serialUSBRead();
        // читаем данные с платы Iskra Mini и записываем в USB
        serialMiniRead();
//Serial.println("Serial1.available");
      }
    }
     
    void progUSBRead()
    {
      // если появились данные с USB
      if (Serial.available()) {
        // считываем символ
        char c = (char)Serial.read();
        // записываем этот символ в плату Iskra Mini
        Serial1.write(c);
        // проверка на завершение процесса прошивки
        switch (c) {
          case 'Q':
          buff[0] = 'Q';
          break;
          case ' ':
          if (buff[0] == 'Q') {
            buff[1] = ' ';
            break;
          }
          buff[0] = '\0';
          break;
          default:
          buff[0]= '\0';
          break;
        }
      }
    }
     
    void progMiniRead()
    {
      // если появились данные с платы Iskra Mini
      if (Serial1.available()) {
        // считываем символ
        char c = (char)Serial1.read();
        // записываем этот символ в USB
        Serial.write(c);
        // проверка на завершение процесса прошивки
        if (buff[1] == ' ') {
          buff[1] = 'O';
          buff[2] = 'K';
        } else if (buff[1] == 'O' && buff[2] == 'K') {
          programming = false;
          clearbuff();
        }
      }
    }
     
    void serialUSBRead()
    {
      // если появились данные с USB
      if (Serial.available()) {
        // считываем символ
        char c = (char)Serial.read();
        // записываем этот символ в плату Iskra Mini
        Serial1.write(c);
      }
    }
    void serialMiniRead()
    {
      // если появились данные с платы Iskra Mini
      if (Serial1.available()) {
        // считываем символ
        char c = (char)Serial1.read();
        // записываем этот символ в плату Iskra Mini
        Serial.write(c);
      }
    }
     
    // функция очистки буфера
    void clearbuff()
    {
      for (int i = 0; i < 4; i++) {
        buff[i] = 0;
      }
    }


