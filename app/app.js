const express = require("express");
const app = express();
const spawn = require("child_process").spawn;
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.use(express.static('public'));

app.get('/', (req, res) => {
	 res.sendFile('./index.html');
});


app.post('/api/download', (req, res) => {
	// These two lines of code download the YouTube Video based on the user-provided link
	const pythonProcess = spawn('python', ["./download-and-process-video.py", req.body.videoUrl]);
	console.log(req.body.videoUrl)
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

port = process.env.PORT || 5500;
app.listen(port, () => {
	console.log(`server running on port ${port}`);
});