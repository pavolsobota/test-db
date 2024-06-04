"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const child_process_1 = require("child_process");
const path_1 = __importDefault(require("path"));
const app = (0, express_1.default)();
const PORT = process.env.PORT || 3000;
const outputFile = path_1.default.join(__dirname, '../public/output.csv'); // Ensure correct path
app.use(express_1.default.static('public'));
app.get('/run-script', (req, res) => {
    (0, child_process_1.exec)('python3 testdb.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send(`Error: ${error.message}`);
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.status(500).send(`Stderr: ${stderr}`);
        }
        console.log(`Stdout: ${stdout}`);
        res.download(outputFile, 'output.csv', (err) => {
            if (err) {
                console.error(`Download Error: ${err.message}`);
                return res.status(500).send(`Download Error: ${err.message}`);
            }
        });
    });
});
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
