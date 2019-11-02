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
        saved_video_parts = []  # also has distinguishing measure to denote speech and silent parts
        saved_audio_parts = []
        for i in range(len(self.breaks):
            if i < len(self.breaks)-1:           
                temp2 = list(self.breaks[i+1].keys())
                time2 = temp2[0]
                temp1 = list(self.breaks[i].keys())
                time1 = temp1[0]

                if self.breaks[i][time1] == "speech" and self.breaks[i+1][time2] == "silence": 
                    saved_video_parts.append({cap["""from time1 to time2"""]: "speech"})   
                    saved_audio_parts.append({"""audio of video from time1 to time2"""})
                else:
                    saved_video_parts.append({cap["""from time1 to time2"""]: "silence"})  
            else:
                temp = list(self.breaks[i].keys())
                time = temp[0]

                if self.breaks[i][time] == "speech":
                    saved_video_parts.append({cap["""from time to end of video"""]: "speech"})   
                    saved_audio_parts.append({"""audio of video from time to end of video"""})
                else:
                    saved_video_parts.append({cap["""from time to end of video"""]: "silence"})  

        video_snippets_path = "./saves/video_snippets/"
        for part in saved_video_parts:
            if not os.path.exists(video_snippets_path)
                os.mkdir(video_snippets_path)
            temp = list(part.values())
            status = temp[0]
            if status == "speech":
                # f = open(video_snippets_path + <name_of_part>_speech.mp4, "a")
                # f.close()
            else:
                # f = open(video_snippets_path + <name_of_part>_silence.mp4, "a")
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
        for i in range(len(self.breaks)):
            if i < len(self.breaks)-1:
                temp2 = list(self.breaks[i+1].keys())
                time2 = temp2[0]
                temp1 = list(self.breaks[i].keys())
                time1 = temp1[0]

                if self.breaks[i][time1] == "speech" and self.breaks[i+1][time2] == "silence":
                    abridged_parts.append(cap["""from time1 to time2"""])
                elif self.breaks[i][time1] == "silence" and self.breaks[i+1][time2] == "speech":
                    abridged_parts.append(cap["""from time1 to time2, speed up by 5x"""])
            else:
                temp = list(self.breaks[i].keys())
                time = temp[0]

                if self.breaks[i][time] == "speech":
                    abridged_parts.append(cap["""from time to end of video"""])
                else:
                    abridged_parts.append(cap["""from time to end of video, speed up by 5x"""])

        # abridged_video = 
        for part in abridged_parts:
            # abridged_video.add(part)
        
        # f = open(sub_video_dir + <name_of_abridged_video>.mp4, "a")
        # f.close()

    # Call this method to empty the resources used for creating the abridged video.
    def close_video(self):
        cap.release()