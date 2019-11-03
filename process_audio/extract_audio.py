# Yash Mistri

from pytube import YouTube
from pydub import AudioSegment
from pydub.silence import split_on_silence
import json

'''
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
'''
def extract_audio(url):
    # download audio from Youtube video given by url
    video = YouTube(url) 
    stream = video.streams.filter(only_audio=True, file_extension='mp4').first()
    
    # get captions
    caption = video.captions.get_by_language_code('en')
    caption_list = caption.generate_srt_captions().splitlines()
    
    stream.download()
    timestamps = [] #list of dictionaries- time: text
    num = 0 # for labeling exported segments
    
    timestamps.append({0.0 : ""})
    
    # load audio from file downloaded above
    audio = AudioSegment.from_file(stream.title + ".mp4", "mp4")
    for i in range(1, len(caption_list), 4):
        sub = caption_list[i].split(' --> ')    # [hhh:mmm:ss,uuu, hhh:mmm:ss,uuu]
        
        time = []
        time_var = [0.0,0.0]

        # parse times from string
        for j in range(2):
            time = sub[0].split(',')                    # [hhh:mmm:ss, uuu]
            time_var[j] += float(time[1]) * .001       # milliseconds
            time = time[0].split(':')                      # split h, m, s
            time_var[j] += float(time[0]) * 360 + float(time[1]) * 60 + float(time[2])
        
        # create entries in dictionary 'timestamps'
        timestamps.append({time_var[0]-0.01 : caption_list[i+1]})
        timestamps.append({time_var[1] : ""})

    
    # export audio clips
    prev = 0.0
    for val in timestamps:
        keys = list(val.keys())
        if prev != keys[0]:
            audio_segment = audio[prev*1000:keys[0]*1000]
            audio_segment.export("l{}".format(num), format="mp4")
            num += 1
        prev = keys[0]

    json_file = json.dumps(timestamps)
    file_obj = open("timestamps.json", "w")
    file_obj.write(json_file)

# test video: extract_audio('https://www.youtube.com/watch?v=zAGVQLHvwOY')
