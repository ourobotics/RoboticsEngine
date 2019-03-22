# ||=======================================================================||
# ||
# ||  Program/File:     SshScript.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    18 March 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# /Library/Utils/
from Library.Utils.SshClient import SshClient
import subprocess
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# ||=======================================================================||

hostname = "192.168.0.20"
username = "pi"
password = "roverpassword1"
location = "/home/pi/Workspace/"

sshClient = SshClient(hostname=hostname, username=username, password=password)

command1 = "git clone https://github.com/lwilkovich/RoboticsEngine"
command2 = "rm -rf " + location + "RoboticsEngine"
command3 = "ls " + location
command4 = "mkdir " + location + "RoboticsEngine"
command5 = "scp -r ../../RoboticsEngine pi@192.168.0.20:/home/pi/Workspace/".split()

# sshClient.executeCommand(command1)
sshClient.executeCommand(command2)
subprocess.call(command5)
sshClient.executeCommand(command3)
# sshClient.executeCommand(command4)
# sshClient.executeCommand(command5)


sshClient.closeClient()