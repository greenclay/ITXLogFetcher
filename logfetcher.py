__author__ = 'Yuki Sawa, email:ysawa@directv.com'

import os
import shutil
from datetime import date
import subprocess
import write_zip

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

            datetoday = date.fromtimestamp(mtime)
            if datefrom <= datetoday and datetoday <= datetto:
                matchingfiles.append([file, filename, servername])
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

    for filee in files_to_copy:
        print "copy2 - 1 - " + filee[1]
        print "copy2 - 2 - " + log_destination_path
        # shutil.copy2(filee[0], log_destination_path + "\\" + source_server_name + "_" + filee[1])
        shutil.copy2(filee[0], log_destination_path)

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
