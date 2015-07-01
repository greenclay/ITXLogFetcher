import wmi

ip = "172.31.211.180"
username = "ITXNET2\Administrator"
password = "Omnibus123!!"
c = wmi.WMI()

__author__ = 'ysawa@directv.com'

import os.path
import os
import shutil
from datetime import date
import subprocess
import write_zip

# looks at when the file was last modified and sees if it was this or last month
# returns True if it was modified within the last month and False if it was not
def get_matchinglogs(path, datefrom, datetto):
    matchingfiles = []
    try:
        for filename in os.listdir(path):
            file = os.path.join(path, filename)

            try:
                mtime = os.path.getmtime(file)
            except OSError:
                print("File " + filename + " does not exist")
                mtime = 0

            datetoday = date.fromtimestamp(mtime)
            if datefrom <= datetoday and datetoday <= datetto:
                matchingfiles.append([file, filename])
    except WindowsError, err:
        print("Error with: " + err.filename)
        print("Error " + str(err.winerror) + " - " + err.strerror)
        matchingfiles = "Error " + str(err.winerror) + " - " + err.strerror

    return matchingfiles


def copyfiles(files_to_copy, log_destination_path = "C:\Users\Administrator.ADMINISTRATOR5\Desktop", zipoption = 1):
    if not os.path.exists(log_destination_path):
        try:
            os.makedirs(log_destination_path)
        except OSError:
            print("OSError - os.makedirs - " + log_destination_path)

    path = log_destination_path

    for file in files_to_copy:
        shutil.copy2(file[0], path)

    if zipoption == 0:
        # if zipoption == 0 then write zip file
        write_zip.write(files_to_copy, path)

    # open a folder in Windows explorer
    subprocess.Popen('explorer "{0}"'.format(log_destination_path))


def main(log_source_path = "C:\Users\Administrator.ADMINISTRATOR5\Desktop", datefrom = date(2015, 6, 24),
         datetto = date(2015, 6, 24)):
    # log_souce_path = "//YUKI-PC/C$/Users/Administrator.ADMINISTRATOR5/Desktop/A"
    # log_destination_path = "//YUKI-PC/C$/Users/Administrator.ADMINISTRATOR5/Desktop"

    log_destination_path = "C:\Users\Administrator.ADMINISTRATOR5\Desktop"
    log_destination_foldername = "logs"

    matchingfiles = get_matchinglogs(log_source_path, datefrom, datetto)
    # print "len of matchingfiles " + str(len(matchingfiles))
    # copyfiles(matchingfiles, self.log_destination_path, self.log_destination_foldername)

    return matchingfiles

if __name__ == '__main__':
    main()
