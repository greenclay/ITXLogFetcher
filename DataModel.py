__author__ = 'Administrator'
import datetime
from datetime import date
from operator import itemgetter
class DataModel(object):
    matchingfiles = []
    testvar = 1234
    options_panel = None
    test = False
    sort_ascending = 1
    prev_sort_selection = None
    @staticmethod
    def testing():
        DataModel.test = True
        return DataModel.test

    @staticmethod
    def get_zipconfig():
        '''
        return the the tuple (zipoption, zip_filename)
        zipoption is 0 or 1 and indicates whether to archive the selected log files into a zip or not
        zip_filename is the filename of the zip file to create
        :return:
        '''
        return DataModel.options_panel.get_zipoption(), DataModel.options_panel.get_zip_filename()

    @staticmethod
    def get_logdestinationpath():
        return DataModel.options_panel.get_logdestinationpath()

    @staticmethod
    def get_servername():
        return DataModel.options_panel.servername_txtctrl.GetLineText(0)

    @staticmethod
    def get_servername():
        return DataModel.options_panel.get_servername()

    ''' get the log source paths specified in "Path to the log files" box '''
    @staticmethod
    def get_logsourcepath():
        logpaths = []
        numChecked = 0
        for check in DataModel.options_panel.checklist_group:
            if check[0].GetValue() == True:
                numChecked += 1
                logpaths.append("\\\\" + DataModel.get_servername() + "\C$\\" + check[1].GetValue()[3:])
        # if there were no folders selected in the checklist boxes,throw an error
        if numChecked == 0:
            return "error no folders selected in checklist"
        return logpaths

    @staticmethod
    def sortColumn(sort_selection):
        if sort_selection == 1:
            DataModel.matchingfiles = sorted(DataModel.matchingfiles, key = lambda x: x[1].lower())  # sort by filename
        elif sort_selection == 2:
            DataModel.matchingfiles = sorted(DataModel.matchingfiles, key = itemgetter(3))  # sort by date
        elif sort_selection == 3:
            DataModel.matchingfiles = sorted(DataModel.matchingfiles, key = lambda x: x[0].lower())  # sort by path
        formatted_matchingfiles = []
        for myfile in DataModel.matchingfiles:
            filename = myfile[1]
            date = str(myfile[3].month).zfill(2) + "-" + str(myfile[3].day).zfill(2) + "-" + str(myfile[3].year)
            path = "C:\\" + myfile[0][len(myfile[2]) + 6:]
            formatted_matchingfiles.append((filename, date, path, DataModel.get_servername(), myfile))

        # Flip the sort order from ascending to descending or vice versa
        # if the same sorting is selected twice in a row
        if DataModel.prev_sort_selection == sort_selection:
            DataModel.sort_ascending = (DataModel.sort_ascending + 1) % 2
        DataModel.prev_sort_selection = sort_selection
        # If sort_ascending == False then reverse the order of the sorted list so it is descending order
        if DataModel.sort_ascending == 0:
            formatted_matchingfiles.reverse()
        return formatted_matchingfiles

    @staticmethod
    def get_day(datepicker):
        '''Process data from picked date'''
        selecteddate = datepicker.GetValue()
        month = selecteddate.Month + 1
        day = selecteddate.Day
        year = selecteddate.Year
        return date(year, month, day)

    @staticmethod
    def get_prevday():
        epoch = datetime.datetime.utcfromtimestamp(0)
        today = datetime.datetime.today()
        yesterday = (today - epoch).total_seconds() - 86400
        return date.fromtimestamp(yesterday)