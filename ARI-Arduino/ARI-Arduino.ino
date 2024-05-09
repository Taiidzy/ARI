int relay = 10;  // Пин, к которому подключено реле

void setup() {
  pinMode(relay, OUTPUT);  // Настройка пина реле как выход
  Serial.begin(9600);      // Начало серийной связи на скорости 9600 бод
}

void loop() {
  if (Serial.available()) {  // Проверка доступности данных для чтения
    char command = Serial.read();  // Чтение одного байта из серийного порта
    if (command == '1') {
      digitalWrite(relay, HIGH);  // Включение реле
    } else if (command == '0') {
      digitalWrite(relay, LOW);   // Выключение реле
    }
  }
}
