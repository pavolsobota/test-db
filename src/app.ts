import express from 'express';
import { exec } from 'child_process';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 3000;
const outputFile = path.join(__dirname, '../public/output.csv');  // Ensure correct path

app.use(express.static('public'));

app.get('/run-script', (req, res) => {
  exec('python3 testdb.py', (error, stdout, stderr) => {
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
