"""
This program tests the CreateAbridgedVideo class used for encapsulating 
2XStudy back-end video splitting and abridging features.
"""

from process_video import CreateAbridgedVideo

# Main Program
if __name__ == "__main__":
    file_name = input("What video would you like to experiment with? ")
    print(file_name)

    print("Check the saves folder and the corresponding files within the saves folder to see the impeccable results!")

#    print(merge_directories("./saves/snippets/","./saves/test1_part1_speech.mp4"))
    breaks = [{0:""},{5:"bbb"},{10:""},{15:"bbb"},{20:""},{25:"bbb"},{30:""},{35:"bbb"},{40:""},{45:"bbb"},{50:""},{55:"bbb"},{60:""},{65:"bbb"},{70:""},{75:"bbb"},{80:""},{85:"bbb"}]
    tool = CreateAbridgedVideo("./saves/"+file_name,breaks)
    tool.break_apart_video("./saves/snippets/")
    tool.abridge_video("./saves/")