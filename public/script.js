"use strict";
var _a;
(_a = document.getElementById('run-script')) === null || _a === void 0 ? void 0 : _a.addEventListener('click', () => {
    fetch('/run-script')
        .then(response => response.text())
        .then(data => {
        const outputElement = document.getElementById('output');
        if (outputElement) {
            outputElement.textContent = data;
        }
    })
        .catch(error => {
        const outputElement = document.getElementById('output');
        if (outputElement) {
            outputElement.textContent = `Error: ${error.message}`;
        }
    });
});
