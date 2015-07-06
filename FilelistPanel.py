__author__ = 'Administrator'
import wx
import logfetcher
from datetime import date
import wx.dataview as dv

# Class contains the file list and date controls
class FilelistPanel(wx.Panel):
    def InitFilelist(self):
        filelist = dv.DataViewListCtrl(self, style = dv.DV_MULTIPLE)
        filelist.AppendTextColumn("File name", width = 150)
        filelist.AppendTextColumn("Path", width = 370)
        filelist.AppendTextColumn("Server", width = 50)
        return filelist

    def __init__(self, parent, options_panel):

        """Constructor"""
        self.matchingfiles = []
        wx.Panel.__init__(self, parent = parent)
        self.options_panel = options_panel
        hsizer = self.InitDateUI()

        self.filelist = self.InitFilelist()

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.result_text = wx.StaticText(self, -1, "Found log files: ")
        sizer.Add(self.result_text, 0)
        sizer.Add(self.filelist, 1, wx.EXPAND | wx.BOTTOM, border = 10)
        sizer.Add(hsizer, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def InitDateUI(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # calendar boxes
        self.datefrom = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)

        self.dateto = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)

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
        hsizer.Add(self.datefrom, 1)
        hsizer.Add((25, 0), 0)
        hsizer.Add(datetolabel, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.dateto, 1)
        hsizer.Add((150, 0), 1)

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
        for file in self.matchingfiles:
            self.filelist.AppendItem([file[1], file[0], file[2]])

        self.result_text.SetLabel("Found log files: " + str(len(self.matchingfiles)) + " files")

    # copy the matching files to the specified folder. Additionally can write a zip file with them in it
    def OnSave(self, event):
        self.OnApply(self)
        zipoption = self.options_panel.get_zipoption()
        logfetcher.copyfiles(self.matchingfiles, self.options_panel.get_logdestinationpath(), self.options_panel.get_servername(), self.options_panel.zip_filename.GetLineText(0),
                             zipoption)

    # If there is a error with opening Windows paths show an error to user
    def ErrorDialog(self, matchingfiles, path, servername):
        if type(matchingfiles) is not list:
            errorcode = matchingfiles

            if "Error 53" in errorcode:
                dlg = wx.MessageDialog(self, errorcode + "\n" + servername , 'Error', wx.OK | wx.ICON_INFORMATION)
            else:
                dlg = wx.MessageDialog(self, errorcode + "\n" + path[len(servername)+6:] , 'Error', wx.OK | wx.ICON_INFORMATION)
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
