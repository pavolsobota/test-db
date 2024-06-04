"use strict";
var _a;
(_a = document.getElementById('run-script')) === null || _a === void 0 ? void 0 : _a.addEventListener('click', () => {
    fetch('/run-script')
        .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Network response was not ok.');
    })
        .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'output.csv'; // Default filename
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
        .catch(error => {
        const outputElement = document.getElementById('output');
        if (outputElement) {
            outputElement.textContent = `Error: ${error.message}`;
        }
    });
});
