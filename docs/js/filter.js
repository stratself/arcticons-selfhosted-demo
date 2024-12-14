function filter(className) {
    var icons = document.querySelectorAll(`.${className}`);
    var button = document.getElementById(`${className}-toggle`);
    icons.forEach(function (icon) {
        icon.classList.toggle("invisible");
    });
    button.classList.toggle("button-on");
} 