from download_videos import download_video as download
from process_audio import extract_audio as audio

import sys
import pytube
import os
print('WORKING')

# Sanity check
if sys.version_info < (3, 0):
    raise Exception("Code must be run using python3")


# TODO if dir already exists skip all this
#if os.path.isdir('./saves') == True:
 #   sys.exit()

# 1. Download the video
# Raises an exception if not a valid url
video_id, yt = download.get_video_id(sys.argv[1])
print(video_id)
try:
    download.download_video(sys.argv[1])
except pytube.exceptions.RegexMatchError as e:
    raise Exception("Malformed youtube url")

# 2. Extract breakpoints from video
try:
    breakpoints = audio.extract_audio(yt, video_id)
except (AttributeError, IndexError) as e:
    raise Exception("Video has no captions")

print(breakpoints)