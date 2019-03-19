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

# ||=======================||
# ||=======================================================================||

def executeCommand(command):
    print (" >> ",command)
    subprocess.run(command.split())

command = "python -m pip install -r ../Settings/System/requirements.txt"
executeCommand(command)

print(" >> ", "Done")