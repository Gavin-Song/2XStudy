# 2XStudy - About Us and The Project

## Inspired and Created @ [HackRPI](http://www.hackrpi.com/) 

**Important:** See more information about this project [here](https://github.com/Gavin-Song/2XStudy). 

## 2XStudy - In a Nutshell
2XStudy is a web-based application that allows learners and educators to extract the most useful and productive information from any YouTube videos (educational ones for ex.). The user simply goes to our website (with a custom domain), enters in a YouTube video url of his/her choice, and sees an abridged edition of the inputted video, with all non-relevant parts (silent sections) of the video omitted. Video snippets paired with audio transcriptions from the most relevant parts of the video are then generated right below the url box and shortened video. All video processing occurs behind the scenes in a server. Used with education YouTube videos, such as those found on Khan Academy, 2XStudy promises to give students a much more efficient educational experience and teachers an effective tool to teach with videos.

## What We Used
**Front-end:** [JavaScript](https://www.javascript.com/), [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML), & [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) 

**Back-end:** [Node.js](https://nodejs.org/en/), [Python](https://www.python.org/), Python libraries ([moviepy] (https://zulko.github.io/moviepy/), [pytube](https://github.com/nficano/pytube), [ffmpeg](https://pypi.org/project/ffmpeg-python/))

**IDEs:** [Visual Studio Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/), [Spyder](https://www.spyder-ide.org/)

**Application Framework for Server:** [Express](https://expressjs.com/), [Google](https://cloud.google.com/)

## Step-By-Step of How App Functions
**1.** Take in user input, in the form of a YouTube video url, from the main website.

**2.** Download the YouTube video and switch video quality to 720p (1280x720) if above 720p to enhance performance.

**3.** Save the video file onto a hidden repository within a server hosted on the Google Cloud. 

**4.** Identify where the relevant (speech) and non-relevant (silent) portions of the video are. Store that information in a list of dictionaries, which each dictionary key the time (in sec) since the video begun and the value the relevancy status.

**5.** Split video into chunks based on the timestamp times and save each video snippet into a subdirectory on the server. These videos will be used for the generated transcription information.

**6.** Create an abridged video version of the original by speeding up the non-relevant portions by 5x.

**7.** Extract audio segments from the video that are relevant (again, non-silent). Save those segments into another subdirectory on the server.

**8.** Transcribe those audio segments into proper English. 

**9.** Display extracted information onto the website below the bar for entering the YouTube url in this order: abridged video and video snippets and corresponding audio transcription as text.

## What We Learned
Our main takeaways could use an essay-long description, discussion, and explanation. However, I'm sure that you will be bored by that, so here it is in just a few bullet points:

* **Scalability:** Scalability is extremely important. Although our newly-forged specialized video transcription and condensation tool implementation, which could be put into the official Coding&&Community app in the future, was seemingly reasonable and step-by-step, all parts of the process took longer than expected. Figuring out the standards and priorities for the application was paramount in our ability to complete it in the time alloted.

* **Library/Module Use and Responsibility:** Be careful about which modules you use and how to use them. Especially with the case of back-end operations, many of which involved splicing, rejoining, and modifying parts of the downloaded video, additional code-based resources had to be utilized to avoid needlessly low-level programming. We wanted to keep back-end development down to a single programming language, which required the use of powe rful libraries. Although their functionality enabled us to focus on higher-level coding, many of them came with a host of edge-case bugs. It is vital to do good research into a programming library before importing it into a project.

* **Branch If Collaborating on GitHub:** If you are using GitHub as a means of cloud-based source control and collaboration, always branch contributions between each developer or team of developers. With each team member in our group assigned specific software development tasks throughout the process - front-end and back-end alike - creating individual personalized branches apart from the master one prevented merge-conflict hassles, accidental code overwritting, and deletion of code files. Removing source control concern and time spent with collaborators unintentionally interrupting their own codebases enabled us to finish this project in time. 

## Challenges
Similarly to the previous section, we could ramble on and on about the challenges we faced. Let's not do that and cut to the chase:

* **Holes Between What We Know and What We Need to Do:** Although our idea was polished, refined, and clear-cut, executing the implementation of certain front-end and back-end processes were out of scope of our current programming experience and knowledge. We had to scour through pages of online documentation to extract necessary classes and functions to employ to plug in those gaps of knowledge and complete our programs.

* **Errors, errors, and errors:** With a good number of different operations, libraries, and the front-end back-end split, we encountered a number of bugs with inner and external dependencies throughout the development process. Inner dependency errors originate from accidentally misinterpreting the correct usage of modules, while external dependency errors occurred due to edge-case reliability issues with the modules themselves. While we did not directly calculate the following, we likely spent half of our time resolving coding errors. Recall the above discussion on **Library/Module Use and Responsibility** as a majority of the errors came with using third-party and public resources.

* **Efficiency:** After correctly implementing error-free programs into our app development, then there was the issue with the runtime of processing the downloaded video (mostly back-end). Video processing is inherently a resource-intensive operation, and as such, bottlenecked the performance of our application. At best, we managed to improve the module implementation side of video processing of the video processing to O(n), with n denoting the number of timestamps used to extract video statistics. Reducing video downloading quality to 720p if above 720p helped as well. However, the work done by the module itself still hindered performance, regardless of whether we used moviepy or ffmpeg.

### Copyright © 2019 by 2XStudy & TheHumbleOnes (dev team). All rights reserved. 
