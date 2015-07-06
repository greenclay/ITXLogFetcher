__author__ = 'Administrator'
import wx
import os
import TextCtrlAutoComplete
import config

class OptionsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)
        self.logsource_list = []
        self.zipoption = config.read_config()
        # self.log_destination = os.getcwd()

        # Server choice controls
        hsizer1, self.logserver_txt = self.InitTextCtrlAutoComplete()

        # Initialize Radio Buttons with with log paths
        # hsizer2, self.radio_group = self.InitRadioButtons()
        hsizer2, self.checklist_group = self.InitCheckBoxes()

        # Controls for folder to copy the log files to
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        folderselect_button = wx.Button(self, -1, "Open", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OpenFileButton, folderselect_button)

        desktoppath = os.path.expanduser('~') + '\Desktop\logs'
        self.logdestination_text = wx.TextCtrl(self, -1, desktoppath, size = (200, -1))

        hsizer3.Add(wx.StaticText(self, -1, "Folder to copy logs to: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add(self.logdestination_text, 1, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add((10,0),0)
        hsizer3.Add(folderselect_button, 0, wx.ALIGN_CENTER_VERTICAL)

        """ zip options """
        # Zip or not option radio boxes
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        choices = ['No', 'Yes']
        self.radiobuttons = wx.RadioBox(
            self, -1, "Zip log files", wx.DefaultPosition, wx.DefaultSize,
            choices, 2, wx.RA_SPECIFY_COLS
        )
        self.radiobuttons.SetSelection(self.zipoption)

        # zip file name control text
        zip_filename_statictxt = wx.StaticText(self, -1, "File name: ")
        self.zip_filename = wx.TextCtrl(self, -1, "log_file.zip", size = (300, -1))

        # Save zip option button
        savezipoption_button = wx.Button(self, -1, "Save zip option", (25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSaveZipOption, savezipoption_button)

        hsizer4.Add(self.radiobuttons, 0)
        hsizer4.Add((10,0))
        hsizer4.Add(zip_filename_statictxt, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer4.Add(self.zip_filename, 1, wx.ALIGN_CENTER_VERTICAL)
        hsizer4.Add((10,0),0)
        hsizer4.Add(savezipoption_button, 0, wx.ALIGN_CENTER_VERTICAL)

        # add all controls into master BoxSizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer1, 0, wx.BOTTOM | wx.EXPAND, border = 5)
        sizer.Add(hsizer2, 0, wx.TOP | wx.EXPAND, border = 5)
        sizer.Add(hsizer3, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 5)
        sizer.Add(hsizer4, 0, wx.ALL | wx.EXPAND, border = 0)
        self.SetSizer(sizer)
        self.Layout()

    def InitZipOptions(self):
        pass

    def InitTextCtrlAutoComplete(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        default_server_choices = ["YUKI-PC", "ITX1503A", "ITX1503B", "ITX1511A", "ITX1511B"]
        # default_server_choices = ["YUKI-PC", "\\\ITX1503A\C$\\", "\\\ITX1503B\C$\\", "\\\ITX1511A\C$\\", "\\\ITX1511B\C$\\"]

        logserver_txt = TextCtrlAutoComplete.TextCtrlAutoComplete(self, choices = default_server_choices, dropDownClick=True)
        hsizer.Add(wx.StaticText(self, -1, "Server: "), 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(logserver_txt, 0)

        return hsizer, logserver_txt

    def InitCheckBoxes(self):
        cb1 = wx.CheckBox(self, -1, "ITXLogs")#, (65, 40), (150, 20), wx.NO_BORDER)
        cb2 = wx.CheckBox(self, -1, "MIRANDA")#, (65, 60), (150, 20), wx.NO_BORDER)
        cb3 = wx.CheckBox(self, -1, "Other")#, (65, 80), (150, 20), wx.NO_BORDER)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb1)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb2)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb3)
        text1 = wx.TextCtrl(self, -1, "ITXLogs")
        text2 = wx.TextCtrl(self, -1, "MIRANDA_LOGS\TXPLAY\TXPlayTrace")
        text3 = wx.TextCtrl(self, -1, "Users\Administrator.ADMINISTRATOR5\Desktop\A")

        checklist_group = []
        checklist_group.append([cb1, text1])
        checklist_group.append([cb2, text2])
        checklist_group.append([cb3, text3])

        hsizer = wx.BoxSizer(wx.VERTICAL)
        for check, text in checklist_group:
            hsizer.Add(check, 0, wx.ALIGN_LEFT | wx.TOP, 5)
            hsizer.Add(text, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)

        return hsizer, checklist_group


    def EvtCheckBox(self, event):
        selected = event.GetEventObject().GetLabel()
        if event.GetEventObject().GetValue():
            if event.GetEventObject().GetLabel() == "ITXLogs":
                self.logsource_list.append(["ITXLogs", self.checklist_group[0][1].GetLineText(0)])
            elif event.GetEventObject().GetLabel() == "MIRANDA":
                self.logsource_list.append(["MIRANDA", self.checklist_group[1][1].GetLineText(0)])
            elif event.GetEventObject().GetLabel() == "Other":
                self.logsource_list.append(["Other", self.checklist_group[2][1].GetLineText(0)])
        else:
            for i, label in enumerate(self.logsource_list):
                if event.GetEventObject().GetValue() == self.logsource_list[i][0]:
                    self.logsource_list.remove(self.logsource_list[i][0])

            # self.logsource_list.remove(event.GetEventObject().GetLabel())


    def InitRadioButtons(self):
        # instantiate RadioButton group
        radio_group = []
        radio1 = wx.RadioButton(self, -1, "ITXLogs", style = wx.RB_GROUP)
        radio2 = wx.RadioButton(self, -1, "MIRANDA")
        radio3 = wx.RadioButton(self, -1, "Other")
        text1 = wx.TextCtrl(self, -1, "ITXLogs")
        text2 = wx.TextCtrl(self, -1, "MIRANDA_LOGS\TXPLAY\TXPlayTrace")
        text3 = wx.TextCtrl(self, -1, "Users\Administrator.ADMINISTRATOR5\Desktop\A")
        radio_group.append((radio1, text1))
        radio_group.append((radio2, text2))
        radio_group.append((radio3, text3))
        text = wx.StaticText(self, -1, "Path to files:")
        # make sizer and add the controls in
        hsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(text, )
        for radio, text in radio_group:
            hsizer.Add(radio, 0, wx.ALIGN_LEFT | wx.TOP, 5)
            hsizer.Add(text, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)

        for radio, text in radio_group:
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButtonSelect, radio)

        self.logsource_txt = radio1.GetLabel()

        return hsizer, radio_group

    def OnRadioButtonSelect(self, event):
        radio_selected = event.GetEventObject()
        if radio_selected.GetLabel() == "ITXLogs":
            self.logsource_txt = self.radio_group[0][1].GetLineText(0)
        elif radio_selected.GetLabel() == "MIRANDA":
            self.logsource_txt = self.radio_group[1][1].GetLineText(0)
        elif radio_selected.GetLabel() == "Other":
            self.logsource_txt = self.radio_group[2][1].GetLineText(0)

        # for radio, text in self.group1_ctrls:
        #     if radio is radio_selected:
        #         text.Enable(True)
        #     else:
        #         text.Enable(False)


    def OpenFileButton(self, event):
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

    def OnSaveZipOption(self, event):
        config.write_config(self.get_zipoption())

    def get_logsourcepath(self):
        logpaths = []
        for check in self.checklist_group:
            if check[0].GetValue() == True:
                logpaths.append("\\\\" + self.logserver_txt.GetLineText(0) + "\C$\\" + check[1].GetValue())
        # logpaths = ["\\\\" + self.logserver_txt.GetLineText(0) + "\C$\\" + servername for label, servername in self.logsource_list]
        print "get_logsourcepath - " + str(logpaths)
        return logpaths

    def get_logdestinationpath(self):
        return self.logdestination_text.GetLineText(0)

    def get_zipoption(self):
        op = self.radiobuttons.GetSelection()
        return op

    def get_servername(self):
        return self.logserver_txt.GetLineText(0)