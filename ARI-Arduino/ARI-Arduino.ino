#include <Wire.h>

int relay1 = 4;  // Пин для реле 1
int relay2 = 5;  // Пин для реле 2
int relay3 = 6;  // Пин для реле 3
int relay4 = 7;  // Пин для реле 4
int relay5 = 8;  // Пин для реле 5
int relay6 = 9;  // Пин для реле 6
int relay7 = 10; // Пин для реле 7
int relay8 = 11; // Пин для реле 8
int relay9 = 12; // Пин для реле 9

void setup() {
  pinMode(relay1, OUTPUT);  // Настройка пина реле 1 как выход
  pinMode(relay2, OUTPUT);  // Настройка пина реле 2 как выход
  pinMode(relay3, OUTPUT);  // Настройка пина реле 3 как выход
  pinMode(relay4, OUTPUT);  // Настройка пина реле 4 как выход
  pinMode(relay5, OUTPUT);  // Настройка пина реле 5 как выход
  pinMode(relay6, OUTPUT);  // Настройка пина реле 6 как выход
  pinMode(relay7, OUTPUT);  // Настройка пина реле 7 как выход
  pinMode(relay8, OUTPUT);  // Настройка пина реле 8 как выход
  pinMode(relay9, OUTPUT);  // Настройка пина реле 9 как выход

  Serial.begin(9600);       // Начало серийной связи на скорости 9600 бод

  // Включение реле на 12 пине при запуске
  digitalWrite(relay9, HIGH); 
  Serial.println("Реле 9 включено при запуске");

  digitalWrite(relay2, HIGH); 
  Serial.println("Реле 2 включено при запуске");

  // Печать исходного состояния реле при запуске
  Serial.println("Arduino запущен");
}

void loop() {
  if (Serial.available()) {  // Проверка доступности данных для чтения
    char command = Serial.read();  // Чтение одного байта из серийного порта
    switch (command) {
      case '0':
        digitalWrite(relay1, HIGH);  // Выключение реле 1
        Serial.println("Реле 1 выключено");
        break;
      case '1':
        digitalWrite(relay1, LOW);   // Включение реле 1
        Serial.println("Реле 1 включено");
        break;
      case '2':
        digitalWrite(relay2, HIGH);  // Выключение реле 2
        Serial.println("Реле 2 выключено");
        break;
      case '3':
        digitalWrite(relay2, LOW);   // Включение реле 2
        Serial.println("Реле 2 включено");
        break;
      case '4':
        digitalWrite(relay3, HIGH);  // Выключение реле 3
        Serial.println("Реле 3 выключено");
        break;
      case '5':
        digitalWrite(relay3, LOW);   // Включение реле 3
        Serial.println("Реле 3 включено");
        break;
      case '6':
        digitalWrite(relay4, HIGH);  // Выключение реле 4
        Serial.println("Реле 4 выключено");
        break;
      case '7':
        digitalWrite(relay4, LOW);   // Включение реле 4
        Serial.println("Реле 4 включено");
        break;
      case '8':
        digitalWrite(relay5, HIGH);  // Выключение реле 5
        Serial.println("Реле 5 выключено");
        break;
      case '9':
        digitalWrite(relay5, LOW);   // Включение реле 5
        Serial.println("Реле 5 включено");
        break;
      case 'A':
        digitalWrite(relay6, HIGH);  // Выключение реле 6
        Serial.println("Реле 6 выключено");
        break;
      case 'B':
        digitalWrite(relay6, LOW);   // Включение реле 6
        Serial.println("Реле 6 включено");
        break;
      case 'C':
        digitalWrite(relay7, HIGH);  // Выключение реле 7
        Serial.println("Реле 7 выключено");
        break;
      case 'D':
        digitalWrite(relay7, LOW);   // Включение реле 7
        Serial.println("Реле 7 включено");
        break;
      case 'E':
        digitalWrite(relay8, HIGH);  // Выключение реле 8
        Serial.println("Реле 8 выключено");
        break;
      case 'F':
        digitalWrite(relay8, LOW);   // Включение реле 8
        Serial.println("Реле 8 включено");
        break;
      case 'G':
        digitalWrite(relay9, HIGH);  // Включение реле 9
        Serial.println("Реле 9 включено");
        break;
      case 'H':
        digitalWrite(relay9, LOW);   // Выключение реле 9
        Serial.println("Реле 9 выключено");
        break;
      default:
        // Обработка неизвестных команд
        Serial.println("Неизвестная команда");
        break;
    }
  }
}
