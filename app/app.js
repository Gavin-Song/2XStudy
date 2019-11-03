const express = require("express");
const app = express();
const spawn = require("child_process").spawn;
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static('public'));

app.post('/api/download', (req, res) => {
	// These two lines of code download the YouTube Video based on the user-provided link
	const pythonProcess = spawn('python3', ["./download-and-process-video.py", req.body.videoUrl]);
	let sent = false;

	pythonProcess.stdout.on('data', data => {
		data = data.toString();
		if (data.startsWith('DONE') && !sent)
			res.send(data.toString());
	});
	pythonProcess.stderr.on('data', data => {
		console.log(data.toString())
		lines = data.toString().split('\n');
		res.send('ERROR ' + lines[lines.length - 2]);
		sent = true;
	});
	pythonProcess.on('close', code => {});
});

app.listen(5500, function () {
	console.log("server running on port 3000");
})