"""
This program tests the CreateAbridgedVideo class used for encapsulating 
2XStudy back-end video splitting and abridging features.
"""

from process_video import CreateAbridgedVideo

# Main Program
if __name__ == "__main__":
#    print(merge_directories("./saves/snippets/","./saves/test1_part1_speech.mp4"))
    breaks = [{0:"blahblahblah"},{0.5:""},{1:"blahblahblah"},{1.5:""},{2.0:"blahblahblah"},{2.5:""},{3.0:"blahblahblah"},{3.5:""},{4.0:"blahblahblah"},{4.5:""},{5.0:"blahblahblah"},{5.5:""},{6.0:"blahblahblah"},{6.5:""},{7.0:"blahblahblah"},{7.5:""}]
    tool = CreateAbridgedVideo("./saves/test1.mp4",breaks)

    tool.break_apart_video("./saves/snippets/")
    tool.abridge_video("./saves/")