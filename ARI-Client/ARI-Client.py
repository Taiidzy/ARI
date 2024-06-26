import threading
import speech_recognition as sr
import requests
import sys
import eel
import os
import subprocess
import json
import webbrowser
import pyautogui
import ctypes

# Инициализация Eel
eel.init("web")

# Переменная для отслеживания состояния Eel
eel_running = False

# Переменная для отслеживания состояния микрофона
mic_on = True
win_commands_on = True
web_commands_on = True
pc_commands_on = True

# Функция для запуска Eel в отдельном потоке
def start_eel():
    global eel_running
    eel.start("main.html", size=(400, 600))
    eel_running = False

# Загрузка команд для веб и ПК
def load_commands(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        commands = json.load(file)
    return commands

# Загрузка команд для веб и ПК
windows_commands = load_commands('windows_commands.json')
commands_web = load_commands('commands_web.json')
commands_pc = load_commands('commands_pc.json')


# Инициализация распознавателя речи и микрофона
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Функция для отправки команды на сервер в отдельном потоке
def send_command_async(command):
    threading.Thread(target=send_command, args=(command,)).start()

# Функция для отправки команды на сервер
def send_command(command):
    try:
        response = requests.post('http://192.168.0.107:5000/command', json={'command': command})
        print(response.text)
    except Exception as e:
        print("Ошибка при отправке команды на сервер:", e)

def update_log(text):
    eel.updateLogText(text)()  # Вызываем функцию updateLogText из JavaScript

# Основной цикл программы
def main():
    global eel_running
    global mic_on
    global win_commands_on
    global web_commands_on
    global pc_commands_on
    while True:
        if mic_on:
            with microphone as source:
                print("Скажите команду:")
                audio = recognizer.listen(source)  # Слушаем микрофон

            try:
                # Распознавание речи с использованием API Google
                command = recognizer.recognize_google(audio, language='ru-RU')
                print(f"Распознанная команда: {command}")
                update_log(command)  # Добавляем вывод команды в интерфейс

                # Проверка команды "отключить клиент"
                if command.lower() == "отключить клиент" or command.lower() == "Отключить клиент":
                    print("Остановка клиента...")
                    end()
                    sys.exit()  # Выход из основного потока
                else:
                    found_command = False
                    print("Поиск веб-команд:")
                    if web_commands_on:  # Проверяем состояние переключателя Веб Команды
                        for key, value in commands_web.items():
                            print(f"Ключ: {key}")
                            if command.lower() in key.lower():
                                print(f"Найдена веб-команда: {key}")
                                webbrowser.open(value)  # Открыть URL в браузере
                                found_command = True
                                break

                    if not found_command:
                        print("Поиск ПК-команд:")
                        if pc_commands_on:  # Проверяем состояние переключателя ПК Команды
                            for key, value in commands_pc.items():
                                print(f"Ключ: {key}")
                                if command.lower() in key.lower():
                                    print(f"Найдена ПК-команда: {key}")
                                    subprocess.Popen([value], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Запустить программу на ПК
                                    found_command = True
                                    break

                    if not found_command:
                        print("Поиск Windows-команд:")
                        if win_commands_on:  # Проверяем состояние переключателя Win Команды
                            for key, value in windows_commands.items():
                                print(f"Ключ: {key}")
                                if command.lower() in key.lower():
                                    print(f"Найдена Windows-команда: {key}")
                                    if value in globals() and callable(globals()[value]):
                                        # Проверяем, существует ли функция и вызываем её
                                        globals()[value]()
                                    else:
                                        print(f"Функция {value} не найдена или не является вызываемой")
                                    found_command = True
                                    break

                    if not found_command:
                        print("Команда не найдена")

                    if mic_on:  # Проверка состояния микрофона перед выполнением команды
                        send_command_async(command)  # Отправляем команду на сервер в отдельном потоке

            except sr.UnknownValueError:
                # Обработка ошибки, если команда не распознана
                print("Не удалось распознать команду")
            except sr.RequestError:
                # Обработка ошибки, если есть проблемы с подключением к API
                print("Ошибка подключения")

def hide_windows():
    try:
        pyautogui.hotkey('win', 'd')
    except Exception as e:
        print("Ошибка при скрытии окон:", e)

def show_windows():
    try:
        pyautogui.hotkey('win', 'd')
    except Exception as e:
        print("Ошибка при показе окон:", e)

def block_windows():
    try:
        print("Пытаюсь заблокировать экран...")
        ctypes.windll.user32.LockWorkStation()
        print("Экран успешно заблокирован.")
    except Exception as e:
        print("Ошибка при заблокировке экрана:", e)


def open_explorer():
    try:
        pyautogui.hotkey('win', 'e')
    except Exception as e:
        print("Ошибка при показе окон:", e)

# Запуск Eel в отдельном потоке
eel_running = True
eel_thread = threading.Thread(target=start_eel)
eel_thread.start()

@eel.expose
def toggleMicrophone():
    global mic_on
    mic_on = not mic_on

@eel.expose
def PcComOn():
    global pc_commands_on
    pc_commands_on = True

@eel.expose
def PcComOff():
    global pc_commands_on
    pc_commands_on = False

@eel.expose
def WinComOn():
    global win_commands_on
    win_commands_on = True

@eel.expose
def WinComOff():
    global win_commands_on
    win_commands_on = False

@eel.expose
def WebComOn():
    global web_commands_on
    web_commands_on = True

@eel.expose
def WebComOff():
    global web_commands_on
    web_commands_on = False


def end():
    os.system(R'taskkill /F /IM chrome.exe')

# Запуск основного цикла программы
main()
