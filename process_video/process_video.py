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
    subclips = []

    # Pass the video in as a file (w/ ./saves/<video id>/<video name>.mp4); breaks is an array of dictionaries of video timestamp info
    def __init__(self,video,breaks):
        self.video = video
        self.breaks = breaks
    
    # Splits video depending on the breaks and saves the video AND audio snippets.
    def break_apart_video(self,snippets_dir):
        video_name = self.video.replace(".mp4","")

        # Just in case the necessary path has not been created yet
        if not os.path.exists(snippets_dir):
            os.makedirs(snippets_dir)
        
        v = VideoFileClip(self.video) # VideoFileClip(<path of original video>)
        for i in range(len(self.breaks)):
            if i < len(self.breaks)-1:           
                temp2 = list(self.breaks[i+1].keys())
                time2 = temp2[0]
                temp1 = list(self.breaks[i].keys())
                time1 = temp1[0]

                snippet = v.subclip(time1,time2) # .subclip(<time1>,<time2>)
                if len(self.breaks[i][time1]) > 0 and len(self.breaks[i+1][time2]) == 0:
                    self.subclips.append({snippet:"speech"})
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_speech.mp4"),verbose=False,logger=None)    # .write_videofile(<output_video_path>, optional parameters possible)
                else:
                    self.subclips.append({snippet:"silence"})
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_silence.mp4"),verbose=False,logger=None)
                    
            else:
                temp = list(self.breaks[i].keys())
                time = temp[0]

                snippet = v.subclip(time,v.duration) 
                if len(self.breaks[i][time]) > 0: 
                    self.subclips.append({snippet:"speech"})
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_speech.mp4"),verbose=False,logger=None)
                else:
                    self.subclips.append({snippet:"silence"})
                    snippet.write_videofile(self.helper_merge_directories(snippets_dir,video_name+"_part"+str(i+1)+"_silence.mp4"),verbose=False,logger=None)

    # Fast forwards new videos and combines the parts together.
    def abridge_video(self,sub_video_dir):
        video_name = self.video.replace(".mp4","")

        # Just in case the necessary has not been created yet
        if not os.path.exists(sub_video_dir):
            os.makedirs(sub_video_dir)

        abridged_parts = []     
        
        for i in range(len(self.subclips)):
            temp = list(self.subclips[i].values())
            status = temp[0]

            temp = list(self.subclips[i].keys())
            video_part = temp[0]
            if status == "silence":
                abridged_parts.append(video_part.speedx(factor=5))  # Speed up silent parts by 5x
            else:
                abridged_parts.append(video_part)    # Leave speech parts as they already are

        abridged_clip = concatenate_videoclips(abridged_parts)
        # abridged_clip = abridged_parts[0]
        # for i in range(1,len(abridged_parts)):
        #    abridged_clip = concatenate_videoclips([abridged_clip,abridged_parts[i]])    
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