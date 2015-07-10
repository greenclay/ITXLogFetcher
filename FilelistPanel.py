__author__ = 'Administrator'
import wx
import logfetcher
from datetime import date
from datetime import datetime
import wx.dataview as dv
import config

import DataModel

# Class contains the file list and date controls
class FilelistPanel(wx.Panel):
    """Constructor"""

    def testing2(self):
        datefrom_date = wx.DateTime()
        datefrom_date.Set(1, 6, 2015)
        self.datefrom.SetValue(datefrom_date)
        self.OnApply(self)
        self.OnSave(self)

    def __init__(self, parent):
        self.matchingfiles = []
        wx.Panel.__init__(self, parent = parent)
        hsizer = self.InitDateUI()

        self.filelist = self.InitFilelist()
        """ TreeList Test, delete later? """  # self.filelist = self.InitTreeList()

        sizer = wx.BoxSizer(wx.VERTICAL)
        description_text = wx.StaticText(self, -1, "Found log files: ")
        self.result_text = wx.StaticText(self, -1, "")
        sizer.Add(description_text, 0)
        sizer.Add(self.filelist, 1, wx.EXPAND)
        sizer.Add(self.result_text, 0, wx.TOP | wx.BOTTOM, 5)
        sizer.Add(hsizer, 0, wx.EXPAND)

        self.SetSizer(sizer)

    """ intalize the file list """

    def InitFilelist(self):
        filelist = dv.DataViewListCtrl(self, style = dv.DV_MULTIPLE | dv.DV_ROW_LINES)
        self.filename_col = filelist.AppendTextColumn("File name", width = 170)
        self.modifieddate_col = filelist.AppendTextColumn("Last modified date", width = 105)
        self.path_col = filelist.AppendTextColumn("Path", width = 393)
        # self.modifieddate_col.Bind(wx.EVT_BUTTON, self.OnSortColumnByDate)
        return filelist

    def InitDateUI(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        ''' INITIALIZE calendar boxes '''
        self.datefrom = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY, size = (135, -1))
        self.dateto = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY, size = (146, -1))

        """ set default day"""
        datefrom_date = wx.DateTime()
        yesterday_date = self.get_prevday()
        datefrom_date.Set(yesterday_date.day, yesterday_date.month - 1, yesterday_date.year)

        self.datefrom.SetValue(datefrom_date)
        self.label = wx.StaticText(self, -1, "")

        # labels
        datefromlabel = wx.StaticText(self, -1, label = "From: ", size = (40, -1))
        datetolabel = wx.StaticText(self, -1, "To: ")


        # apply button
        applybutton = wx.Button(self, -1, label = "Search")
        applybutton.Bind(wx.EVT_BUTTON, self.OnApply)
        applybutton.SetDefault()

        # apply button
        savebutton = wx.Button(self, -1, label = "Save to folder")

        savebutton.Bind(wx.EVT_BUTTON, self.OnSave)

        ''' Add controls to Sizer '''
        hsizer.Add(datefromlabel, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.datefrom, 0)
        hsizer.Add((10, 0), 0)
        hsizer.Add(datetolabel, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.dateto, 0)
        hsizer.Add((10, 0), 1)

        hsizer.Add(applybutton, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer((10, 0))
        hsizer.Add(savebutton, 0, wx.ALIGN_CENTER_VERTICAL)

        return hsizer

    def OnSortColumnByDate(self, event):
        sort_selection = event.GetEventObject().GetCurrentSelection()  # 0 = file name, 1 = date, 2 = path
        # DataModel.sortColumn(sort_selection)

        if sort_selection == 1:
            self.matchingfiles = sorted(self.matchingfiles, key = lambda x: x[1].lower())  # sort by filename
        elif sort_selection == 2:
            self.matchingfiles = sorted(self.matchingfiles, key = lambda x: x[3])  # sort by date
        elif sort_selection == 3:
            self.matchingfiles = sorted(self.matchingfiles, key = lambda x: x[0].lower())  # sort by path

        self.filelist.DeleteAllItems()
        for file in self.matchingfiles:
            date = str(file[3].month).zfill(2) + "-" + str(file[3].day).zfill(2) + "-" + str(file[3].year)
            path = "C:\\" + file[0][len(file[2]) + 6:]
            self.filelist.AppendItem([file[1], date, path, file])

    # When the "search" button is pressed look for log files that match the specified dates and update the file list
    def OnApply(self, event):
        picked_dateto = self.get_day(self.dateto)
        picked_datefrom = self.get_day(self.datefrom)

        # log_path = self.log_source.GetLineText(0)
        log_path = self.options_panel.get_logsourcepath()

        servername = self.options_panel.get_servername()
        if len(servername) == 0:
            self.ErrorDialog("Please select a server", "", "")
            return
        if len(log_path) == 0:
            self.ErrorDialog("Please select at least one path to the log files", "", "")
            return
        self.matchingfiles = []
        error = False
        for path in log_path:
            servername = self.options_panel.get_servername()
            mylist = logfetcher.get_matchinglogs(path, servername, datefrom = picked_datefrom, dateto = picked_dateto)
            error = self.ErrorDialog(mylist, path, servername)
            if error:
                return
            self.matchingfiles = self.matchingfiles + mylist

        # update the file list box
        self.filelist.DeleteAllItems()

        for file in self.matchingfiles:
            date = str(file[3].month).zfill(2) + "-" + str(file[3].day).zfill(2) + "-" + str(file[3].year)
            path = "C:\\" + file[0][len(file[2]) + 6:]
            self.filelist.AppendItem([file[1], date, path, file])

        self.result_text.SetLabel("Found " + str(len(self.matchingfiles)) + " files")


    def OnSave(self, event):
        selected = self.filelist.GetSelections()
        selectedfiles = []
        for s in selected:
            selectedfiles.append(self.filelist.GetValue(s.GetID() - 1, 3))

        zipoption = self.options_panel.get_zipoption()
        if len(selectedfiles) == 0:
            err = logfetcher.copyfiles(self.matchingfiles, self.options_panel.get_logdestinationpath(), self.options_panel.get_servername(),
                                       self.options_panel.zip_filename.GetLineText(0),
                                       self, zipoption)
        else:
            err = logfetcher.copyfiles(selectedfiles, self.options_panel.get_logdestinationpath(), self.options_panel.get_servername(),
                                       self.options_panel.zip_filename.GetLineText(0), self, zipoption)
        if (err != None):
            self.ErrorDialog(err, "", "")

        ''' save the typed in server names to history.txt '''
        self.options_panel.server_choices.append(self.options_panel.get_servername())
        config.write_servername_history(self.options_panel.server_choices)
        self.options_panel.servername_txtctrl.AutoComplete(self.options_panel.server_choices)

        # output results to the screen
        self.result_text.SetLabel("Saved " + str(len(self.matchingfiles)) + " files")

    # If there is a error with opening Windows paths, servers, file permissions etc show an error to user
    def ErrorDialog(self, matchingfiles, path, servername):
        if type(matchingfiles) is not list:
            errorcode = matchingfiles
            print "\nERROR\n" + errorcode + "\n" + servername + "\n" + path + "\n"
            if "Error 53" in errorcode or "Error 1396" in errorcode:
                dlg = wx.MessageDialog(self, errorcode + "\n" + servername, 'Error', wx.OK | wx.ICON_INFORMATION)
            else:
                dlg = wx.MessageDialog(self, errorcode + "\n" + path[len(servername) + 6:], 'Error', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return True
        return False

    def get_day(self, datepicker):
        '''Process data from picked date'''
        selecteddate = datepicker.GetValue()
        month = selecteddate.Month + 1
        day = selecteddate.Day
        year = selecteddate.Year
        return date(year, month, day)

    def get_prevday(self):
        epoch = datetime.utcfromtimestamp(0)
        today = datetime.today()
        yesterday = (today - epoch).total_seconds() - 86400
        return date.fromtimestamp(yesterday)
