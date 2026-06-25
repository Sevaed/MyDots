import jar_parser

path_forge = "/home/sevaed/.config/projects/MCPM/.tmp/test_mods/forge/1.19.2/sophisticatedbackpacks-1.19.2-3.20.2.1035.jar"
path_fabric = "/home/sevaed/.config/projects/MCPM/.tmp/test_mods/fabric/fabric-api-0.77.0+1.19.2.jar"

semver = jar_parser.mod_information(path_fabric)
maven = jar_parser.mod_information(path_forge)

print(str(semver) + "\n" + str(maven))
