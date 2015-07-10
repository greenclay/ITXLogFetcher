__author__ = 'Administrator'
import datetime
from operator import itemgetter

matchingfiles = []

def sortColumn(sort_selection):
    if sort_selection == 1:
        matchingfiles = sorted(matchingfiles, key = lambda x: x[1].lower())  # sort by filename
    elif sort_selection == 2:
        matchingfiles = sorted(matchingfiles, key = itemgetter(3))  # sort by date
    elif sort_selection == 3:
        matchingfiles = sorted(matchingfiles, key = lambda x: x[0].lower())  # sort by path

'''Process data from picked date'''
def get_day(self, datepicker):
    selecteddate = datepicker.GetValue()
    month = selecteddate.Month + 1
    day = selecteddate.Day
    year = selecteddate.Year
    return datetime.date(year, month, day)

''' Using today's date calculate previous day's date and return it'''
def get_prevday(self):
    epoch = datetime.utcfromtimestamp(0)
    today = datetime.today()
    yesterday = (today - epoch).total_seconds() - 86400
    return datetime.date.fromtimestamp(yesterday)