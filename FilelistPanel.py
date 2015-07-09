__author__ = 'Administrator'
import wx
import logfetcher
from datetime import date
from datetime import datetime
import wx.dataview as dv
from operator import itemgetter
# Class contains the file list and date controls
class FilelistPanel(wx.Panel):
    """Constructor"""
    def __init__(self, parent, options_panel):
        self.matchingfiles = []
        wx.Panel.__init__(self, parent = parent)
        self.options_panel = options_panel
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
        self.modifieddate_col = filelist.AppendTextColumn("Last modified date", width = 95)
        self.path_col = filelist.AppendTextColumn("Path", width = 380)
        # self.modifieddate_col.Bind(wx.EVT_BUTTON, self.OnSortColumnByDate)
        print self.filename_col.Title
        return filelist

    def InitDateUI(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        ''' INITIALIZE calendar boxes '''
        self.datefrom = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY, size=(85,-1))
        self.dateto = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY, size=(85, -1))

        """ set default day"""
        datefrom_date = wx.DateTime()
        yesterday_date = self.get_prevday()
        datefrom_date.Set(yesterday_date.day, yesterday_date.month-1, yesterday_date.year)

        self.datefrom.SetValue(datefrom_date)
        self.label = wx.StaticText(self, -1, "")

        # labels
        datefromlabel = wx.StaticText(self, -1, label = "From: ", size=(40,-1))
        datetolabel = wx.StaticText(self, -1, "To: ")


        """ INITIALIZE Sort by column selector Combo box """
        sortingChoices = ["File name", "Modified date", "File path"]
        cb = wx.ComboBox(self, 500, "Sort files by...", (0, 0),(100, -1),
                         sortingChoices, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.OnSortColumnByDate)

        # apply button
        applybutton = wx.Button(self, -1, label = "Search")
        applybutton.Bind(wx.EVT_BUTTON, self.OnApply)

        # apply button
        savebutton = wx.Button(self, -1, label = "Save to folder")
        savebutton.Bind(wx.EVT_BUTTON, self.OnSave)

        ''' Add controls to Sizer '''
        hsizer.Add(datefromlabel, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.datefrom, 1)
        hsizer.Add((30, 0), 0)
        hsizer.Add(datetolabel, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.dateto, 1)
        hsizer.Add((10, 0), 0)
        hsizer.Add(cb, 1)
        hsizer.Add((10, 0), 0)

        hsizer.Add(applybutton, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer((10, 0))
        hsizer.Add(savebutton, 0, wx.ALIGN_CENTER_VERTICAL)

        return hsizer

    def OnSortColumnByDate(self, event):
        self.matchingfiles = sorted(self.matchingfiles, key = itemgetter(3)) # sort by date
        print self.matchingfiles
        self.filelist.DeleteAllItems()
        for file in self.matchingfiles:
            date = str(file[3].month).zfill(2) + "-" + str(file[3].day).zfill(2) + "-" + str(file[3].year)
            path = "C:\\" + file[0][len(file[2]) + 6:]
            self.filelist.AppendItem([file[1], date, path, file])

        # self.matchingfiles = sorted(self.matchingfiles, key = itemgetter(1)) # sort by filename
        # self.matchingfiles = sorted(self.matchingfiles, key = itemgetter(0)) # sort by path

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
            mylist = logfetcher.main(path, servername, datefrom = picked_datefrom, datetto = picked_dateto)
            error = self.ErrorDialog(mylist, path, servername)
            if error:
                return
            self.matchingfiles = self.matchingfiles + mylist

        # update the file list box
        self.filelist.DeleteAllItems()

        print self.matchingfiles
        for file in self.matchingfiles:
            date = str(file[3].month).zfill(2) + "-" + str(file[3].day).zfill(2) + "-" + str(file[3].year)
            path = "C:\\" + file[0][len(file[2]) + 6:]
            self.filelist.AppendItem([file[1], date, path, file])

        self.result_text.SetLabel("Found " + str(len(self.matchingfiles)) + " files")


    def OnSave(self, event):
        # self.OnApply(self)
        print "OnSave:"
        # print self.filelist.GetSelectedRow()
        print self.filelist.GetSelectedItemsCount()
        selected = self.filelist.GetSelections()
        selectedfiles = []
        for s in selected:
            # print self.filelist.GetValue(s,1)
            print self.filelist.GetValue(s.GetID() - 1, 3)
            selectedfiles.append(self.filelist.GetValue(s.GetID() - 1, 3))

        zipoption = self.options_panel.get_zipoption()
        if len(selectedfiles) == 0:
            logfetcher.copyfiles(self.matchingfiles, self.options_panel.get_logdestinationpath(), self.options_panel.get_servername(),
                                 self.options_panel.zip_filename.GetLineText(0),
                                 zipoption)
        else:
            logfetcher.copyfiles(selectedfiles, self.options_panel.get_logdestinationpath(), self.options_panel.get_servername(),
                                 self.options_panel.zip_filename.GetLineText(0), zipoption)

    # If there is a error with opening Windows paths show an error to user
    def ErrorDialog(self, matchingfiles, path, servername):
        if type(matchingfiles) is not list:
            errorcode = matchingfiles

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