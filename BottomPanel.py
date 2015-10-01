
import wx
import os
import config
import PopupDialog
import DataModel

''' wx.Panel Class that contains the bottom half of the App from the "Folders to search" line to the bottom
    Includes:
    1. "Select folder to save files to" buttons
    1. The three CheckBox and TextCtrl which specify what folders on the server to search.
        The three options are ITXLogs, TXPlay, and an "Other" folder that the user can specify
    2. The yes/no RadioBox option with the "Archive logs into a zip file" heading which lets you choose what option the app should
    default to when it's opened.
    The "yes" option tells the app to archive the selected files into a zip file and save it into the same
    folder in the ""Folder to save log files to" text box.
    The "no" option tells the app to only save the selected files into the folder.
    3. The "Save current setting to zip files" button which saves the current option of wether or not to archive the files into a zip file.
    If the option is saved, the next time the app is opened again it will default to the option that was saved.
    4. The "Save zip file as:" TextCtrl box that specifies the filename of the zip file if you choose to make one.
'''
class BottomPanel(wx.Panel):
    # default paths to the ITX and TXPlay log folders
    ITXLogPath = "C:\ITXLogs"
    TXPlayLogPath = "C:\MIRANDA_LOGS\TXPLAY\TXPlayTrace"

    ''' Method to set varibles up for quick testing'''
    def testing1(self):
        self.servername_txtctrl.SetValue("YUKI-PC")
        self.checklist_group[0][0].SetValue(True)
        self.checklist_group[1][0].SetValue(True)

    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)
        self.logsource_list = []
        self.zipoption = config.read_config()

        ''' Server choice controls '''
        hsizer1, self.servername_txtctrl, self.server_choices = self.InitServernameTextCtrl()

        ''' Initialize check buttons with log path controls'''
        hsizer2, self.checklist_group = self.InitCheckBoxes()

        ''' Intialize controls for folder to copy the log files to '''
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        folderselect_button = wx.Button(self, -1, "Select folder to save files to", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OpenFileButton, folderselect_button)

        # desktoppath = os.path.expanduser('~') + '\Desktop\logs'
        desktoppath = 'C:\ITXLogFetcher_logs'
        self.logdestination_text = wx.TextCtrl(self, -1, desktoppath, size = (200, -1))
        self.logdestination_text.AutoCompleteDirectories()

        hsizer3.Add(wx.StaticText(self, -1, "Folder to save log files to: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add(self.logdestination_text, 1, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add((10, 0), 0)
        hsizer3.Add(folderselect_button, 0, wx.ALIGN_CENTER_VERTICAL)

        ''' zip options control '''
        hsizer4, self.radiobuttons, self.zip_filename = self.InitZipOptions()

        # add all controls into master BoxSizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer1, 0, wx.BOTTOM | wx.EXPAND, border = 5)
        sizer.Add(hsizer3, 0, wx.EXPAND | wx.TOP, border = 10) # save folder select
        sizer.Add(hsizer2, 0, wx.TOP | wx.EXPAND, border = 20)
        sizer.Add(hsizer4, 0, wx.EXPAND | wx.TOP, border = 15)
        self.SetSizer(sizer)
        self.Layout()

    ''' intitalize the "Archive logs into a zip file" RadioBox, "Save current setting to zip files" Button and
        "Save zip file as" TextCtrl
    '''
    def InitZipOptions(self):
        """ zip options """
        # Zip or not option radio boxes
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        choices = ['No', 'Yes']
        radiobuttons = wx.RadioBox(
            self, -1, "Archive logs into a zip file", wx.DefaultPosition, wx.DefaultSize,
            choices, 2, wx.RA_SPECIFY_COLS
        )
        radiobuttons.SetSelection(self.zipoption)

        # zip file name control text
        zip_filename_statictxt = wx.StaticText(self, -1, "Save zip file as: ")
        zip_filename = wx.TextCtrl(self, -1, "log_files.zip", size = (300, -1))
        # Save zip option button
        savezipoption_button = wx.Button(self, -1, "Save current setting to zip files", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSaveZipOption, savezipoption_button)

        # add all parts to hsizer
        hsizer4.Add(radiobuttons, 0)
        hsizer4.Add((10, 0))
        hsizer4.Add(savezipoption_button, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer4.Add((10, 0), 0)
        hsizer4.Add(zip_filename_statictxt, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer4.Add(zip_filename, 1, wx.ALIGN_CENTER_VERTICAL)
        return hsizer4, radiobuttons, zip_filename

    ''' Intialize "Sort by..." ComboBox drop down selector that lets you sort the file list by file name, modified date, or file path '''
    def InitSortByOptions(self):
        sortingChoices = ["Sort files by...", "File name", "Modified date", "File path"]
        cb = wx.ComboBox(self, -1, "Sort files by...", (0, 0), (148, -1),
                         sortingChoices, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        # bind the button to OnSortColumnBySelection()
        self.Bind(wx.EVT_COMBOBOX, self.OnSortColumnBySelection, cb)
        return cb

    ''' Intialize the "Server" TextCtrl box that lets you specify what server to search '''
    def InitServernameTextCtrl(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # get the history of servers typed in
        server_history_choices = config.read_servername_history()

        servername_txtctrl = wx.TextCtrl(self, -1, size = (134, -1))
        # enable AutoComplete for the server name
        # use server_choices as choices for the AutoComplete
        servername_txtctrl.AutoComplete(server_history_choices)

        cb = self.InitSortByOptions()
        hsizer.Add(wx.StaticText(self, -1, "Server: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(servername_txtctrl, 0)
        hsizer.Add((30, 0), 0)
        hsizer.Add(cb, 0)
        return hsizer, servername_txtctrl, server_history_choices

    ''' intialize the "Path to the log files" textboxes and check boxes '''
    def InitCheckBoxes(self):

        description_text = wx.StaticText(self, -1, "Folders to search: ")
        cb1 = wx.CheckBox(self, -1, "ITXLogs")  # , (65, 40), (150, 20), wx.NO_BORDER)
        cb2 = wx.CheckBox(self, -1, "TXPlay")  # , (65, 60), (150, 20), wx.NO_BORDER)
        cb3 = wx.CheckBox(self, -1, "Other")  # , (65, 80), (150, 20), wx.NO_BORDER)

        # the default file paths to ITXLogs and TXPlay
        text1 = wx.TextCtrl(self, -1, BottomPanel.ITXLogPath)
        text2 = wx.TextCtrl(self, -1, BottomPanel.TXPlayLogPath)
        # set "Other" path
        self.otherpath_txtctrl = wx.TextCtrl(self, -1, "")

        #init Select folder for Other
        open_networkfolder_button = wx.Button(self, -1, "Select folder", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OpenNetworkFolderButton, open_networkfolder_button)
        checklist_group = [] # the list that holds the checkboxes
        checklist_group.append([cb1, text1])
        checklist_group.append([cb2, text2])
        checklist_group.append([cb3, self.otherpath_txtctrl])

        # add TextCtrl and CheckBoxs to BoxSizer
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(description_text, 0)
        for check, text in checklist_group[0:2]:
            vsizer.Add(check, 0, wx.ALIGN_LEFT | wx.TOP, 15)
            vsizer.Add(text, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)
        vsizer.Add(cb3, 0, wx.ALIGN_LEFT | wx.TOP, 10)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.otherpath_txtctrl, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)
        hsizer.Add((10, -1))
        hsizer.Add(open_networkfolder_button, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)

        vsizer.Add(hsizer, 1, wx.EXPAND)
        return vsizer, checklist_group

    ''' call SortBy method in top_panel class '''
    def OnSortColumnBySelection(self, event):
        self.top_panel.OnSortColumnBySelection(event)

    ''' Method that creates a DirDialog pop up window that lets the user choose a folder to search on the selected server
    The window is opened when the "Select folder" button next to "Other" in the "Path to the log files" section is pressed
    '''
    def OpenNetworkFolderButton(self, event):
        dlg = wx.DirDialog(
            self, message = "Choose a folder to search",
            defaultPath = "\\\\" + self.servername_txtctrl.GetLineText(0) + "\C$\\",
            # defaultFile = "",
            # wildcard = wildcard,
            style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )

        # self.otherpath_txtctrl = os.getcwd()
        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPath().lower()
            servername = self.get_servername().lower()
            if servername not in paths:
                PopupDialog.ErrorDialog.popup("You chose a local path. Please choose a path in the chosen server: " + servername, "", "", None)
            else:
                self.otherpath_txtctrl.SetLabel(paths[len(servername) + 3:])
                self.checklist_group[2][0].SetValue(True)
        # Compare this with the debug above; did we change working dirs?

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

    ''' Method that handles the 'Select folder to save files to'
        Pop ups a DirDialog to select a folder on the server
    '''
    def OpenFileButton(self, event):
        dlg = wx.DirDialog(
            self, message = "Choose a folder to save to",
            defaultPath = os.path.expanduser('~') + '\Desktop',
            # defaultFile = "",
            # wildcard = wildcard,
            style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPath()
            self.logdestination_text.SetLabel(paths)
        # Compare this with the debug above; did we change working dirs?

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

    ''' write the zip option to config.txt when 'Save current setting to zip file' button is pressed '''
    def OnSaveZipOption(self, event):
        config.write_config(self.get_zipoption())

    ''' return text in 'Folder to save files to' box '''
    def get_logdestinationpath(self):
        return self.logdestination_text.GetLineText(0)

    ''' get the currently selected 'Archive logs into a zip file' option
        either a yes or no
    '''
    def get_zipoption(self):
        return self.radiobuttons.GetSelection()

    ''' return text in 'Server' box '''
    def get_servername(self):
        return self.servername_txtctrl.GetLineText(0)

    ''' return zip file name in 'Save zip file as' '''
    def get_zip_filename(self):
        return self.zip_filename.GetLineText(0)
