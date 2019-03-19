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
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# ||=======================================================================||

hostname = "odd01.cs.ohio.edu"
username = "lwilkovi"
password = "Bellaeisle1!"

sshClient = SshClient(hostname=hostname, username=username, password=password)

command1 = "git clone https://github.com/lwilkovich/RoboticsEngine"
command2 = "rm -rf RoboticsEngine"
command3 = "ps"

sshClient.executeCommand(command3)
# sshClient.executeCommand(command2)
# sshClient.executeCommand(command1)
# sshClient.executeCommand(command2)
# sshClient.executeCommand(command1)

sshClient.closeClient()