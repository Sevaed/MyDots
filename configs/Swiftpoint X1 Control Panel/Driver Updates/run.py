#!/usr/bin/python
from matplotlib.pylab import full
import os
import tarfile
import filecmp

files = os.listdir("/home/sevaed/.config/Swiftpoint X1 Control Panel/Driver Updates")
dirs = {}
archives = {}


def name_to_num(name: str):
    if name.startswith("Swiftpoint X1 Control Panel "):
        first = name.removeprefix("Swiftpoint X1 Control Panel ")
        second = first.replace(".", "")
        return int(second)
    elif name.endswith("xz"):
        first = name.removesuffix(".tar.xz")
        second = first.replace(".", "")
        return int(second)


def install_update(path: str):
    INSTALL_PATH = "/home/sevaed/.config/Swiftpoint X1 Control Panel/Driver Updates"
    with tarfile.open(path) as file:
        file.extractall(filter="fully_trusted", path=INSTALL_PATH)
    udev_rule_path = os.path.join(
        INSTALL_PATH,
        "Swiftpoint X1 Control Panel "
        + path.removeprefix(INSTALL_PATH + "/").removesuffix(".tar.xz"),
        "60-Swiftpoint.rules",
    )
    UDEV_RULE_PATH = os.path.join("/etc/udev/rules.d", "60-Swiftpoint.rules")
    if not filecmp.cmp(UDEV_RULE_PATH, udev_rule_path):
        exit("update udev")


def full_path(name: str, is_dir=True):
    if not is_dir:
        file = archives[name]
        path = os.path.join(
            "/home/sevaed/.config/Swiftpoint X1 Control Panel/Driver Updates", file
        )
        install_update(path)
        INSTALL_PATH = "/home/sevaed/.config/Swiftpoint X1 Control Panel/Driver Updates"
        return os.path.join(
            INSTALL_PATH,
            "Swiftpoint X1 Control Panel "
            + path.removeprefix(INSTALL_PATH + "/").removesuffix(".tar.xz"),
            "Swiftpoint X1 Control Panel",
        )
    else:
        file = dirs[name]
        return os.path.join(
            "/home/sevaed/.config/Swiftpoint X1 Control Panel/Driver Updates",
            file,
            "Swiftpoint X1 Control Panel",
        )


for i in files:
    if i != "run.py":
        if i.endswith(".xz"):
            archives[name_to_num(i)] = i
        else:
            dirs[name_to_num(i)] = i

dirs_vers = []
archives_vers = []

for i in dirs.keys():
    dirs_vers.append(i)

for i in archives.keys():
    archives_vers.append(i)

dirs_vers.sort(reverse=True)
archives_vers.sort(reverse=True)


if dirs_vers[0] >= archives_vers[0]:
    print(full_path(dirs_vers[0]))
else:
    print(full_path(archives_vers[0], is_dir=0))
