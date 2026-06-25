from os.path import isdir
import sys
import os
import json

config_folder = "/home/seva/.config/"
MCMP_config_folder = os.path.join(config_folder, "MineCraftPackageManager")
if not os.path.exists(MCMP_config_folder):
    os.mkdir(MCMP_config_folder)

config_file = os.path.join(MCMP_config_folder, "MCMP_config.jsonc")
if not os.path.exists(config_file):
    with open(config_file, "w") as file:
        file.write("{}")

with open(config_file, "r") as file:
    config = json.load(file)
