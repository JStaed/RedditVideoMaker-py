# RedditVideoMaker-py

<br />

## Dependencies
* Python 3.8+
* ffmpeg
* praw
* boto3
* moviepy
* AWS account

### Installation of Dependencies
* Install Python 3.8+ from https://www.python.org/downloads/
* Install FFMPEG binary from https://www.ffmpeg.org/download.html
* Add the folder containing ffmpeg.exe to PATH
* Open command prompt
* Execute the following command to install python packages `pip install ffmpeg, praw, boto3, moviepy`
* Create or login to AWS and install the AWS CLI and your credentials and config files
* Place the credentials and config files in C://Users/{USER}/.aws/

<br />

## Installation and Instructions
* Download and extract the source code
* Open the command prompt in the project directory
* Place background videos in the Video Clips folder with the following naming convention `Clip0.mp4, Clip1.mp4, etc`
* Execute `python main.py`
* Follow the prompts given by the console

### Program Options
- 1: Audio Generation
    - Generate speech files from a specific Reddit post or weekly top posts from a specific Subreddit
- 2: Combine Audio
    - Combine speech files from a project folder into one full-length audio file
- 3: Create Video
    - Create a video/videos from the specified audio clips and specified video clip
- 4: Segment Clips
    - Split a video into 1-minute-long clips, appropriate length for YouTube Shorts
