__author__ = 'Yuki Sawa, email:ysawa@directv.com'

import os
import shutil
from datetime import date
import subprocess
import write_zip

""" Format of matchingfiles list """
""" file = [file path, file name, server name, time stamp]"""

# looks at when the file was last modified and sees if it was this or last month
# returns True if it was modified within the last month and False if it was not
def get_matchinglogs(path, datefrom, datetto, servername):
    matchingfiles = [] # matchingfiles contains tuples of form [entire file path, file name only]
    try:
        for filename in os.listdir(path):
            file = os.path.join(path, filename)

            try:
                mtime = os.path.getmtime(file)
            except OSError:
                print("File " + filename + " does not exist")
                mtime = 0

            timestamp = date.fromtimestamp(mtime)
            if datefrom <= timestamp and timestamp <= datetto:
                matchingfiles.append([file, filename, servername, timestamp])
    except WindowsError, err:
        print("Error with: " + err.filename)
        print("Error " + str(err.winerror) + " - " + err.strerror)
        matchingfiles = "Error " + str(err.winerror) + " - " + err.strerror

    return matchingfiles


def copyfiles(files_to_copy, log_destination_path, source_server_name, zip_filename, zipoption = 0):
    if not os.path.exists(log_destination_path):
        try:
            os.makedirs(log_destination_path)
        except OSError:
            print("OSError - os.makedirs - " + log_destination_path)

    for myfile in files_to_copy:
        # print "shutil.copy2, myfile[1] aka filename: " + myfile[1]
        # print "shutil.copy2, log_destination_path: " + log_destination_path
        # shutil.copy2(filee[0], log_destination_path + "\\" + source_server_name + "_" + filee[1])
        shutil.copy2(myfile[0], log_destination_path + "\\" +  myfile[2] + "_" +  myfile[1])

    if zipoption == 1:
        # if zipoption == 1 then combine the files and write a zip file
        write_zip.write(files_to_copy, log_destination_path, zip_filename)

    # open a folder in Windows explorer
    subprocess.Popen('explorer "{0}"'.format(log_destination_path))


def main(log_source_path, servername, datefrom = date(2015, 6, 24),
         datetto = date(2015, 6, 24)):
    matchingfiles = get_matchinglogs(log_source_path, datefrom, datetto, servername)

    return matchingfiles

if __name__ == '__main__':
    main()
