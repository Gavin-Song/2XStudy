# 2XStudy
You can find 2XStudy [here](https://two-x-study.herokuapp.com/index.html). As this is a RPI hackathon project, you can find the official devpost [here](https://devpost.com/software/2xstudy-yhl6w0). You can find the team repository [here](https://github.com/Gavin-Song/2XStudy). 

2XStudy is a web application that can improve the delivery of content from YouTube videos for learners and educators. To use it, enter the url corresponding to a YouTube video into the input bar, click "Convert", and wait for the application to process the video. The intended result is an abridged edition of the video, with all non-relevant parts (silent sections) of the video omitted. Video snippets paired with audio transcriptions from the most relevant parts of the video are generated right below the url box and shortened video. All video processing occurs behind the scenes in a server. 

## Technologies
**Front-end:** [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML), [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS), and [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/) 

**Back-end:** [Node.js](https://nodejs.org/en/), [Express.js](https://expressjs.com/), [Python](https://www.python.org/), Python libraries ([MoviePy](https://zulko.github.io/moviepy/), [pytube](https://github.com/nficano/pytube), [ffmpeg-python](https://pypi.org/project/ffmpeg-python/))

**IDEs:** [Visual Studio Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/), [Spyder](https://www.spyder-ide.org/)

**Server Hosting:** [Google Cloud](https://cloud.google.com/)

## How the App Functions
**1.** 2XStudy takes in user input, in the form of a YouTube video url, from the main website.

**2.** The app downloads the YouTube video and switch video quality to **720p (1280x720)** if **above 720p** to enhance video processing performance.

**3.** 2XStudy saves the video file onto a hidden repository within a server hosted on the Google Cloud. 

**4.** The app identifies where the relevant (speech) and non-relevant (silent) portions of the video are and stores that information in a list of dictionaries, which each dictionary key the time (in sec) since the video begun and the value the relevancy status.

**5.** 2XStudy splits the video into video snippets based on the timestamp times and saves each video snippet into a subdirectory on the server. The video snippets are used to generate the transcriptions.

**6.** The app creates an abridged version of the original video by speeding up the non-relevant portions of the video by 5x and saves the abridged video onto root directory on the server.

**7.** 2XStudy extracts audio segments from the video that are relevant (speech) and saves those segments into another subdirectory on the server.

**8.** The app transcribes those audio segments into English. 

**9.** 2XStudy displays the video and audio transcriptions below the input bar in this order: abridged video, video snippets, and corresponding audio transcriptions.

## What We Learned
* **Scalability:** Scalability is extremely important. Although our newly-forged specialized video transcription and condensation tool implementation was seemingly straightforwards, all parts of the process took longer than expected. Figuring out the standards and priorities for the application was paramount in our ability to complete it in the time alloted.

* **Library/Module Use and Responsibility:** Be careful about which modules you use and how to use them. Especially with the case of back-end operations, many of which involved splicing, rejoining, and modifying parts of the downloaded video, additional code-based resources had to be utilized to avoid needless low-level programming. We wanted to keep back-end development down to a single programming language, which required the use of powerful libraries. Although their functionality enabled us to focus on higher-level coding, many of them came with a host of edge-case bugs. It is vital to do good research into a programming library before importing it into a project.

* **Branch If Collaborating on GitHub:** If you are using GitHub as a means of cloud-based source control and collaboration, always branch contributions between each developer or team of developers. With each team member in our group assigned specific software development tasks throughout the process - front-end and back-end alike - creating individual personalized branches apart from the master one prevented merge-conflict hassles, accidental code overwritting, and deletion of code files. Removing source control concern and time spent with collaborators unintentionally interrupting their own codebases enabled us to finish this project in time. 

## Challenges
* **Holes Between What We Know and What We Need to Do:** Although our idea was polished, refined, and clear-cut, executing the implementation of certain front-end and back-end processes were out of scope of our current programming experience and knowledge. We had to scour through pages of online documentation to extract necessary classes and functions to employ to plug in those gaps of knowledge and complete our programs.

* **Errors, errors, and errors:** With a good number of different operations, libraries, and the front-end back-end split, we encountered a number of bugs with inner and external dependencies throughout the development process. Inner dependency errors originate from accidentally misinterpreting the correct usage of modules, while external dependency errors occurred due to edge-case reliability issues with the modules themselves. While we did not directly calculate the following, we likely spent half of our time resolving coding errors. Recall the above discussion on **Library/Module Use and Responsibility** as a majority of the errors came with using third-party and public resources.

* **Efficiency:** After correctly implementing error-free programs into our app development, then there was the issue with the runtime of processing the downloaded video (mostly back-end). Video processing is inherently a resource-intensive operation, and as such, bottlenecked the performance of our application. At best, we managed to improve the module implementation side of video processing of the video processing to O(n), with n denoting the number of timestamps used to extract video statistics. Reducing video downloading quality to 720p if above 720p helped as well. However, the work done by the module itself still hindered performance, regardless of whether we used MoviePy or ffmpeg.

### © Copyright 2019 2XStudy & TheHumbleOnes (dev team)
