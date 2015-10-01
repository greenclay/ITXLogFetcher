
import wx
import wx.dataview as dv
import config
from LogFetcherThread import LogFetcherThread
from LogFetcherThread import LogCopyerThread
import PopupDialog

from DataModel import DataModel
import os
# Class contains the file list and date controls
''' wx.Panel Class which contains the top half of the app.
    This is everything above the "Path to the log files: " line
    Includes:
    1. The file list, a DataViewListCtrl, which lists the found files on a server/folder path
        Each row of the file list is a file that was found in a folder on the selected server.
        The file list has 4 columns. The first column is the file name. The second is the file's last modified date.
        The third column is the path to the file on the server. The fourth is the name of the server.
        You can select certain files to save using shift/ctrl and the left mouse button.
        If no files are selected then all files will be saved.
    2. The "Search for files" and "Save selected files to folder" buttons
        The "Search" button tells the app to search for the files in the selected server/folders and show the results on the file list.
        "Save files to folder" button saves the selected files into the specified folder. The default save folder is "C:\ITXLogFetcher_logs"
    3. The two DatePickerCtrl drop downs which allow you to select the dates the files' last modified date
    4. The TextCtrl box to type in the server name
    5. The "Sory files by..." drop down control
    6. The "Folder to save log files to" TextCtrl box where you can type in the folder to save the logs files to

'''
class TopPanel(wx.Panel):
    """Constructor"""

    def testing2(self):
        datefrom_date = wx.DateTime()
        datefrom_date.Set(24, 5, 2015)
        self.datefrom.SetValue(datefrom_date)
        self.OnApply(self)
        # self.OnSave(self)

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

        # hsizer = self.InitSelectSaveFolderUI()
        # sizer.Add(hsizer,0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(sizer)

    """ intalize the file list """

    def InitFilelist(self):
        filelist = dv.DataViewListCtrl(self, style = dv.DV_MULTIPLE | dv.DV_ROW_LINES)
        filelist.AppendTextColumn("File name", width = 150)
        filelist.AppendTextColumn("Last modified date", width = 110)
        filelist.AppendTextColumn("Path", width = 355)
        filelist.AppendTextColumn("Server", width = 98)
        return filelist

    def InitDateUI(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        ''' INITIALIZE DatePickers '''
        self.datefrom = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY, size = (135, -1))
        self.dateto = wx.DatePickerCtrl(self, -1, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY, size = (146, -1))

        """ set default day"""
        datefrom_date = wx.DateTime()
        yesterday_date = DataModel.get_prevday()
        datefrom_date.Set(yesterday_date.day, yesterday_date.month - 1, yesterday_date.year)

        self.datefrom.SetValue(datefrom_date)
        self.label = wx.StaticText(self, -1, "")

        # initialize date from and date to labels
        datefromlabel = wx.StaticText(self, -1, label = "From: ", size = (40, -1))
        datetolabel = wx.StaticText(self, -1, "To: ")


        # init Search for files button
        applybutton = wx.Button(self, -1, label = "Search for files")
        applybutton.Bind(wx.EVT_BUTTON, self.OnApply)
        applybutton.SetDefault()

        # init Save files button
        savebutton = wx.Button(self, -1, label = "Save selected files to folder")
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

    def OnSortColumnBySelection(self, event):
        '''
        When the user selects "Sort by..." sort the filelist by the user's choice
        :param event: wxpython event
        :return: None
        '''
        # sort_selection has 3 choices:
        # 0 = sort by file name, 1 = sort by date, 2 = sort by path
        sort_selection = event.GetEventObject().GetCurrentSelection()
        formatted_matchingfiles = DataModel.sortColumn(sort_selection)

        # Clear the filelist and update it with the sorted matchingfiles
        self.filelist.DeleteAllItems()
        for myfile in formatted_matchingfiles:
            self.filelist.AppendItem(myfile)

    '''
    Called when user presses "Search for files" button
    Creates LogFetcherThread to look for the files and displays a Pop up dialog with the progress on it
    '''
    def OnApply(self, event):

        # get the required info from the interface
        picked_dateto = DataModel.get_day(self.dateto)
        picked_datefrom = DataModel.get_day(self.datefrom)

        # Start a new thread and look for files that match the dates and directories
        # Needs a new thread so ProgressDialog and LogFetcher can run in parallel.
        # Otherwise ProgressDialog would wait for LogFetcher to complete before running
        lfthread = LogFetcherThread(picked_datefrom, picked_dateto)

        # Show a popup with a progress bar
        PopupDialog.ProgressDialog(self, lfthread, message = "Searching for files...")
        self.UpdateFilelist()

    ''' Update the file list by deleting everything with filelist.DeleteAllItems()
        then adding all files in DataModel.matchingfiles into the filelist
    '''
    def UpdateFilelist(self):
        self.filelist.DeleteAllItems()
        # for each matching file, format the date and path
        # then add a row to the file list consisting of: (filename, last modified date, file path, server name, file object)
        for myfile in DataModel.matchingfiles:
            formatted_date = str(myfile[3].month).zfill(2) + "-" + str(myfile[3].day).zfill(2) + "-" + str(myfile[3].year)
            path = "C:\\" + myfile[0][len(myfile[2]) + 6:]
            self.filelist.AppendItem((myfile[1], formatted_date, path, myfile[2], myfile))

        self.result_text.SetLabel("Found " + str(len(self.matchingfiles)) + " files")

    def OnSave(self, event):
        '''
        Runs when "Save files to folder" button is clicked.
        Takes the currently selected files in the filelist and copies them to the folder specified by the user.
        If no files are selected then all the files are copied.
        :param event:
        :return:
        '''
        # get the files selected in the filelist
        selected = self.filelist.GetSelections()
        selectedfiles = []
        for s in selected:
            # get the value of each selected file and append them to a list
            selectedfiles.append(self.filelist.GetValue(s.GetID() - 1, 4))

        # If there were no files selected then copy all the files
        # otherwise only copy the selected.
        # Start the copying thread.
        if len(selectedfiles) == 0:
            lcthread = LogCopyerThread(DataModel.matchingfiles)
        else:
            lcthread = LogCopyerThread(selectedfiles)
        lcthread.start()
        pd = PopupDialog.ProgressDialog(self, lcthread, message = "Copying files...")

        ''' save the typed in server names to history.txt '''
        DataModel.bottom_panel.server_choices.append(self.bottom_panel.get_servername())
        config.write_servername_history(self.bottom_panel.server_choices)
        DataModel.bottom_panel.servername_txtctrl.AutoComplete(self.bottom_panel.server_choices)

        # output results to the screen
        self.result_text.SetLabel("Saved " + str(len(self.matchingfiles)) + " files")

