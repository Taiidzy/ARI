from flask import Flask, request
import serial
import threading
from datetime import datetime
import subprocess

app = Flask(__name__)

# Подключение к Arduino через указанный COM порт
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
except serial.SerialException as e:
    print("Ошибка подключения к Arduino:", e)

# Функция для отправки данных на Arduino
def send_to_arduino(command):
    if arduino:
        arduino.write(command.encode())

# Отдельный поток для чтения данных с Arduino
def read_from_arduino():
    while True:
        if arduino:
            data = arduino.readline().decode().strip()
            if data:
                print(f"Arduino: {data}")

# Запуск потока чтения данных с Arduino
thread = threading.Thread(target=read_from_arduino)
thread.start()

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    command = data.get('command')

    # Проверка команды и отправка соответствующего сигнала на Arduino
    if command == 'Включи подсветку':
        send_to_arduino('1')  # Команда на включение реле
    elif command == 'Выключи подсветку':
        send_to_arduino('0')  # Команда на выключение реле
    

    # Запись команды в файл
    with open('commands.log', 'a', encoding='utf-8') as file:
        file.write(f'{datetime.now()}: {command}\n')

    return 'Команда отправлена на Arduino'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
