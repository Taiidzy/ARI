from flask import Flask, request, jsonify, render_template
import serial
import threading
from datetime import datetime
import os
import json
import logging

app = Flask(__name__)

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Получение порта Arduino из переменных среды
arduino_port = os.getenv('ARDUINO_PORT', '/dev/ttyACM0')

# Объявляем arduino глобальной переменной
arduino = None

# Функция для установления соединения с Arduino
def connect_to_arduino():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, 9600, timeout=1)
    except serial.SerialException as e:
        logger.error("Ошибка при подключении к Arduino: %s", e)

# Функция для отправки данных на Arduino
def send_to_arduino(value):
    if arduino:
        arduino.write(value.encode())

# Функция для чтения данных с Arduino
# def read_from_arduino():
#     while True:
#         if arduino:
#             try:
#                 data = arduino.readline()
#                 if data:
#                     logger.info("Сообщение от Arduino (в байтах): %s", data)
#             except serial.SerialException as e:
#                 logger.error("Ошибка при чтении данных с Arduino: %s", e)
#                 break


# Запуск потока для установки соединения с Arduino
connect_thread = threading.Thread(target=connect_to_arduino)
connect_thread.start()

# Запуск потока для чтения данных с Arduino
# 		read_thread = threading.Thread(target=read_from_arduino)
#	 	read_thread.start()

# Функция для обработки команд из файла JSON
def process_commands_from_json(command):
    with open('commands.json', 'r', encoding='utf-8') as file:
        commands = json.load(file)
    if command in commands:
        value = commands[command]
        if value:
            send_to_arduino(value)
            # Запись команды в журнал
            with open('commands.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f'{datetime.now()}: {str(command)}\n')  # Явное преобразование в строку
            # Отображение команды в консоли
            logger.info("Обработана команда: %s", command)
        else:
            logger.warning("Команда %s не имеет определенного значения", command)
    else:
        logger.warning("Команда %s не найдена в файле commands.json", command)


@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    print("Пришла команда: ", command)
    if command:
        process_commands_from_json(command)
        return 'Команда отправлена на Arduino'
    else:
        return 'Не удалось отправить команду на Arduino'

@app.route('/control')
def control():
    return render_template('control.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
