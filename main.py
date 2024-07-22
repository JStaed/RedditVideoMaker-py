import praw
import boto3
from contextlib import closing
import os
import sys
from moviepy.editor import concatenate_audioclips, CompositeAudioClip, AudioFileClip, VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import random as rand
import math
from scriptreader import synthesize_script


def generate_audio_long():
    try:
        mode = int(input("Subreddit/Direct Link [1/2]: "))
    except ValueError:
        print("Input must be an integer")
        return
    # Read-only instance
    reddit_read_only = praw.Reddit(
        client_id="0D5tjk8C1Rl9O_tYErEN_g",
        client_secret="IhFL7W-TV-toy4hyHZ8HCDFbzurlTA",
        user_agent="JStaed Scraper"
    )
    if mode == 1:
        subName = input("Subreddit Name: r/")
        try:
            postCount = int(input("Number of Clips: "))
        except ValueError:
            print("Input must be an integer")
            return

        subreddit = reddit_read_only.subreddit(subName)

        posts = subreddit.top(time_filter="week", limit=postCount)
        os.mkdir(subName)
        script = ""
        x = 0
        for post in posts:
            content = str.strip(post.title, "\n") + "\n" + str.strip(post.selftext, "\n")
            script += content + "\n\n"
            x += 1
        with open(f"{subName}\\script.txt", "w") as f:
            f.write(script)
    elif mode == 2:
        postID = input("Post ID: ")
        posts = [reddit_read_only.submission(id=postID)]
        os.mkdir(postID)
        script = ""
        x = 0
        for post in posts:
            content = str.strip(post.title, "\n") + "\n" + str.strip(post.selftext, "\n")
            script += content + "\n\n"
            x += 1
        with open(f"{postID}\\script.txt", "w") as f:
            f.write(script)
        synthesize_script(postID)


def generate_audio():
    try:
        mode = int(input("Subreddit/Direct Link [1/2]: "))
    except ValueError:
        print("Input must be an integer")
        return
    # Read-only instance
    reddit_read_only = praw.Reddit(
        client_id="0D5tjk8C1Rl9O_tYErEN_g",
        client_secret="IhFL7W-TV-toy4hyHZ8HCDFbzurlTA",
        user_agent="JStaed Scraper"
    )
    session = boto3.session.Session()
    polly = session.client("polly")
    if mode == 1:
        subName = input("Subreddit Name: r/")
        try:
            postCount = int(input("Number of Clips: "))
        except ValueError:
            print("Input must be an integer")
            return

        subreddit = reddit_read_only.subreddit(subName)

        posts = subreddit.top(time_filter="week", limit=postCount)
        os.mkdir(subName)
        script = ""
        x = 0
        for post in posts:
            content = str.strip(post.title, "\n") + "\n" + str.strip(post.selftext, "\n")
            script += content + "\n\n"
            response = polly.synthesize_speech(Text=content, VoiceId="Matthew", OutputFormat="mp3", Engine="generative")
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join(subName, f"speech{x}.mp3")

                    try:
                        # Open a file for writing the output as a binary stream
                        with open(output, "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        # Could not write to file, exit gracefully
                        print(error)
                        sys.exit(-1)
            else:
                print("No AudioStream")
            x += 1
        with open(f"{subName}\\script.txt", "w") as f:
            f.write(script)
    elif mode == 2:
        postID = input("Post ID: ")
        posts = [reddit_read_only.submission(id=postID)]
        script = ""
        x = 0
        for post in posts:
            subName = post.title
            content = str.strip(post.title, "\n") + "\n" + str.strip(post.selftext, "\n")
            script += content + "\n\n"
            response = polly.synthesize_speech(Text=content, VoiceId="Matthew", OutputFormat="mp3", Engine="generative")
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join(subName, f"speech{x}.mp3")

                    try:
                        # Open a file for writing the output as a binary stream
                        with open(output, "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        # Could not write to file, exit gracefully
                        print(error)
                        sys.exit(-1)
            else:
                print("No AudioStream")
            x += 1
        with open(f"{subName}\\script.txt", "w") as f:
            f.write(script)


def combine_audio():
    audioDir = input("Project Directory: ")
    try:
        f = open(f"{audioDir}\\script.txt", 'r')
        f.close()
    except FileNotFoundError:
        print(f"{audioDir} is not a valid directory or does not contain a script file.")
        print()
        return

    audioClips = []
    x = 0
    while True:
        try:
            f = open(f"{audioDir}\\speech{x}.mp3")
            f.close()
            audioClips.append(AudioFileClip(f"{audioDir}\\speech{x}.mp3"))
            audioClips.append(AudioFileClip(f"pause.mp3"))
            x += 1
        except FileNotFoundError:
            break
    final = concatenate_audioclips(audioClips)
    final.write_audiofile(f"{audioDir}\\final.mp3")


def create_video():
    audioDir = input("Project Directory: ")
    videoID = input("Video ID: ")
    try:
        mode = int(input("Individual Videos/Full Video [1/2]: "))
    except ValueError:
        print("Input must be an integer")
        return
    if mode == 1:
        try:
            f = open(f"{audioDir}\\speech.mp3")
            f.close()
        except FileNotFoundError:
            print(f"Audio Not Found in {audioDir}.")
            print()
            return
        try:
            os.mkdir(f"{audioDir}\\FinalClips")
        except OSError:
            pass
        x = 0
        while True:
            try:
                videoClip = VideoFileClip(f"Video Clips\\Clip{videoID}.mp4")
                audioClip = CompositeAudioClip([AudioFileClip(f"{audioDir}\\speech{x}.mp3")])
                start_time = rand.randint(0, int(math.floor(videoClip.end)) - int(math.floor(audioClip.end)))
                videoClip = videoClip.subclip(start_time, audioClip.end + start_time)
                videoClip.audio = audioClip
                videoClip.write_videofile(f"{audioDir}\\FinalClips\\final{x}.mp4", audio_codec="aac")
            except FileNotFoundError:
                break
            x += 1
    elif mode == 2:
        try:
            f = open(f"{audioDir}\\final.mp3")
            f.close()
        except FileNotFoundError:
            print(f"final.mp3 Not Found in {audioDir}.")
            print()
            return
        videoClip = VideoFileClip(f"Video Clips\\Clip{videoID}.mp4")
        audioClip = CompositeAudioClip([AudioFileClip(f"{audioDir}\\final.mp3")])
        start_time = rand.randint(0, int(math.floor(videoClip.end)) - int(math.floor(audioClip.end)))
        videoClip = videoClip.subclip(start_time, audioClip.end + start_time)
        videoClip.audio = audioClip
        videoClip.write_videofile(f"{audioDir}\\final.mp4", audio_codec="aac")


def segment_clips():
    audioDir = input("Project Directory: ")
    try:
        f = open(f"{audioDir}\\FinalClips\\final0.mp4")
        f.close()
    except FileNotFoundError:
        print(f"Clips Not Found in {audioDir}\\FinalClips.")
        print()
        return
    try:
        os.mkdir(f"{audioDir}\\FinalClips\\Youtube")
    except OSError:
        pass
    x = 0
    while True:
        try:
            clip = VideoFileClip(f"{audioDir}\\FinalClips\\final{x}.mp4")
            start = 0
            end = 59
            part = 0
            stop = False
            while end <= clip.end:
                newClip = clip.subclip(start, end)
                newClip.write_videofile(f"{audioDir}\\FinalClips\\Youtube\\clip{x}_part{part}.mp4", audio_codec="aac")
                end += 59
                print(f"clip end: {clip.end}")
                print(f"end: {end}\n start: {start}")
                if stop:
                    break
                if end > clip.end:
                    end = clip.end
                    stop = True
                start += 59
                part += 1
            x += 1
        except OSError:
            break


def main():
    print("""
Options:
    1: Audio Generation
    2: Combine Audio
    3: Create Video
    4: Segment Clips
    """)
    try:
        sel = int(input("Selection: "))
    except ValueError:
        print("Input must be an integer")
        main()

    if sel == 1:
        try:
            mode = int(input("Short/Long [1/2]: "))
        except ValueError:
            print("Input must be an integer")
            main()
        if mode == 1:
            generate_audio()
        elif mode == 2:
            generate_audio_long()
        else:
            print("Input must be 1 or 2")
    elif sel == 2:
        combine_audio()
    elif sel == 3:
        create_video()
    elif sel == 4:
        segment_clips()
    main()


if __name__ == '__main__':
    main()
