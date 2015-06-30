__author__ = 'ysawa@directv.com'

from socket import *
import wmi
ip = "172.31.211.180"
username = "ITXNET2\Administrator"
password = "Omnibus123!!"
c = wmi.WMI ()

def test1():
    try:
        print("Establishing connection to %s" % ip)
        connection = wmi.WMI(ip, user=username, password=password)
        for s in c.Win32_Service ():
            if s.State == 'Stopped':
                print s.Caption, s.State
        print("Connection established")
    except wmi.x_wmi:
        print("Your Username and Password of "+getfqdn(ip)+" are wrong.")

def test2():
    ip = "localhost"
    try:
        print("Establishing connection to %s" % ip)
        # connection = wmi.WMI(ip, user=username, password=password)
        c = wmi.WMI()
        for s in c.Win32_Service ():
            if s.State == 'Stopped':
                print(s.Caption, s.State)
        print("Connection established")
    except wmi.x_wmi:
        print("Your Username and Password of "+getfqdn(ip)+" are wrong.")

def runnotepad():
    c = wmi.WMI ()

    process_id, return_value = c.Win32_Process.Create (CommandLine="notepad.exe")
    for process in c.Win32_Process (ProcessId=process_id):
      print process.ProcessId, process.Name

    # result = process.Terminate ()

def find_drivetypes():
    DRIVE_TYPES = {
      0 : "Unknown",
      1 : "No Root Directory",
      2 : "Removable Disk",
      3 : "Local Disk",
      4 : "Network Drive",
      5 : "Compact Disc",
      6 : "RAM Disk"
    }

    for drive in c.Win32_LogicalDisk ():
        disk = drive
        if disk.DriveType == 3:
            space = 100 * long (disk.FreeSpace) / long (disk.Size)
            print "%s has %d%% free" % (disk.Name, space)
        print drive.Caption, DRIVE_TYPES[drive.DriveType]

def directory():
    print c.Win32_Process.Create
    print "test"


# find_drivetypes()
directory()