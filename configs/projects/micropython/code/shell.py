import os

debug = False


def mod(num: int) -> int:
    if num >= 0:
        return num
    else:
        return num * -1


def is_path_exists(path: str):
    if debug:
        print(f"is_path_exists({path})")
    if is_file(path):
        return True, True
    if path in [".", "..", "/"]:
        return True, False
    if path.count("/") == 0:
        if path in os.listdir():
            return True, False
        else:
            return False, True
    thing = path.strip().split("/")
    if path.strip().startswith("/"):
        exists = "/"
    else:
        exists = "."
    for i in thing:
        if i != ".." and i in os.listdir(exists):
            exists += "/" + i
        elif i == "..":
            exists += "/.."
        elif i == "":
            pass
        else:
            if i == thing[-1]:
                return False, True
            else:
                return False, False
    return True, False


def is_file(path):
    if debug:
        print(f"is_file({path})")
    try:
        with open(path, "r") as file:
            file.close()
    except IsADirectoryError:
        return False
    except FileNotFoundError:
        return False
    else:
        return True


def cd(path="/"):
    if debug:
        print(f"cd({path})")
    exists, file = is_path_exists(path)
    if not exists:
        print(f"Error {path} does not exists")
    if file:
        print(f"Error {path} is file")
    if exists and not file:
        os.chdir(path)


def ls(path="."):
    if debug:
        print(f"ls({path})")
    if is_file(path):
        print(path)
        return
    try:
        things = [".", ".."]
        for i in os.listdir(path):
            things.append(i)
        for i in things:
            print(i)
    except FileNotFoundError:
        print(f"Error {path} does not exist")


def mkdir(path: str):
    if debug:
        print(f"mkdir({path})")
    exists, creatable = is_path_exists(path)
    if not exists and creatable:
        os.mkdir(path)
    elif exists:
        print(f"Error {path} alredy exists")
    elif not creatable:
        print(f"Error {path} is not creatable")


def recursive_remove(path):
    if debug:
        print(f"recursive_remove({path})")
    if is_path_exists(path):
        if is_file(path):
            os.remove(path)
        elif os.listdir(path):
            for file in os.listdir(path):
                recursive_remove(path + f"/{file}")
            os.rmdir(path)
        else:
            os.rmdir(path)


def rm(path, flag=""):
    if debug:
        print(f"rm({path},{flag})")
    if flag in ["-r", "-rf"]:
        recursive_remove(path)
    elif is_file(path):
        os.remove(path)
    else:
        print(f"Error: {path} is a directory")


def cat(path):
    if debug:
        print(f"cat({path})")
    if is_file(path):
        with open(path, "r") as file:
            print(file.read())
    else:
        print(f"Error: {path} is a directory")


def mv(src, dest):
    if debug:
        print(f"mv({src},{dest})")
    dest_exists, dest_createble = is_path_exists(dest)
    src_exists, src_createble = is_path_exists(src)
    if not src_exists:
        print(f"Error {src} does not exists")
        return
    if dest_exists:
        print(f"Error {dest} already exists")
    if not dest_createble:
        print(f"Error cannot create {dest}")
    if dest in os.listdir():
        dest = src[src.rfind("/") - 1 :]
    os.rename(src, dest)


def exit():
    global active
    active = False


def help():
    global aliases
    for i in aliases.keys():
        print(i)


def toggle_debug(mode=None):
    global debug
    if type(mode) is None:
        print(f"Debug is {debug}")
    elif mode:
        debug = True
        print(f"Debug is {debug}")
    else:
        debug = False
        print(f"Debug is {debug}")


aliases = {
    "help": help,
    "ls": ls,
    "mv": mv,
    "rm": rm,
    "mkdir": mkdir,
    "cat": cat,
    "cd": cd,
    "debug": toggle_debug,
    "exit": exit,
    "quit": exit,
    "e": exit,
    "q": exit,
}


def parse_input(input: str):
    input = input.strip()
    args = input.split(" ")
    if args[0] not in aliases:
        print("Command not found")
    else:
        if len(args) == 3:
            if args[0] == "rm":
                aliases[args[0]](args[2], args[1])
            else:
                aliases[args[0]](args[1], args[2])
        elif len(args) == 1:
            aliases[args[0]]()
        else:
            aliases[args[0]](args[1])


active = True
while True:
    if not active:
        break
    cwd = os.getcwd()
    parse_input(input(cwd + "/$ "))
