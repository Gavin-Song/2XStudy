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
    # Pass the video in as a file (w/ ./saves/<video id>/<video name>.mp4); breaks is an array of dictionaries of video timestamp info
    def __init__(self,video,breaks):
        self.video = video
        self.breaks = breaks
        self.v = VideoFileClip(self.video) # VideoFileClip(<path of original video>)
        self.v = self.v.set_fps(int(round(self.v.fps))) # Rounding frame rate to a whole number to avoid edge-case errors.
    
    def get_video_length(self):
        return VideoFileClip(self.video).durationW

    def set_breaks(self,breaks):
        self.breaks = breaks

    # Splits video depending on the breaks and saves the video AND audio snippets.
    def break_apart_video(self,snippets_dir):
        video_name = self.video.replace(".mp4","")

        # Just in case the necessary path has not been created yet
        if not os.path.exists(snippets_dir):
            os.makedirs(snippets_dir)
        
        for i in range(len(self.breaks)):
            if i < len(self.breaks)-1:           
                temp2 = list(self.breaks[i+1].keys())
                time2 = float(temp2[0])
                temp1 = list(self.breaks[i].keys())
                time1 = float(temp1[0])

                snippet = self.v.subclip(time1,time2) # .subclip(<time1>,<time2>)
                if len(self.breaks[i][time1]) > 0 and len(self.breaks[i+1][time2]) == 0:
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_speech.mp4"),fps=8,verbose=False,logger=None)    # .write_videofile(<output_video_path>, optional parameters possible)
                else:
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_silence.mp4"),fps=8,verbose=False,logger=None)
            else:
                temp = list(self.breaks[i].keys())
                time = float(temp[0])

                snippet = self.v.subclip(time,self.v.duration) 
                if len(self.breaks[i][time]) > 0: 
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_speech.mp4"),fps=8,verbose=False,logger=None)
                else:
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_silence.mp4"),fps=8,verbose=False,logger=None)

    # Fast forwards new videos and combines the parts together.
    def abridge_video(self,sub_video_dir):
        video_name = self.video.replace(".mp4","")

        # Just in case the necessary has not been created yet
        if not os.path.exists(sub_video_dir):
            os.makedirs(sub_video_dir)

        abridged_parts = []     
        
        for i in range(len(self.breaks)):
            if i < len(self.breaks)-1:           
                temp2 = list(self.breaks[i+1].keys())
                time2 = float(temp2[0])
                temp1 = list(self.breaks[i].keys())
                time1 = float(temp1[0])

                snippet = self.v.subclip(time1,time2) # .subclip(<time1>,<time2>)
                if len(self.breaks[i][time1]) > 0 and len(self.breaks[i+1][time2]) == 0:
                    abridged_parts.append(snippet)  # Don't speed up speech parts.
                else:
                    abridged_parts.append(snippet.speedx(factor=5)) # Speed up the silent parts by 5 times.
                snippet.reader.close()
                snippet.audio.reader.close_proc()
            else:
                temp = list(self.breaks[i].keys())
                time = float(temp[0])

                snippet = self.v.subclip(time,self.v.duration) 
                if len(self.breaks[i][time]) > 0:
                    abridged_parts.append(snippet)  # Don't speed up speech parts.
                else:
                    abridged_parts.append(snippet.speedx(factor=5)) # Speed up the silent parts by 5 times.
                snippet.reader.close()
                snippet.audio.reader.close_proc()

        abridged_clip = concatenate_videoclips(abridged_parts)  
        abridged_clip.write_videofile(self.helper_merge_directories(sub_video_dir,video_name+"_abridged.mp4"),verbose=False,logger=None)

    # Helper method to combine original video file directory with new video file directory
    # Note: use with caution: pass in the directories to combine with the order dependency imposed by argument order
    def helper_merge_directories(self,from_d,to_d):
        combination = ""
        longer = from_d if len(from_d) > len(to_d) else to_d
        shorter = from_d if len(from_d) < len(to_d) else to_d
        for i in range(len(longer)):
            if i >= len(shorter):
                combination += to_d[i:]
                break
            elif from_d[i] != to_d[i]:
                combination += from_d[i:] + to_d[i:]
                break
            else:
                combination += from_d[i]
        return combination