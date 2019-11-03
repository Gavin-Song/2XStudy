from download_videos import download_video as download
from process_audio import extract_audio as audio
from process_video import process_video as video

import sys, os
import pytube
import shutil
import re
import json

# Sanity check
if sys.version_info < (3, 0):
    raise Exception("Code must be run using python3")

# Already exists no calculate
video_id, yt = download.get_video_id(sys.argv[1])
if os.path.exists("./public/saves/" + video_id):
    with open("./public/saves/" + video_id + "/meta_data.json") as f:
        print("DONE {} {}".format(
            video_id,
            f.read()
        ))
    __import__("sys").exit(0)


# Not a url
if not re.match(r"^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+", sys.argv[1]):
    raise Exception("pytube.exceptions.RegexMatchError")

# 1. Download the video
# Raises an exception if not a valid url
try:
    _, _, metadata = download.download_video(sys.argv[1])
except Exception as e:
    if os.path.exists("./public/saves/" + video_id):
        shutil.rmtree("./public/saves/" + video_id)
    raise Exception(str(e))

# Intermediate: make some directories
def make_if_not_exist(p):
    if not os.path.exists(p):
        os.makedirs(p)

make_if_not_exist("./public/saves/" + video_id + "/video_snippets")
make_if_not_exist("./public/saves/" + video_id + "/audio_snippets")

# 2. Extract breakpoints from video
try:
    breakpoints = audio.extract_audio(yt, video_id)
except:
    if os.path.exists("./public/saves/" + video_id):
        shutil.rmtree("./public/saves/" + video_id)
    raise Exception("Video has no captions")

# 3. Slice and format the video
temp_vid = "./public/saves/" + video_id + "/temp.mp4"
video.set_cut_dir(video_id)
video.process_videos(temp_vid, breakpoints)

# 4. Thumbnail
video.run_process(video.FFMPEG_DIR, ["-ss", "00:00:05", "-i", temp_vid, "-vframes", "1", "-q:v", "2",
    "./public/saves/" + video_id + "/thumb.jpg"])
# os.remove(temp_vid)

# 5. Make the HMTL template

transcriptions = ""
count = 0
for i, b in enumerate(breakpoints):
    text = b[list(b.keys())[0]]
    if text == "": continue
    transcriptions += """
<audio id="audio-{id}" style="display: none">
  <source src="/saves/{video_id}/audio_snippets/{id}.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>

<video width="50%" src="/saves/{video_id}/video_snippets/{id2}.mp4" muted loop></video>

<table class="text-snippet" style="width: calc(100% + 160px); position: relative; left: -160px">
    <tr>
        <td style="width: 160px">
            <!-- Toggle volume_up and pause -->
            <button onclick="togglePlaybackSound({id}, this)" class="round-button inline-big-button" style="margin: auto"><i class="material-icons">
                    volume_up</i></button>
            &nbsp;
            <button class="round-button inline-big-button" style="margin: auto"><i class="material-icons">
                    refresh</i></button>
        </td>
        <td style="width: calc(100% - 160px)">
            <p>
                {text}
            </p>
        </td>
    </tr>
</table>
        """.format(video_id=video_id, id=count, text=text, id2=i)
    count += 1


template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">

    <title>2XStudy</title>
    <meta name="description" content="An app to transcribe and abridge youtube videos for studying">
    <meta name="author" content="TheHumbleOnes">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/page.css">
    <link href="https://fonts.googleapis.com/css?family=Jomolhari|Montserrat&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Inconsolata&display=swap" rel="stylesheet">
</head>

<body>
    <script>
        let BREAKS = {speeds};
    </script>

    <div class="title-bar">
        <a href="/index.html"><img src="/img/logo.png" class="logo"></a>
        <ul class="nav">
            <li><a href="/index.html">Home</a></li>
            <li><a href="/about.html">About</a></li>
            <li><a href="https://github.com/Gavin-Song/2XStudy">Github</a></li>
        </ul>
    </div>

    <div class="page-container">
        <br><br><br><br>

        <!-- Absolutely placed -->
        <button onclick="window.location.href = '/index.html';" class="invisible-button inline-big-button back-button"><i class="material-icons">
            arrow_back_ios
        </i></button>

        <button class="round-button inline-big-button edit-button"><i class="material-icons">
                edit</i></button>

        <button onclick="share()" class="round-button inline-big-button share-button"><i class="material-icons">
                share</i></button>
        
        <!-- Normal stuff -->
        <br>
        <h1>{title}</h1>
        <small style="position: relative; top: -10px">{author} | {time}</small>
        <br><br>

        <h2>Abriged Video</h2><br>
        <video id="main-vid" width="100%" height="auto" src="{src}" type="video/mp4" controls>
            Your browser does not support the video tag.
        </video>
        <div id="video-speed-control">
            <button id="video-speed-0.25" onclick="videoSpeed(0.25)">0.25x</button>
            <button id="video-speed-0.5" onclick="videoSpeed(0.5)">0.5x</button>
            <button id="video-speed-0.75" onclick="videoSpeed(0.75)">0.75x</button>
            <button id="video-speed-1" class="active" onclick="videoSpeed(1)">1x</button>
            <button id="video-speed-1.25" onclick="videoSpeed(1.25)">1.25x</button>
            <button id="video-speed-1.5" onclick="videoSpeed(1.5)">1.5x</button>
            <button id="video-speed-1.75" onclick="videoSpeed(1.75)">1.75x</button>
            <button id="video-speed-2" onclick="videoSpeed(2)">2x</button>
            <button id="video-speed-2.5" onclick="videoSpeed(2.5)">2.5x</button>
            <button id="video-speed-3" onclick="videoSpeed(3)">3x</button>
        </div>

        <br><br><br>
        <h2>Transcription</h2>
        {transcriptions}

        <br><br><br><br>
    </div>

    <div class="modal" style="display: none" id="modal">
        <button onclick="document.getElementById('modal').style.display = 'none';"
            style="float: right" class="invisible-button inline-big-button">
            <i class="material-icons">close</i></button>

        <div id="qrcode"></div>
        <br>
        Or share this url
        <div class="monospace" id="url">
            
        </div>
    </div>

    <!-- NO JS ENABLED -->
    <noscript>
        <div class="modal" style="background-color: red" id="modal">
            <button onclick="document.getElementById('modal').style.display = 'none';"
                class="invisible-button inline-big-button">
                <i class="material-icons">close</i></button>
            Please enable javascript!
        </div>
    </noscript>

    <script src="/js/qrcode.js"></script>
    <script src="/js/share.js"></script>
    <script src="/js/video.js"></script>
</body>

</html>""".format(
    title=metadata["video_title"],
    author=metadata["video_author"],
    time=metadata["video_length"],
    src="/saves/" + video_id + "/temp.mp4",
    transcriptions=transcriptions,
    speeds=json.dumps(breakpoints)
)
with open("./public/saves/" + video_id + "/index.html", "w") as f:
    f.write(template)

print("DONE {} {}".format(video_id, json.dumps(metadata)))