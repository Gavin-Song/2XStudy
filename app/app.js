const express = require("express");
const app = express();
const spawn = require("child_process").spawn;
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.get('/', (req, res) => {
	// Home (TEST) Page, Submit YouTube Video Link
	res.send(`
	<h1>Home (TEST) Page, Submit YouTube Video Link</h1>
	<form action='/api/download' method='POST'>
		<input name='videoUrl' type='text'>
		<button type='submit'>Submit</button>
	</form>
	`);
});

app.post('/api/download', (req, res) => {
	// These two lines of code download the YouTube Video based on the user-provided link
	const pythonProcess = spawn('python3', ["./download-and-process-video.py", req.body.videoUrl]);

	console.log("REE")
	pythonProcess.stdout.on('data', (data) => {
		console.log(`stdout: ${data}`);
	});
	pythonProcess.stderr.on('data', (data) => {
		console.error(`stderr: ${data}`);
	});
	pythonProcess.on('close', (code) => {
		console.log(`child process exited with code ${code}`);
	});
	res.send('Page to Display After Processsing/Speeding Up Video')
});

app.listen(5500, function () {
	console.log("server running on port 3000");
})