# ||=======================================================================||
# ||
# ||  Program/File:     InstallPackages.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    19 March 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Premades
import subprocess
# ||=======================||
# Global Variables

# ||=======================||
# Notes
# python3 -m pip search <package>
# python3 -m pip install -r <path>
# sudo apt-cache policy <package>
# sudo apt-get install <package>=<version>
# ||=======================||
# ||=======================================================================||

def executeCommand(command):
    print (" >> ",command)
    subprocess.run(command.split())

command = "python3 -m pip install -r ../Settings/System/Requirements.txt"
executeCommand(command)

file = open("../Settings/System/PackageList.package", 'r')
packages = file.readlines()
for i in range(len(packages)):
    command = "sudo apt-get install " + packages[i]
    executeCommand(command)


print(" >> ", "Done")