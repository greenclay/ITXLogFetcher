__author__ = 'Yuki Sawa, yukisawa@gmail.com'

from threading import Thread
from datetime import date
import os
from DataModel import DataModel
import PopupDialog
import shutil
import subprocess
import write_zip

''' LogFetcherThread is created when FilelistPanel calls TopPanel.OnApply() which is when "Search for files" button is pressed
    it takes
'''
''' LogCopyerThread is created when FilelistPanel calls TopPanel.OnSave() which is when the user presses "Save selected files to folder"
    it takes a list of files on the selected ITX server and copies them onto the local computer.
'''
'''
    There needs to be 2 threads when TopPanel.OnSave() and TopPanel.OnApply() are called.
    1 thread handles the copying/searching while the other handles the progress bar, ProgressDialog

    myfile tuple layout = ( filepath, filename, servername, timestamp )
    A myfile tuple in matchingfiles consists of filepath, filename, servername, last modified date
'''

''' Thread that find files in the specified server and folders '''
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

        # if there are no paths selected in the check boxes, throw an Error Popup
        if logpaths == "error no folders selected in checklist":
            self.done = True
            PopupDialog.ErrorDialog.popup("Please select a path to search", "", "", self)
            return

        # for each selected checkbox path look for files
        for path in logpaths:
            matchingfiles = []  # matchingfiles contains tuples of form [entire file path, file name only]
            try:
                for filename in os.listdir(path):
                    if self.abort == True:
                        self.done = True
                        return
                    filepath = os.path.join(path, filename)
                    # Check if the filepath is an actual file
                    # Then use getmtime() to find the file's last modified date
                    if os.path.isfile(filepath):
                        try:
                            mtime = os.path.getmtime(filepath)
                        except OSError:
                            print("File " + filename + " does not exist")
                            # if there was an error getting the last modified date, give it mtime=0
                            mtime = 0

                        # Check if the file's modified date falls within the date range specified by the
                        # user in the DatePickers.
                        # If it does add it to matchingfiles
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
        """abort worker thread when user presses Cancel."""
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

            # if the file has "MIRADA_LOGS\TXPLAY" in its file path, add _txplay_ to its file name
            # if the file has "ITXLogs" in its file path, add _itxlogs_
            # otherwise don't add anything
            # ie Servername_txplay_filename.txt or Servername_itxlogs_filename.txt
            if "MIRANDA_LOGS\TXPLAY".lower() in myfile[0].lower():
                filename = myfile[2] + "_txplay_" + myfile[1]
            elif "ITXLogs".lower() in myfile[0].lower():
                filename = myfile[2] + "_itxlogs_" + myfile[1]
            else:
                filename = myfile[2] + "_" + myfile[1]

            print "Copying: " + myfile[1]
            print "To: " + filename + "\n"
            try:
                # copy the files to the user's computer
                shutil.copy2(myfile[0], log_destination_path + "\\" + filename)
            except WindowsError as err:
                # if there's an error with the copying, like permisison denied
                # show an ErrorDialog pop up
                self.done = True
                print("Error with: " + err.filename)
                print("Error " + str(err.winerror) + " - " + err.strerror)
                errorcode = "Error " + str(err.winerror) + " - " + err.strerror
                PopupDialog.ErrorDialog.popup(errorcode, log_destination_path, myfile[2], self)
                return str(err.strerror)
            except IOError as (errno, strerror):
                # if there's an error with the copying, like permisison denied
                # show an ErrorDialog pop up
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
