import os


def create_tmpdir():
    tmp_dir = "/tmp/MCPM"
    idFilePath = os.path.join(tmp_dir, ".idFile")
    idFileContent = (
        "https://github.com/Sevaed \nThere isn't anything intresting in this file"
    )
    if not os.path.isdir(tmp_dir):
        pass
    else:
        is_done = False
        tryies = 1
        while not is_done:
            if not os.path.isdir(tmp_dir):
                break
            if os.path.isfile(idFilePath):
                with open(idFilePath, "r") as idFile:
                    if idFile.read() == idFileContent:
                        return tmp_dir
                    else:
                        tryies += 1
                        tmp_dir = f"/tmp/MCPM{tryies}"
            else:
                tryies += 1
                tmp_dir = f"/tmp/MCPM{tryies}"
    os.mkdir(tmp_dir)
    with open(os.path.join(tmp_dir, ".idFile"), "w") as file:
        file.write(idFileContent)
    return tmp_dir
