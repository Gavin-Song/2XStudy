from subprocess import Popen, PIPE
import os

FFMPEG_DIR = "./process_video/ffmpeg/ffmpeg"
CUT_DIR_BASE = "./public/saves/{}/video_snippets/"
CUT_DIR = ""
NO_LOG = ["-hide_banner", "-loglevel", "panic"]
NO_LOG_STR = "-hide_banner -loglevel panic"

TEMP_FILE = "temp2.mp4"
TEMP_TXT = "temp.txt"
PADDING = 1


def set_cut_dir(video_id):
    """
    Sets cut dir to video id
    :param video_id
    """
    global CUT_DIR
    CUT_DIR = CUT_DIR_BASE.format(video_id)


def run_process(command, args):
    """
    Runs a command with arguments, supplied
    as an array (ie ["-i", "myfile.mp4"]). Double
    quotes in arguments must be omitted (strings will
    be auto quoted and adding quotes will cause duplicate
    quotes)

    :param: command
    :param: args
    :return: stdout
    :raises: Exception if stderr occurs
    """
    args = [command] + args + NO_LOG
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        raise Exception(stderr)
    return stdout


def rename_temp_file(video):
    """
    Renames TEMP_FILE to replace video
    :param video: File to replace
    """
    os.remove(video)
    os.rename(TEMP_FILE, video)


def format_time(seconds):
    """
    Formats a time in seconds
    :param seconds:
    :return: Time formatted as hh:mm:ss
    """
    format_zero = lambda x: str(int(x)) if int(x) > 9 else "0{}".format(int(x))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{}:{}:{}".format(format_zero(h), format_zero(m), format_zero(s))


def cut_video(video, out, start, end):
    """
    Cuts a video file in place
    :param video: Path to video to cut
    :param out:   Path to out file
    :param start: Start time since 0:00 in seconds
    :param end:   End time since 0:00 in seconds
    :return:      None
    """
    diff = format_time(end - start)
    start = format_time(start)
    run_process(FFMPEG_DIR, [
        "-ss", start, "-i", video, "-t", diff,
        "-c:v", "libx264", "-crf", "18", "-c:a", "copy", # Copy and re-encode
         out, "-y"
    ])


def fast_forward_video(video, factor=5):
    """
    Fast forwards a video file in place
    :param video:  Path to file to cut
    :param factor: Factor to speed up by
    :return:
    """
    if factor < 1:
        raise Exception("Factor cannot be less than 1")

    # We can only speed up audio by at most a factor of 2 so we
    # need to string multiple together
    m, atempo = float(factor), []
    while m > 2:
        atempo.append("atempo=2.0")
        m = m / 2
    if m > 1:
        atempo.append("atempo={}".format(m))
    atempo = ",".join(atempo)

    run_process(FFMPEG_DIR, ["-y", "-i", video, "-filter_complex",
                             '[0:v]setpts={}*PTS[v];[0:a]{}[a]'.format(1.0 / factor, atempo),
                             "-map", '[v]', "-map", '[a]', TEMP_FILE])
    rename_temp_file(video)


def concat(videos, out):
    """
    Concats array of video directories to output
    :param videos:
    :param out:
    """
    with open(TEMP_TXT, "w") as f:
        f.write("\n".join(["file '{}'".format(p) for p in videos]))
    run_process(FFMPEG_DIR, ["-y", "-f", "concat", "-safe", "0", "-i", TEMP_TXT, "-c", "copy", out])
    os.remove(TEMP_TXT)


def process_videos(video, breaks):
    """
    Main process function
    :param video: Path to raw video
    :param breaks: Array of timestamps of breaks:
                    [{ start_timestamp : transcription="" if silent }, ...]
    """
    breaks.append({999999: ""})  # Dummy end
    to_delete = []

    for i in range(len(breaks) - 1):
        current_break = breaks[i]
        current_file_name = CUT_DIR + "{}.mp4".format(i)

        start, end = list(breaks[i].keys())[0], list(breaks[i + 1].keys())[0]
        cut_video(video, current_file_name, start, end)

        # if len(current_break[start]) == 0:  # Silence
            # fast_forward_video(current_file_name)
            # to_delete.append(current_file_name)

    # concat([CUT_DIR + "{}.mp4".format(i) for i in range(len(breaks) - 1)], "abridged.mp4")
    # for f in to_delete:
    #     os.remove(f)
