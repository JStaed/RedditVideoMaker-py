import subprocess
import codecs
import boto3
import sys
from contextlib import closing
import os


def synthesize_script(projectPath):
    session = boto3.session.Session()
    polly = session.client("polly")
    inputFileName = f"{projectPath}\\script.txt"

    f = codecs.open(inputFileName)
    cnt = 0

    for line in f:
        if '\n' == line:
            with open("shortpause.mp3", "rb") as p:
                pause = open(f"{projectPath}\\speech{cnt}.mp3", "wb")
                pause.write(p.read())
                pause.close
        else:
            response = polly.synthesize_speech(Text=line, VoiceId="Matthew", OutputFormat="mp3", Engine="generative")
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join(projectPath, f"speech{cnt}.mp3")

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
        cnt += 1
    print(f"Synthesized {projectPath}\\script.txt")
