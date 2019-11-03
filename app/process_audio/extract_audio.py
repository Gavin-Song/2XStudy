# Yash Mistri

from pytube import YouTube
from process_video import process_video
import json
import os
import subprocess

SAVE_DIR_FORMAT = "./public/saves/{}/"
PADDING = 1

"""
function extract_audio

parameters: type: string name: url (url of YouTube video)

returns: nothing (void)

goals:
    extract audio from video
    for every caption:
        add new entry to dictionary:
            key: time where audio switches to or from silence and speech
            value: the transcription from current time to the next time
        create audio snippet from previous time to current time in dictionary
        save audio snippet to saves/audio_snippets
    save dictionary to saves/transcriptions.json
"""
def extract_audio(youtube, video_id):
    """
    :param youtube: Youtube object from pytube
    :param video_id: Video id
    :return: Array of [{time_in_seconds: text}]
    """

    # download audio from Youtube video given by url
    video = youtube

    # Get captions
    caption = video.captions.get_by_language_code("en") or video.captions.all()[0]
    caption_list = caption.generate_srt_captions().splitlines()

    # stream.download()
    timestamps = [] #list of dictionaries- time: text
    num = 0 # for labeling exported segments
    timestamps.append({0.0 : ""})

    # load audio from file downloaded above
    process_video.run_process(process_video.FFMPEG_DIR, [
        "-y", "-i", SAVE_DIR_FORMAT.format(video_id) + "temp.mp4",
        "-vn", "-acodec", "libmp3lame", "-ac", "2", "-ab",
        "160k", "-ar", "48000", SAVE_DIR_FORMAT.format(video_id) + "temp.mp3"
    ])

    for i in range(1, len(caption_list), 4):
        sub = caption_list[i].split(' --> ')    # [hhh:mmm:ss,uuu, hhh:mmm:ss,uuu]
        time = []
        time_var = [0.0, 0.0]

        # parse times from string
        for j in range(2):
            time = sub[0].split(',')                    # [hhh:mmm:ss, uuu]
            time_var[j] += float(time[1]) * .001       # milliseconds
            time = time[0].split(':')                      # split h, m, s
            time_var[j] += float(time[0]) * 360 + float(time[1]) * 60 + float(time[2])

        # create entries in dictionary 'timestamps'
        timestamps.append({time_var[0] - 0.01 - PADDING : caption_list[i + 1]})
        timestamps.append({time_var[1] + PADDING : ""})


    # Export audio clips
    prev, previ = 0.0, 0
    for val in timestamps:
        keys = list(val.keys())
        if prev != keys[0]:
            # Slice audio from prev to here and export
            if list(timestamps[num].values())[0] != "":
                pass
                process_video.run_process(process_video.FFMPEG_DIR, [
                    "-y", "-ss", process_video.format_time(prev),
                    "-t", process_video.format_time(keys[0] - prev),
                    "-i", SAVE_DIR_FORMAT.format(video_id) + "temp.mp3",
                    "-acodec", "copy",
                    "-async", "1",
                    SAVE_DIR_FORMAT.format(video_id) + "audio_snippets/{}.mp3".format(num)
                ])
            num += 1
        prev, previ = keys[0], num

    json_file = json.dumps(timestamps)
    file_obj = open(SAVE_DIR_FORMAT.format(video_id) + "timestamps.json", "w")
    file_obj.write(json_file)
    # os.remove(SAVE_DIR_FORMAT.format(video_id) + "temp.mp3")
    return timestamps
