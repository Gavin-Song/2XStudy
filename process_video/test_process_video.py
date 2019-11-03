"""
This program tests the CreateAbridgedVideo class used for encapsulating 
2XStudy back-end video splitting and abridging features.
"""

from process_video import CreateAbridgedVideo

# Main Program
if __name__ == "__main__":
    file_name = input("What video would you like to experiment with? ")
    print(file_name)
    alternating_parts = input("How many parts would you like to split this video into? ")
    print(alternating_parts)
    alternating_parts = int(alternating_parts)

    print("Check the saves folder and the corresponding files within the saves folder to see the impeccable results!")

#    print(merge_directories("./saves/snippets/","./saves/test1_part1_speech.mp4"))
    breaks = []
    tool = CreateAbridgedVideo("./saves/"+file_name,breaks)
    video_length_factor = tool.get_video_length()/alternating_parts
    speech = True
    for i in range(alternating_parts):
        status = ""
        if speech:
            status = "blahblahblah"
        breaks.append({i*video_length_factor:status})
        speech = not speech

    tool.set_breaks(breaks)
    tool.break_apart_video("./saves/snippets/")
    tool.abridge_video("./saves/")