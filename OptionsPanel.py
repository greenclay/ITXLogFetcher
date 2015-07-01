__author__ = 'Administrator'
import wx
import os
from wx import TextCtrlAutoComplete



class OptionsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)

        self.log_destination = os.getcwd()

        # Server choice controls
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        default_server = "\\YUKI-PC\C$\\"
        default_server = "\\ITX1503A\C$\\"
        self.logserver_txt = wx.TextCtrl(self, -1, default_server)

        hsizer1.Add(wx.StaticText(self, -1, "Server: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer1.Add(self.logserver_txt, 0, wx.ALIGN_CENTER_VERTICAL)


        # Initialize Radio Buttons with log paths
        hsizer2 = self.InitRadioButtons()

        # hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        # self.logsource_txt = wx.TextCtrl(self, -1, "/Users/Administrator.ADMINISTRATOR5/Desktop/A", size = (700, -1))
        # hsizer2.Add(wx.StaticText(self, -1, "Log path: "), 0, wx.ALIGN_CENTER_VERTICAL)
        # hsizer2.Add(self.logsource_txt, 0, wx.ALIGN_CENTER_VERTICAL)


        # Controls for folder to copy the log files to

        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        folderselect_button = wx.Button(self, -1, "Open", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OpenFileButton, folderselect_button)

        desktoppath = os.path.expanduser('~') + '\Desktop\logs'
        self.logdestination_text = wx.TextCtrl(self, -1, desktoppath, size = (200, -1))

        hsizer3.Add(wx.StaticText(self, -1, "Folder to copy logs to: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add(self.logdestination_text, 1, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add(folderselect_button, 0, wx.ALIGN_CENTER_VERTICAL)

        # zip or not radio boxes
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        choices = ['Yes', 'No']
        self.radiobuttons = wx.RadioBox(
            self, -1, "Zip log files", wx.DefaultPosition, wx.DefaultSize,
            choices, 2, wx.RA_SPECIFY_COLS
        )
        hsizer4.Add(self.radiobuttons, 1)

        # add all controls into master BoxSizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer1, 0, wx.ALL | wx.EXPAND, border = 0)
        sizer.Add(hsizer2, 0, wx.ALL | wx.EXPAND, border = 0)
        sizer.Add(hsizer3, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 5)
        sizer.Add(hsizer4, 0, wx.ALL | wx.EXPAND, border = 0)
        self.SetSizer(sizer)
        self.Layout()

    def InitRadioButtons(self):
        # instantiate RadioButton group
        self.radio_group = []
        radio1 = wx.RadioButton(self, -1, " ITXLogs ", style = wx.RB_GROUP)
        radio2 = wx.RadioButton(self, -1, " MIRANDA ")
        radio3 = wx.RadioButton(self, -1, " Other ")
        text1 = wx.TextCtrl(self, -1, "ITXLogs")
        text2 = wx.TextCtrl(self, -1, "MIRANDA_LOGS\TXPLAY\TXPlayTrace")
        text3 = wx.TextCtrl(self, -1, "")
        self.radio_group.append((radio1, text1))
        self.radio_group.append((radio2, text2))
        self.radio_group.append((radio3, text3))

        text = wx.StaticText(self, -1, "Path to files:")
        # make sizer and add the controls in
        hsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(text, )
        for radio, text in self.radio_group:
            hsizer.Add(radio, 0, wx.ALIGN_LEFT  | wx.TOP, 5)
            hsizer.Add(text, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)

        return hsizer

    def OpenFileButton(self, evt):
        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'open' dialog, and allows multitple
        # file selections as well.
        #
        # Finally, if the directory is changed in the process of getting files, this
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.DirDialog(
            self, message = "Choose a file",
            defaultPath = os.path.expanduser('~') + '\Desktop',
            # defaultFile = "",
            # wildcard = wildcard,
            style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )

        self.log_destination = os.getcwd()
        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPath()
            self.log_destination = paths
            self.logdestination_text.SetLabel(paths)
        # Compare this with the debug above; did we change working dirs?

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

    def get_logsourcepath(self):
        return self.logserver_txt.GetLineText(0) + self.logsource_txt.GetLineText(0)

    def get_logdestinationpath(self):
        return self.logdestination_text.GetLineText(0)
