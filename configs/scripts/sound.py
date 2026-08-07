#!/bin/python3
import subprocess
import os
import sys
import shutil

sounds_dir = f"/home/{os.getlogin()}/.config/scripts/sounds"
args = sys.argv


def play_sound(name):
    path = os.path.join(sounds_dir, name + ".mp3")
    subprocess.call(["ffplay","-nodisp", "-hide_banner" ,"-loglevel","error", "-autoexit", path])


subprocess.call(["mkdir", "-p", sounds_dir])

if len(args) > 1:
    if "-h" in args:
        print(
            "-h ~ print this help page \n-l ~ showing list of names of avalible sounds \n ------------------------------- \nsyntax: python main.py <name of sound> "
        )
        sys.exit()
    if "-l" in args:
        count = 0
        for i in os.listdir(sounds_dir):
            count += 1
            print(str(count) + ". " + i.rsplit(".", 1)[0])
        sys.exit()
    if shutil.which("ffplay") is None:
        print("Command ffplay is not avalible, did you install ffmpeg?")
        sys.exit()
    play_sound(args[1])
else:
    print(
        "-h ~ print this help page \n-l ~ showing list of names of avalible sounds \n ------------------------------- \nsyntax: python main.py <name of sound> "
    )
