__author__ = 'Yuki Sawa, yukisawa@gmail.com'
import zipfile
from DataModel import DataModel



''' first rewrite the log file by adding the date to each line
    then rename the file to Splunk format and copy it to the destination folder
'''

'''
A myfile tuple in matchingfiles consists of filepath, filename, servername, last modified date
'''
class file_handler(object):
    def __init__(self, myfile, log_destination_path):
        if zipfile.is_zipfile(myfile[0]):
            self.unzip_file(myfile, log_destination_path)
        else:
            print myfile[0] + " is not a zip file"

    ''' if the log file is in Omniplayer.log format then rewrite it as so '''
    def rewrite_and_copy_Omniplayer(self, new_filename, extracted_file, log_destination_path):
        edited_logs = []
        with open(extracted_file, "r") as openfile:
            openfile.readline()
            for line in openfile:
                if line != "\n":
                    date = self.year + "-" + self.month + "-" + self.day + " "
                    line = date + line.strip()
                    edited_logs.append(line)
        with open(log_destination_path + "\\" + new_filename, "w") as newfile:
            for line in edited_logs:
                newfile.write(line + "\n")

        print "extracted_file " + extracted_file
        # copy the file from \unzipped\ to log_destination_path
        # shutil.copy2(extracted_file, log_destination_path + "\\" + new_filename)

    ''' unzip the log file, check if the filename matches one of the 3 log types and if it is,
    rewrite by adding dates to each line and copy it to log_destination_path '''
    def unzip_file(self, myfile, log_destination_path):
        print "unzip_file - " + myfile[0]
        zfile = zipfile.ZipFile(myfile[0])
        dir = log_destination_path + "\\unzipped\\"
        zfile.extractall(dir)
        print "zfile.namelist(): " + str(zfile.namelist())
        for file_in_zip in zfile.namelist():
            new_filename, filetype = self.check_filename(file_in_zip, myfile)

            if filetype is not None:
                zfile.extract(file_in_zip)
                extracted_file = dir + "\\" + file_in_zip
                if filetype == "Omniplayer":
                    self.rewrite_and_copy_Omniplayer(myfile, new_filename, extracted_file, log_destination_path)

        zfile.close()
        # with zipfile.ZipFile(filename) as zfile:
        #     print "1 is zip file - " + DataModel.get_logdestinationpath()
        #     dir = DataModel.get_logdestinationpath() + "\\unzipped\\"
        #     print "2 before " + dir
        #     zfile.extractall(dir)
        #     print "3 after " + dir
        # check_valid_logfile(filename)

    def check_filename(self, file_in_zip, myfile):
        ''' check if file is in '25_06 -- 03_20_07.log' format aka Omniplayer.log '''
        ''' DD_MM -- HH_MM_SS.log '''
        try:
            filetype = None
            filenamesplit = file_in_zip.split("--")
            if len(filenamesplit) == 2:
                if len(filenamesplit[0]) == 6 and len(filenamesplit[1]) == 13:
                    date = filenamesplit[0].strip().split("_")
                    time = filenamesplit[1].strip().split("_")
                    if len(date) == 2 and len(time) == 3:
                        if date[0].isdigit() and date[1].isdigit() and time[0].isdigit() and time[1].isdigit() and time[2][0:2].isdigit():
                            self.year = str(myfile[3].year)
                            self.month = date[1]
                            self.day = date[0]
                            hour = time[0]
                            minute = time[1]
                            second = time[2][0:2]
                            new_filename = myfile[2] + "_Omniplayer_" + self.month + "_" + self.day + "_" + self.year + "_" + hour + "_" + minute + ".log"
                            filetype = "Omniplayer"
            if filetype is not None:
                print "new filename: " + new_filename + " - filetype: " + filetype
            return new_filename, filetype
        except IndexError:
            print "IndexError: list index out of range"
            return

''' check if a found file is a valid TXPlay or ITXLogger log file
def check_valid_logfile(filename):
    if zipfile.is_zipfile(filename):
    with open(filename, 'r') as myfile:
        myfile.readline()
        myfile.readline()
        myfile.readline()
        line = myfile.readline().strip()
        # myfile.seek(4)
        # line = myfile.readline().strip()
        print line
        if line == "Application Name: TXPlay":
            print("file is TXPLAY")
        for i in range(1,11):
            print myfile.readline()
        line = myfile.readline()
        month = line[1:2]
        day = line[3:5]
        year = line[6:]
'''
def unzip_file(filename):
    print "unzip file - " + filename
    if zipfile.is_zipfile(filename):
        print "0 checked if is zip"
        zfile = zipfile.ZipFile(filename)
        print "opened that shit"
        print DataModel.get_logdestinationpath()
        print "1 is zip file - " + DataModel.get_logdestinationpath()
        dir = DataModel.get_logdestinationpath() + "\\unzipped\\"
        print "2 before " + dir
        zfile.extractall(dir)
        print "3 after " + dir
        #
        # with zipfile.ZipFile(filename) as zfile:
        #     print "1 is zip file - " + DataModel.get_logdestinationpath()
        #     dir = DataModel.get_logdestinationpath() + "\\unzipped\\"
        #     print "2 before " + dir
        #     zfile.extractall(dir)
