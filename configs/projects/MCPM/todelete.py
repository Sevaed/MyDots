fabric = {
    "modloader": "fabric",
    "name": "Fabric API",
    "id": "fabric-api",
    "mod_version": "0.77.0",
    "icon": "assets/fabric/icon.png",
    "authors": ["FabricMC"],
    "dependencies": {"fabricloader": ">=0.14.9", "java": ">=17", "minecraft": "1.19.2"},
    "modloader_version": ">=0.14.9",
    "minecraft_version": "1.19.2",
    "description": "Core API module providing key hooks and intercompatibility features.",
}
forge = {
    "modloader": "forge",
    "name": "ImmediatelyFast",
    "id": "immediatelyfast",
    "mod_version": "1.4.0",
    "icon": "immediatelyfast-icon.png",
    "authors": "RK_01",
    "dependencies": [
        {
            "modId": "forge",
            "mandatory": True,
            "versionRange": "[43,)",
            "ordering": "NONE",
            "side": "CLIENT",
        },
        {
            "modId": "minecraft",
            "mandatory": True,
            "versionRange": "[1.19,1.19.2]",
            "ordering": "NONE",
            "side": "CLIENT",
        },
    ],
    "modloader_version": ">=43",
    "minecraft_version": ">=1.19,<=1.19.2",
    "description": "Speed up and optimize immediate mode rendering in Minecraft\n",
}
