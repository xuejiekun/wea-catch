 window.oncontextmenu = function() {
    event.preventDefault(); // 阻止默认事件行为
    return false;
    //alert('hello')
}

window.onkeydown = window.onkeyup = window.onkeypress = function (event) {
    // 判断是否按下F12，F12键码为123
    if (event.keyCode === 123) {
        event.preventDefault(); // 阻止默认事件行为
        window.event.returnValue = false;
    }
}