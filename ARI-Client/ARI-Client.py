import threading
import speech_recognition as sr
import requests
import sys
import eel
import os

# Инициализация Eel
eel.init("web")

# Переменная для отслеживания состояния Eel
eel_running = False

# Переменная для отслеживания состояния микрофона
mic_on = True

# Функция для запуска Eel в отдельном потоке
def start_eel():
    global eel_running
    eel.start("main.html", size=(400, 600))
    eel_running = False

# Инициализация распознавателя речи и микрофона
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Функция для отправки команды на сервер в отдельном потоке
def send_command_async(command):
    threading.Thread(target=send_command, args=(command,)).start()

# Функция для отправки команды на сервер
def send_command(command):
    try:
        response = requests.post('http://localhost:5000/command', json={'command': command})
        print(response.text)
    except Exception as e:
        print("Ошибка при отправке команды на сервер:", e)

# Основной цикл программы
def main():
    global eel_running
    global mic_on
    while True:
        if mic_on:
            with microphone as source:
                print("Скажите команду:")
                audio = recognizer.listen(source)  # Слушаем микрофон

            try:
                # Распознавание речи с использованием API Google
                command = recognizer.recognize_google(audio, language='ru-RU')
                print(f"Распознанная команда: {command}")

                # Проверка команды "отключить клиент"
                if command.lower() == "отключить клиент" or command.lower() == "Отключить клиент":
                    print("Остановка клиента...")
                    end()
                    sys.exit()  # Выход из основного потока
                    
                else:
                    if mic_on:  # Проверка состояния микрофона перед выполнением команды
                        send_command_async(command)  # Отправляем команду на сервер в отдельном потоке

            except sr.UnknownValueError:
                # Обработка ошибки, если команда не распознана
                print("Не удалось распознать команду")
            except sr.RequestError:
                # Обработка ошибки, если есть проблемы с подключением к API
                print("Ошибка подключения")

# Запуск Eel в отдельном потоке
eel_running = True
eel_thread = threading.Thread(target=start_eel)
eel_thread.start()

@eel.expose
def toggleMicrophone():
    global mic_on
    mic_on = not mic_on

def end():
    os.system(R'taskkill /F /IM chrome.exe')

# Запуск основного цикла программы
main()
