__author__ = 'Administrator'
import datetime
from operator import itemgetter
class DataModel(object):
    matchingfiles = []
    options_panel = []
    testvar = 1234

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
            formatted_matchingfiles.append((filename, date, path, myfile))

        return formatted_matchingfiles

    '''Process data from picked date'''
    def get_day(datepicker):
        selecteddate = datepicker.GetValue()
        month = selecteddate.Month + 1
        day = selecteddate.Day
        year = selecteddate.Year
        return datetime.date(year, month, day)

    ''' Using today's date calculate previous day's date and return it'''
    def get_prevday():
        epoch = datetime.utcfromtimestamp(0)
        today = datetime.today()
        yesterday = (today - epoch).total_seconds() - 86400
        return datetime.date.fromtimestamp(yesterday)