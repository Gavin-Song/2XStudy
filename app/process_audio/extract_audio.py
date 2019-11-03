# Yash Mistri

from pytube import YouTube
from process_video import process_video
import json
import os
import subprocess

SAVE_DIR_FORMAT = "./saves/{}/"
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
    commands_queued = []
    commands_queued.append([
        process_video.FFMPEG_DIR,
        "-y", "-i", SAVE_DIR_FORMAT.format(video_id) + "temp.mp4",
        "-vn", "-acodec", "libmp3lame", "-ac", "2", "-ab",
        "160k", "-ar", "48000", SAVE_DIR_FORMAT.format(video_id) + "temp.mp3"
    ])

    # process_video.run_process(process_video.FFMPEG_DIR, [
    #     "-y", "-i", SAVE_DIR_FORMAT.format(video_id) + "temp.mp4",
    #     "-vn", "-acodec", "libmp3lame", "-ac", "2", "-ab",
    #     "160k", "-ar", "48000", SAVE_DIR_FORMAT.format(video_id) + "temp.mp3"
    # ])

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
        timestamps.append({time_var[0] - 0.01 : caption_list[i + 1]})
        timestamps.append({time_var[1] : ""})


    # Export audio clips
    prev, previ = 0.0, 0
    for val in timestamps:
        keys = list(val.keys())
        if prev != keys[0]:
            # Slice audio from prev to here and export
            if list(timestamps[num].values())[0] != "":
                commands_queued.append([
                    process_video.FFMPEG_DIR,
                    "-y", "-ss", process_video.format_time(prev - PADDING),
                    "-t", process_video.format_time(keys[0] - prev + PADDING),
                    "-i", SAVE_DIR_FORMAT.format(video_id) + "temp.mp3",
                    "-acodec", "copy",
                    SAVE_DIR_FORMAT.format(video_id) + "audio_snippets/{}.mp3".format(num)
                ])
            num += 1
        prev, previ = keys[0], num

    # Run commands that are queued
    print(str(subprocess.check_output(commands_queued[0])))
    commands = "\n".join([ str(subprocess.check_output(x)) + " " + process_video.NO_LOG_STR for x in commands_queued ])
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE)
    process.communicate(commands.encode('utf-8'))

    json_file = json.dumps(timestamps)
    file_obj = open(SAVE_DIR_FORMAT.format(video_id) + "timestamps.json", "w")
    file_obj.write(json_file)
    os.remove(SAVE_DIR_FORMAT.format(video_id) + "temp.mp3")
    return timestamps

# test video: extract_audio('https://www.youtube.com/watch?v=zAGVQLHvwOY')
