#!/usr/bin/python
import json
from sys import argv
from os import path, makedirs
from subprocess import run

SAVELIST = path.expanduser("~/.config/backup/MyDots/savelist.json")
CONFIG_FOLDER = path.expanduser("~/.config")

file_path = path.expanduser("~/.config/backup/MyDots/configs")

with open(SAVELIST, "r") as file:
    data = json.load(file)


def recover():
    src = file_path + "/"
    dst = CONFIG_FOLDER
    run(["rsync", "-drq", "--mkpath", "--ignore-existing", src, dst], check=True)
    print("sudo ln -s ~/.config/tint.scores /var/games/tint.scores")


def backup():
    for i in data:
        src = path.join(CONFIG_FOLDER, i)
        dst = path.join(file_path, path.dirname(i))
        makedirs(dst, exist_ok=True)
        # print("rsync", "-drq", "--mkpath", '--exclude="git"', src, " ", dst)
        run(["rsync", "-drq", "--mkpath", "--exclude=git", src, dst], check=True)

if len(argv) == 2:
    if argv[1] in ["backup","--backup","back","-b"]:
        backup()
    elif argv[1] in ["recover","--recover","rec","-r"]:
        recover()
else:
    exit("backup/--backup/back/-b for creating backup\nrecover/--recover/rec/-r for recovering backup")
