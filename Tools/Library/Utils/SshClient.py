# ||=======================================================================||
# ||
# ||  Program/File:     sshtest.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    18 March 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Premades
import sys
from paramiko import SSHClient, AutoAddPolicy
import warnings
import time
# ||=======================||
# Global Variables
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
# ||=======================||
# Notes

# ||=======================||
# ||=======================================================================||

class SshClient():
    
    def __init__(self, hostname=None, username=None, password=None):
        print(" >> ","ssh "+username+hostname)
        passLen = len(password) 
        print(" >> ",username+hostname+"'s password:", '*'*passLen)
        if ((hostname == None) or (username == None) or (password == None)):
            raise Exception("Failure To Provide Login Information!")
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = 22
        self.sleeptime = 0.001

        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self.hostname, username=self.username, password=self.password, port=self.port)
        self.ssh_transp = self.ssh.get_transport()

# ||=======================================================================||

    def executeCommand(self, command):
        outdata = []
        errdata = []
        chan = self.ssh_transp.open_session()
        chan.setblocking(0)
        chan.exec_command(command)
        print(" >> ", command)
        while True:  # monitoring process
            # Reading from output streams
            if chan.recv_ready():
                data = chan.recv(1000).decode()
                outdata.append(data.replace('\n','\t').replace('\r','\n'))
                print('\t',data.replace('\n','\t').replace('\r',''))
            elif chan.recv_stderr_ready():
                data = chan.recv_stderr(1000).decode()
                errdata.append(data.replace('\n','\t').replace('\r','\n'))
                print('\t',data.replace('\n','\t').replace('\r',''))
            elif chan.exit_status_ready() and chan.recv_ready() == False and chan.recv_stderr_ready() == False:  # If completed
                break
            # time.sleep(self.sleeptime)
        return (outdata,errdata)

# ||=======================================================================||

    def closeClient(self):
        print()
        print(" >> ","Done.")
        self.ssh_transp.close()

# ||=======================================================================||