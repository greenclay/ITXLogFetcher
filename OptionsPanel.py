__author__ = 'Administrator'
import wx
import os
import config

import DataModel

class OptionsPanel(wx.Panel):
    ''' Methods to set varibles up for quick testing'''

    def testing1(self):
        self.servername_txtctrl.SetValue("YUKI-PC")
        self.checklist_group[0][0].SetValue(True)
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)
        self.logsource_list = []
        self.zipoption = config.read_config()

        ''' Server choice controls '''
        hsizer1, self.servername_txtctrl, self.server_choices = self.InitServernameTextCtr()

        ''' Initialize check buttons with log path controls'''
        hsizer2, self.checklist_group = self.InitCheckBoxes()

        ''' Intialize controls for folder to copy the log files to '''
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        folderselect_button = wx.Button(self, -1, "Open", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OpenFileButton, folderselect_button)

        desktoppath = os.path.expanduser('~') + '\Desktop\logs'
        self.logdestination_text = wx.TextCtrl(self, -1, desktoppath, size = (200, -1))
        self.logdestination_text.AutoCompleteDirectories()

        hsizer3.Add(wx.StaticText(self, -1, "Folder to copy logs to: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add(self.logdestination_text, 1, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add((10, 0), 0)
        hsizer3.Add(folderselect_button, 0, wx.ALIGN_CENTER_VERTICAL)

        ''' zip options control '''
        hsizer4, self.radiobuttons, self.zip_filename = self.InitZipOptions()

        # add all controls into master BoxSizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer1, 0, wx.BOTTOM | wx.EXPAND, border = 5)
        sizer.Add(hsizer2, 0, wx.TOP | wx.EXPAND, border = 5)
        sizer.Add(hsizer3, 0, wx.EXPAND | wx.TOP, border = 15)
        sizer.Add(hsizer4, 0, wx.EXPAND | wx.TOP, border = 15)
        self.SetSizer(sizer)
        self.Layout()


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
        zip_filename_statictxt = wx.StaticText(self, -1, "File name: ")
        zip_filename = wx.TextCtrl(self, -1, "log_file.zip", size = (300, -1))
        # Save zip option button
        savezipoption_button = wx.Button(self, -1, "Save current zip file config", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSaveZipOption, savezipoption_button)

        hsizer4.Add(radiobuttons, 0)
        hsizer4.Add((10, 0))
        hsizer4.Add(savezipoption_button, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer4.Add((10, 0), 0)
        hsizer4.Add(zip_filename_statictxt, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer4.Add(zip_filename, 1, wx.ALIGN_CENTER_VERTICAL)
        return hsizer4, radiobuttons, zip_filename


    def InitSortByOptions(self):
        """ INITIALIZE Sort by column selector Combo box """
        sortingChoices = ["Sort files by...", "File name", "Modified date", "File path"]
        cb = wx.ComboBox(self, -1, "Sort files by...", (0, 0), (148, -1),
                         sortingChoices, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.OnSortColumnByDate, cb)

        return cb

    def InitServernameTextCtr(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        server_choices = config.read_servername_history()

        # servername_txtctrl = TextCtrlAutoComplete.TextCtrlAutoComplete(self, choices = default_server_choices, dropDownClick=True)
        servername_txtctrl = wx.TextCtrl(self, -1, size = (134, -1))
        servername_txtctrl.AutoComplete(server_choices)

        cb = self.InitSortByOptions()
        hsizer.Add(wx.StaticText(self, -1, "Server: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(servername_txtctrl, 0)
        hsizer.Add((30, 0), 0)
        hsizer.Add(cb, 0)
        return hsizer, servername_txtctrl, server_choices

    def InitCheckBoxes(self):
        description_text = wx.StaticText(self, -1, "Paths to the log files: ")
        cb1 = wx.CheckBox(self, -1, "ITXLogs")  # , (65, 40), (150, 20), wx.NO_BORDER)
        cb2 = wx.CheckBox(self, -1, "MIRANDA")  # , (65, 60), (150, 20), wx.NO_BORDER)
        cb3 = wx.CheckBox(self, -1, "Other")  # , (65, 80), (150, 20), wx.NO_BORDER)
        text1 = wx.TextCtrl(self, -1, "ITXLogs")
        text2 = wx.TextCtrl(self, -1, "MIRANDA_LOGS\TXPLAY\TXPlayTrace")
        self.otherpath_txtctrl = wx.TextCtrl(self, -1, "")

        open_networkfolder_button = wx.Button(self, -1, "Open", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OpenNetworkFolderButton, open_networkfolder_button)
        checklist_group = []
        checklist_group.append([cb1, text1])
        checklist_group.append([cb2, text2])
        checklist_group.append([cb3, self.otherpath_txtctrl])

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(description_text, 0)
        for check, text in checklist_group[0:2]:
            vsizer.Add(check, 0, wx.ALIGN_LEFT | wx.TOP, 5)
            vsizer.Add(text, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)
        vsizer.Add(cb3, 0, wx.ALIGN_LEFT | wx.TOP, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.otherpath_txtctrl, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)
        hsizer.Add((10, -1))
        hsizer.Add(open_networkfolder_button, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)

        vsizer.Add(hsizer, 1, wx.EXPAND)
        return vsizer, checklist_group

    def OnSortColumnByDate(self, event):
        self.filelist_panel.OnSortColumnByDate(event)

    def OpenNetworkFolderButton(self, event):
        dlg = wx.DirDialog(
            self, message = "Choose a file",
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
            paths = dlg.GetPath()
            servername = self.get_servername()
            if servername not in paths:
                self.filelist_panel.ErrorDialog("You chose a local path. Please choose a path in the chosen server: " + servername, "", "")
            self.otherpath_txtctrl.SetLabel(paths[len(servername) + 6:])
        # Compare this with the debug above; did we change working dirs?

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

    def OpenFileButton(self, event):
        dlg = wx.DirDialog(
            self, message = "Choose a file",
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

    def OnSaveZipOption(self, event):
        config.write_config(self.get_zipoption())

    def get_logsourcepath(self):
        logpaths = []
        for check in self.checklist_group:
            if check[0].GetValue() == True:
                logpaths.append("\\\\" + self.servername_txtctrl.GetLineText(0) + "\C$\\" + check[1].GetValue())
        return logpaths

    def get_logdestinationpath(self):
        return self.logdestination_text.GetLineText(0)

    def get_zipoption(self):
        op = self.radiobuttons.GetSelection()
        return op

    def get_servername(self):
        return self.servername_txtctrl.GetLineText(0)
