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



