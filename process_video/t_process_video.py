"""
This program tests the CreateAbridgedVideo class used for encapsulating 
2XStudy back-end video splitting and abridging features.
"""

from process_video import CreateAbridgedVideo
import time

# Main Program
if __name__ == "__main__":
    file_name = input("What video would you like to experiment with? ")
    print(file_name)

    print("Check the saves folder and the corresponding files within the saves folder to see the impeccable results!")

    # The actual breaks data will NOT necessarily look exactly like the following below,
    # which was used for testing purposes.
    breaks = [{0:""},{5:"bbb"},{10:""},{15:"bbb"},{20:""},{25:"bbb"},{30:""},{35:"bbb"},{40:""},{45:"bbb"},{50:""},{55:"bbb"},{60:""},{65:"bbb"},{70:""},{75:"bbb"},{80:""},{85:"bbb"}]
#    breaks = [{0:""},{2:"bsdf"},{5:""}]
    start_time = time.time()
    tool = CreateAbridgedVideo("./saves/"+file_name,breaks) # Assume ./saves/ folder already exists
    tool.break_apart_video("./saves/snippets/")
    tool.abridge_video("./saves/")
    print("The processing took {0:.2f} seconds.".format(time.time()-start_time))