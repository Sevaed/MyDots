import json
import zipfile
import tomllib
import tmp
import os
import semantic_version as semver
from unified_range import api as unified_range


def extract_modloader(mod):
    fabric = "fabric.mod.json"
    forge = "pack.mcmeta"
    names = mod.namelist()
    for name in names:
        if name == fabric:
            return "fabric"
        elif name == forge:
            return "forge"
    exit(
        "Couldn't determinate modloader, first: make sure that you choose correct file, second: make sure file is for fabric/forge MCPM currently does not support other modloaders, third: make issue on my github (https://github.com/Sevaed/MCPM) with file attached"
    )


def forge_minecraft_version_find(mod_information):
    dependencies = mod_information["dependencies"]
    # modID = mod_information["id"]
    for iteration in dependencies:
        if iteration["modId"] == "minecraft":
            return iteration["versionRange"]
    exit(
        "Couldn't determinate minecraft version required for this mod, please make an issue on project's GitHub(https://github.com/Sevaed/MCPM) don't forget to attach this mod"
    )


def forge_version_format_to_semver(version: str):
    try:
        semver.Version.parse(version)
    except ValueError:
        return unified_range.to_semver_comma_separated(version).replace(" ", "")
    # semver.SimpleSpec(
    #
    #       unified_range.to_semver_comma_separated(version).replace(" ", "")
    #   )
    else:
        return version
        # semver.Version(version)


def fabric_versions_to_semever(version: str):
    try:
        semver.Version.parse(version)
    except ValueError:
        return version  # semver.SimpleSpec(version)
    else:
        return version  # semver.Version(version)


def mod_information(path):
    tmpdir = tmp.create_tmpdir()
    with zipfile.ZipFile(path, "r") as mod:
        modloader = extract_modloader(mod)
        mod_information = {}
        if modloader == "fabric":
            with mod.open("fabric.mod.json", "r") as mod_info:
                mod_dict = json.load(mod_info)
            mod_information["modloader"] = "fabric"
            mod_information["name"] = mod_dict["name"]
            mod_information["id"] = mod_dict["id"]
            mod_information["mod_version"] = fabric_versions_to_semever(
                mod_dict["version"].split("+")[0]
            )
            mod_information["icon"] = mod_dict["icon"]
            mod_information["authors"] = mod_dict["authors"]
            mod_information["dependencies"] = mod_dict["depends"]
            mod_information["modloader_version"] = fabric_versions_to_semever(
                mod_dict["depends"]["fabricloader"]
            )
            mod_information["minecraft_version"] = fabric_versions_to_semever(
                mod_dict["depends"]["minecraft"]
            )
            mod_information["description"] = mod_dict["description"]
        if modloader == "forge":
            mod.extract("META-INF/mods.toml", tmpdir)
            with open(os.path.join(tmpdir, "META-INF", "mods.toml"), "rb") as mod_info:
                mod_dict = tomllib.load(mod_info)
                mod_information["modloader"] = "forge"
                mod_information["name"] = mod_dict["mods"][0]["displayName"]
                mod_information["id"] = mod_dict["mods"][0]["modId"]
                mod_information["mod_version"] = forge_version_format_to_semver(
                    mod_dict["mods"][0]["version"].split("+")[0]
                )
                mod_information["icon"] = mod_dict["mods"][0]["logoFile"]
                mod_information["authors"] = mod_dict["mods"][0]["authors"]
                mod_information["dependencies"] = mod_dict["dependencies"][
                    mod_information["id"]
                ]
                mod_information["modloader_version"] = forge_version_format_to_semver(
                    mod_dict["loaderVersion"]
                )
                mod_information["minecraft_version"] = forge_version_format_to_semver(
                    forge_minecraft_version_find(mod_information)
                )
                mod_information["description"] = mod_dict["mods"][0]["description"]

    return mod_information


def formatter(mod_information):
    pass
