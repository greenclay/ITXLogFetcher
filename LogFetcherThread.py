__author__ = 'Yuki Sawa, yukisawa@gmail.com'

from threading import Thread
from datetime import date
import os
from DataModel import DataModel
import PopupDialog
import shutil
import write_zip
import subprocess
import file_handler
import zipfile

''' LogFetcherThread is created when FilelistPanel calls OnApply()

'''
''' LogCopyerThread is created when FilelistPanel calls OnSave() which is when the user presses "Save selected files to folder"
    it takes a list of files on the selected ITX server and copies them onto the local computer.
'''
'''
    myfile tuple layout = ( filepath, filename, servername, timestamp )
    A myfile tuple in matchingfiles consists of filepath, filename, servername, last modified date
'''

# Thread class that executes processing
class LogFetcherThread(Thread):
    """Worker Thread Class."""
    def __init__(self,  datefrom, dateto):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.logpaths = DataModel.get_logsourcepath()
        self.servername = DataModel.get_servername()
        self.datefrom = datefrom
        self.dateto = dateto
        self.done = False
        self.abort = False
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        '''
        Runs in parallel with PopupDialog.ProgressDialog
        self.abort - If the user presses the cancel on the ProgressDialog then ProgressDialog
        will set self.abort = True to sinal that this thread should end and file search halted.
        self.done - ProgressDialog periodically checks self.done, setting self.done = True lets it
        know that execution is done and ProgressDialog should also end
        :return:
        '''
        logpaths = self.logpaths
        datefrom = self.datefrom
        dateto = self.dateto
        servername = self.servername
        DataModel.matchingfiles = []

        if logpaths == "error no folders selected in checklist":
            self.done = True
            PopupDialog.ErrorDialog.popup("Please select a path to search", "", "", self)
            return

        for path in logpaths:
            matchingfiles = []  # matchingfiles contains tuples of form [entire file path, file name only]
            try:
                print(logpaths)
                print("path - " + path)
                for filename in os.listdir(path):
                    if self.abort == True:
                        self.done = True
                        return
                    filepath = os.path.join(path, filename)
                    # print path
                    # print(filename)
                    # print filepath
                    if os.path.isfile(filepath):
                        try:
                            mtime = os.path.getmtime(filepath)
                        except OSError:
                            print("File " + filename + " does not exist")
                            mtime = 0

                        timestamp = date.fromtimestamp(mtime)
                        if datefrom <= timestamp <= dateto:
                            ''' create a myfile tuple then append it to matchingfiles
                                it consists of filepath, filename, servername, last modified date
                            '''
                            myfile = ( filepath, filename, servername, timestamp )
                            matchingfiles.append(myfile)
            except WindowsError, err:
                self.done = True
                print("Error with: " + err.filename)
                print("Error " + str(err.winerror) + " - " + err.strerror)
                errorcode = "Error " + str(err.winerror) + " - " + err.strerror
                PopupDialog.ErrorDialog.popup(errorcode, path, servername, self)
                return
            DataModel.matchingfiles += matchingfiles
        self.done = True
        return

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1

class LogCopyerThread(Thread):
    def __init__(self,  files_to_copy):
        """Init Worker Thrlead Class."""
        Thread.__init__(self)
        self.files_to_copy = files_to_copy
        self.done = False
        self.abort = False

        (self.zipoption, self.zip_filename) = DataModel.get_zipconfig()
        print self.zipoption
        self.log_destination_path = DataModel.get_logdestinationpath()

        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this\
        # self.start()

    def run(self):
        # get settings, file paths
        log_destination_path = self.log_destination_path

        zipoption = self.zipoption
        zip_filename = self.zip_filename

        if not os.path.exists(log_destination_path):
            try:
                os.makedirs(log_destination_path)
            except OSError:
                print("OSError - os.makedirs - " + log_destination_path)
                self.done = True

        for myfile in self.files_to_copy:
            if self.abort == True:
                self.done = True
                return

            if "MIRANDA_LOGS\TXPLAY".lower() in myfile[0].lower():
                filename = myfile[2] + "_txplay_" + myfile[1]
            elif "ITXLogs".lower() in myfile[0].lower():
                filename = myfile[2] + "_itxlogs_" + myfile[1]
            else:
                filename = myfile[2] + "_" + myfile[1]

            print "Copying: " + myfile[1]
            print "To: " + filename + "\n"
            try:
                ''' unzip file for ITX logs onto Splunk plans '''
                # self.unzip_file(myfile[0])
                # file_handler.unzip_file(myfile, log_destination_path)
                ''' '''
                shutil.copy2(myfile[0], log_destination_path + "\\" + filename)
            except WindowsError as err:
                self.done = True
                print("Error with: " + err.filename)
                print("Error " + str(err.winerror) + " - " + err.strerror)
                errorcode = "Error " + str(err.winerror) + " - " + err.strerror
                PopupDialog.ErrorDialog.popup(errorcode, log_destination_path, myfile[2], self)
                return str(err.strerror)
            except IOError as (errno, strerror):
                self.done = True
                print("Error with: " + myfile[0])
                print("Error " + str(errno) + " - " + strerror)
                errorcode = "Error " + str(errno) + " - " + strerror
                PopupDialog.ErrorDialog.popup(errorcode, myfile[0], myfile[2], self)
                return str(strerror)
        print "Copied files to: " + log_destination_path

        if zipoption == 1:
            # if zipoption == 1 then combine the files and write a zip file
            write_zip.write(self.files_to_copy, log_destination_path, zip_filename)

        if DataModel.test == False:
            # open a folder in Windows explorer
            subprocess.Popen('explorer "{0}"'.format(log_destination_path))

        self.done = True

    def unzip_file(self, filename):
        print "unzip_file - " + filename
        if zipfile.is_zipfile(filename):
            print "0 checked if is zip"
            zfile = zipfile.ZipFile(filename)
            dir = self.log_destination_path + "\\unzipped\\"
            print "2 before " + dir
            zfile.extractall(dir)
            print "3 after " + dir
            #
            # with zipfile.ZipFile(filename) as zfile:
            #     print "1 is zip file - " + DataModel.get_logdestinationpath()
            #     dir = DataModel.get_logdestinationpath() + "\\unzipped\\"
            #     print "2 before " + dir
            #     zfile.extractall(dir)
            #     print "3 after " + dir
        else:
            file_handler.check_valid_logfile(filename)
            print "is not zip"

    # def rename(self, filename):
    #     if "MIRANDA_LOGS\TXPLAY\TXPlayTrace" in myfile[0]:
    #         filename = myfile[2] + "_txplay_" + myfile[1]
    #     else:
    #         filename = myfile[2] + "_" + myfile[1]