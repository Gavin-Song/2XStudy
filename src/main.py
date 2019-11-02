import pytube
import os
import datetime
import json

video_url = 'https://www.youtube.com/watch?v=s4gBChg6AII'

yt = pytube.YouTube(video_url)
video = yt.streams.filter(progressive=True) \
  .order_by('resolution') \
  .desc() \
  .first()

video_data = yt.player_config_args.get('player_response').get('videoDetails')
video_id = video_data['videoId']
video_title = video_data['title']
video_author = video_data['author']
video_length_in_seconds = video_data['lengthSeconds']
video_length_formatted = str(datetime.timedelta(seconds=int(video_length_in_seconds)))

newpath = './saves/' + video_id
if not os.path.exists(newpath):
    os.makedirs(newpath)

video.download('./saves/' + video_id, 'temp')

meta_data = {'video_id': video_id, 'video_title': video_title, \
             'video_author': video_author, 'video_length': video_length_formatted}

output_file = 'meta_data.json'
with open('./saves/' + video_id + '/' + output_file, 'w+') as f:
  json.dump(meta_data, f)