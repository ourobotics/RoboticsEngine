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
# pip freeze | xargs pip uninstall -y
# ||=======================||
# ||=======================================================================||


def executeCommand(command):
    print (" >> ",command)
    subprocess.run(command.split())

def run():
    pythonBinary = input("Please specify your Python Binary (e.g. 'python3' foo.py): ")
    if (pythonBinary == ''):
        pythonBinary = "python3"

    file = open("../Settings/System/PackageList.package", 'r')
    packages = file.readlines()
    for i in range(len(packages)):
        command = "sudo apt-get install " + packages[i]
        executeCommand(command)
    command = "sudo apt-get update"
    executeCommand(command)

    command = "sudo " + pythonBinary + " -m pip install -r ../Settings/System/Requirements.txt"
    executeCommand(command)

    print(" >> ", "Done")

run()