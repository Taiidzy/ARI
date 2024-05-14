window.onresize = function () {
    window.resizeTo(400, 600);
}

function toggleMicrophone() {
    var micBtnOn = document.querySelector('.mic-btn-on');
    var micBtnOff = document.querySelector('.mic-btn-off');

    var isOnVisible = micBtnOn.style.display !== 'none';

    if (isOnVisible) {
        micBtnOn.style.display = 'none';
        micBtnOff.style.display = 'block';
    } else {
        micBtnOn.style.display = 'block';
        micBtnOff.style.display = 'none';
    }

    // Вызов функции toggleMicrophone в Python
    eel.toggleMicrophone();
}

function WebComOn() {
    var webCheckbox = document.querySelector("#settingsMenu input[type=checkbox][id='WebCommandsSwitch']");
    // Вызов функции WebComOn в Python
    if (webCheckbox.checked) {
        eel.WebComOn();
    } else {
        eel.WebComOff();
    }
}

function PcComOn() {
    // Получаем переключатель ПК команд
    var pcCommandsSwitch = document.querySelector("#settingsMenu input[type=checkbox][id='pcCommandsSwitch']");
    
    // Вызываем соответствующую функцию Python, если переключатель включен
    if (pcCommandsSwitch.checked) {
        eel.PcComOn();
    } else {
        eel.PcComOff();
    }
}

function WinComOn() {
    // Получаем переключатель Windows команд
    var winCommandsSwitch = document.querySelector("#settingsMenu input[type=checkbox][id='winCommandsSwitch']");
    
    // Вызываем соответствующую функцию Python, если переключатель включен
    if (winCommandsSwitch.checked) {
        eel.WinComOn();
    } else {
        eel.WinComOff();
    }
}

eel.expose(updateLogText); // Объявляем функцию доступной для Python кода

function updateLogText(text) {
    console.log(text); // Выводим текст в консоль браузера
    var logText = document.getElementById('logText');
    logText.textContent += text + '\n';
}

function toggleSettingsMenu() {
    var menu = document.getElementById('settingsMenu');
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'block';
    }
}

function toggleLog() {
    var logToggle = document.getElementById('logToggle');
    // Ваш код для обработки переключения лога
}

function toggleLogDisplay() {
    var logDiv = document.getElementById("logDiv"); // Получаем элемент лога
    var logCheckbox = document.querySelector("#settingsMenu input[type=checkbox]"); // Получаем переключатель лога

    if (logCheckbox.checked) { // Если переключатель включен
        logDiv.style.display = "block"; // Показываем лог
    } else {
        logDiv.style.display = "none"; // Скрываем лог
    }
}

document.getElementById("addCommandsBtn").addEventListener("click", function() {
    var containerDiv = document.querySelector(".container");
    var addComandDiv = document.getElementById("addComand");
    
    containerDiv.classList.add("hidden");
    addComandDiv.classList.remove("hidden");
});

document.getElementById("home").addEventListener("click", function() {
    var containerDiv = document.querySelector(".container");
    var addComandDiv = document.getElementById("addComand");
    
    containerDiv.classList.remove("hidden");
    addComandDiv.classList.add("hidden");
});
