import cv2
import numpy as np
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
    # Pass the video in as a file (.mp4); breaks is an array of dictionaries of video break info
    def __init__(self,video,breaks):
        self.video = video
        self.breaks = breaks
        cap = cv2.VideoCapture(video) 

    # Splits video depending on the breaks and saves the video AND audio snippets.
    def break_apart_video(self):
        saved_video_parts = []
        saved_audio_parts = []
        for i in range(len(self.breaks)-1):           
            temp2 = list(self.breaks[i+1].keys())
            time2 = temp2[0]
            temp1 = list(self.breaks[i].keys())
            time1 = temp1[0]

            saved_video_parts.append(cap["""from time1 to time2"""])   # Append from the first time to the second time

        video_snippets_path = "./saves/video_snippets/"
        for part in saved_video_parts:
            if not os.path.exists(video_snippets_path)
                os.mkdir(video_snippets_path)
            # f = open(video_snippets_path + <name_of_part>.mp4, "a")
            # f.close()

        audio_snippets_path = "./saves/audio_snippets/"
        for part in saved_audio_parts:
            if not os.path.exists(audio_snippets_path)
                os.mkdir(audio_snippets_path)
            # f = open(audio_snippets_path + <name_of_part>.mp3, "a")
            # f.close()

    # Fast forwards new videos and combines the parts together.
    def abridge_video(self,sub_video_dir):
        abridged_parts = []     
        for i in range(len(self.breaks)-1):
            temp2 = list(self.breaks[i+1].keys())
            time2 = temp2[0]
            temp1 = list(self.breaks[i].keys())
            time1 = temp1[0]

            if self.breaks[i][time1] == "speech" and self.breaks[i+1][time2] == "silence":
                abridged_parts.append(cap["""from time1 to time2"""])
            elif self.breaks[i][time1] == "silence" and self.breaks[i+1][time2] == "speech":
                abridged_parts.append(cap["""from time1 to time2, speed up by 5x"""])

        # abridged = 
        for part in abridged_parts:
            # abridged.add(part)
        
        # f = open(sub_video_dir + <name_of_part>.mp4, "a")
        # f.close()

    # Call this method to empty the resources used for creating the abridged video.
    def close_video(self):
        cap.release()