from download_videos import download_video as download
from process_audio import extract_audio as audio
from process_video import process_video as video

import sys, os
import pytube
import shutil

# Sanity check
if sys.version_info < (3, 0):
    raise Exception("Code must be run using python3")


# TODO if dir already exists skip all this


# 1. Download the video
# Raises an exception if not a valid url
video_id, yt = download.get_video_id(sys.argv[1])
try:
    download.download_video(sys.argv[1])
except pytube.exceptions.RegexMatchError as e:
    shutil.rmtree("./public/saves/" + video_id)
    raise Exception("Malformed youtube url")

# Intermediate: make some directories
def make_if_not_exist(p):
    if not os.path.exists(p):
        os.makedirs(p)

make_if_not_exist("./public/saves/" + video_id + "/video_snippets")
make_if_not_exist("./public/saves/" + video_id + "/audio_snippets")

# 2. Extract breakpoints from video
try:
    breakpoints = audio.extract_audio(yt, video_id)
except (AttributeError, IndexError) as e:
    shutil.rmtree("./public/saves/" + video_id)
    raise Exception("Video has no captions")

# 3. Slice and format the video
temp_vid = "./public/saves/" + video_id + "/temp.mp4"
video.set_cut_dir(video_id)
video.process_videos(temp_vid, breakpoints)
os.remove(temp_vid)
