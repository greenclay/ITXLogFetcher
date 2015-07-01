__author__ = 'Administrator'
import wx
import logfetcher
from datetime import date

# Class contains the file list and date controls
class FilelistPanel(wx.Panel):
    def __init__(self, parent, options_panel):
        """Constructor"""
        self.matchingfiles = []
        wx.Panel.__init__(self, parent = parent)
        self.options_panel = options_panel
        hsizer = self.InitDateUI()
        self.filelist_listbox = wx.ListBox(self, -1, wx.DefaultPosition, wx.DefaultSize, [], wx.LB_SINGLE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.filelist_listbox, 3, wx.EXPAND)
        sizer.Add(hsizer, 0, wx.ALL, 10)

        self.SetSizer(sizer)

    def update_filelist(self, matchingfiles):
        self.filelist_listbox.Clear()
        for file in matchingfiles:
            self.filelist_listbox.Append(file[1])

    def InitDateUI(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # calendar boxes
        self.datefrom = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.datefrom.Bind(wx.EVT_DATE_CHANGED, self.OnApply)

        self.dateto = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.dateto.Bind(wx.EVT_DATE_CHANGED, self.OnApply)

        self.label = wx.StaticText(self, -1, "")

        # labels
        datefromlabel = wx.StaticText(self, -1, label = "From: ")
        datetolabel = wx.StaticText(self, -1, "To: ")

        # apply button
        applybutton = wx.Button(self, -1, label = "Search")
        applybutton.Bind(wx.EVT_BUTTON, self.OnApply)

        # apply button
        savebutton = wx.Button(self, -1, label = "Save to folder")
        savebutton.Bind(wx.EVT_BUTTON, self.OnSave)

        hsizer.Add(datefromlabel, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.datefrom, 0)
        hsizer.AddSpacer((25, 0))
        hsizer.Add(datetolabel, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.dateto, 0)
        hsizer.AddSpacer((60, 0))

        hsizer.Add(applybutton, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer((10, 0))
        hsizer.Add(savebutton, 0, wx.ALIGN_CENTER_VERTICAL)

        return hsizer

    # When the "search" button is pressed look for log files that match the specified dates
    def OnApply(self, event):
        picked_dateto = self.get_day(self.dateto)
        picked_datefrom = self.get_day(self.datefrom)

        # log_path = self.log_source.GetLineText(0)
        log_path = self.options_panel.get_logsourcepath()
        self.matchingfiles = logfetcher.main(log_source_path = log_path, datefrom = picked_datefrom, datetto = picked_dateto)

        if type(self.matchingfiles) is not list:
            print self.matchingfiles
            self.ErrorDialog(self.matchingfiles)
            self.matchingfiles = []

        self.filelist_listbox.Clear()
        for file in self.matchingfiles:
            self.filelist_listbox.Append(file[1])

    # copy the matching files to the specified folder. Additionally can write a zip file with them in it
    def OnSave(self, event):
        self.OnApply(self)
        zipoption = self.options_panel.radiobuttons.GetSelection()
        print zipoption
        logfetcher.copyfiles(self.matchingfiles, self.options_panel.get_logdestinationpath(), zipoption)

    # If there is a error with opening Windows paths show an error to user
    def ErrorDialog(self, errorcode):
        dlg = wx.MessageDialog(self, errorcode,
                               'Error',
                               wx.OK | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def get_day(self, datepicker):
        '''Process data from picked date'''
        selecteddate = datepicker.GetValue()
        month = selecteddate.Month + 1
        day = selecteddate.Day
        year = selecteddate.Year
        return date(year, month, day)
