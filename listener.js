/*
process.stdin.resume();
process.stdin.setEncoding('utf8');
var util = require('util');

process.stdin.on('data', function (text) {
 console.log('received data:', util.inspect(text));
 if (text === 'quit\r\n') {
   done();
 }
});

function done() {
 console.log('Now that process.stdin is paused, there is nothing more to do.');
 process.exit();
}
*/

const { exec } = require('child_process');
exec('cls', (err, stdout, stderr) => {
  if (err) {
    console.log("ERROR")
    return;
  }

  // the *entire* stdout and stderr (buffered)
  console.log(`stdout: ${stdout}`);
  console.log(`stderr: ${stderr}`);
});
