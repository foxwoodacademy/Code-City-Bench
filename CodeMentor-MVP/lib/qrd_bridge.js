// Bridge: QRD Terminal -> mentor CLI
// Inject this into qrd_codementor.html to make COMMANDS actually work

const { exec } = require('child_process');
const path = require('path');

function explainFile(filePath) {
    const cmd = `mentor "${filePath}" --html`;
    return new Promise((resolve, reject) => {
        exec(cmd, { cwd: '/storage/emulated/0/RootBase/CodeMentor-MVP' }, (err, stdout) => {
            if (err) reject(err);
            else resolve(stdout);
        });
    });
}

module.exports = { explainFile };
