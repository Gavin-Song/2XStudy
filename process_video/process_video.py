# import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

""" 
This class is specialized for the 2XStudy back-end operations
of breaking apart the video into parts depending on the location
of the breaks in the video and combining those parts into an
abridged video to be saved onto the user's computer. It also
saves the breaks and non-break sections of the video into separate
files for display on the generated webpage transcription.
"""
class CreateAbridgedVideo:
    # Pass the video in as a file (w/ ./saves/<video id>/<video name>.mp4); breaks is an array of dictionaries of video break info
    def __init__(self,video,breaks):
        self.video = video
        self.breaks = breaks

    # Splits video depending on the breaks and saves the video AND audio snippets.
    def break_apart_video(self,snippets_dir):
        video_name = self.video-".mp4"

        # Just in case the necessary path has not been created yet
        if not os.path.exists(snippets_path):
            os.makedirs(snippets_path)

        for i in range(len(self.breaks)):
            if i < len(self.breaks)-1:           
                temp2 = list(self.breaks[i+1].keys())
                time2 = temp2[0]
                temp1 = list(self.breaks[i].keys())
                time1 = temp1[0]

                with VideoFileClip(video) as v: # VideoFileClip(<path of original video>)
                    snippet = v.subclip(time1,time2) # .subclip(<time1>,<time2>)
                    if self.breaks[i][time1] == "speech" and self.breaks[i+1][time2] == "silence": 
                        snippet.write_videofile(snippets_dir+video_name+"_part"+str(i+1)+"_speech.mp4")    # .write_videofile(<output_video_path>, optional parameters possible)
                    else:
                        snippet.write_videofile(snippets_dir+video_name+"_part"+str(i+1)+"_silence.mp4")
            else:
                temp = list(self.breaks[i].keys())
                time = temp[0]

                with VideoFileClip(video) as v: 
                    snippet = v.subclip(time,v.duration) 
                    if self.breaks[i][time] == "speech": 
                        snippet.write_videofile(snippets_dir+video_name+"_part"+str(i+1)+"_speech.mp4")
                    else:
                        snippet.write_videofile(snippets_dir+video_name+"_part"+str(i+1)+"_silence.mp4")

    # Fast forwards new videos and combines the parts together.
    def abridge_video(self,sub_video_dir):
        video_name = self.video-".mp4"

        # Just in case the necessary has not been created yet
        if not os.path.exists(sub_video_dir):
            os.makedirs(sub_video_dir)

        abridged_parts = []     
        for i in range(len(self.breaks)):
            if i < len(self.breaks)-1:
                temp2 = list(self.breaks[i+1].keys())
                time2 = temp2[0]
                temp1 = list(self.breaks[i].keys())
                time1 = temp1[0]

                with VideoFileClip(video) as v: # VideoFileClip(<path of original video>)
                    snippet = v.subclip(time1,time2) # .subclip(<time1>,<time2>)
                    if self.breaks[i][time1] == "speech" and self.breaks[i+1][time2] == "silence":
                        abridged_parts.append(snippet)
                    elif self.breaks[i][time1] == "silence" and self.breaks[i+1][time2] == "speech":
                        snippet.fps *= 5  # Speed up silent parts by 5x
                        abridged_parts.append(snippet)   
            else:
                temp = list(self.breaks[i].keys())
                time = temp[0]

                with VideoFileClip(video) as v: # VideoFileClip(<path of original video>)
                    snippet = v.subclip(time,v.duration) # .subclip(<time1>,<time2>)
                    if self.breaks[i][time] == "speech":
                        abridged_parts.append(snippet)
                    else:
                        snippet.fps *= 5  # Speed up silent parts by 5x
                        abridged_parts.append(snippet) 

        abridged_clip = concatenate_videoclips(abridged_parts)    
        abridged_clip.write_videofile(sub_video_dir+video_name+"_abridged.mp4")

    # Call this method to empty the resources used for creating the abridged video.
    def close_video(self):
        cap.release()