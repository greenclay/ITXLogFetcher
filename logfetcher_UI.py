#!/usr/bin/python

# simple.py

import wx
import wx.calendar

import logfetcher


from datetime import date

class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(500,500))

        # self.Maximize()
        # self.InitUITwoVerticalBoxSizer()
        self.InitUI2()
        self.Centre()
        self.Show()

    def pathUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        sourceText = wx.StaticText(self.panel, label="Location of logs")
        hbox.Add(sourceText, 0, wx.LEFT, 10)

        # Date FROM MONTH control box
        self.log_source = wx.TextCtrl(self.panel, 0, "//YUKI-PC/C$/Users/Administrator.ADMINISTRATOR5/Desktop/A", size=(500,20))
        hbox.Add(self.log_source, 1, wx.ALL | wx.LEFT, 10)

        return hbox

    def dateUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # labeling text
        fromText = wx.StaticText(self.panel, label="From")
        hbox.Add(fromText, 0, wx.LEFT | wx.RIGHT, 0)

        # Date FROM MONTH control box
        self.date_from_month = wx.TextCtrl(self.panel, 0, "6", size=(50,20))
        hbox.Add(self.date_from_month, 1, wx.LEFT | wx.RIGHT, 5)

        # Date FROM DAY text control box
        self.date_from_day = wx.TextCtrl(self.panel, 0, "24", size=(50,20))
        hbox.Add(self.date_from_day, 1, wx.LEFT | wx.RIGHT, 5)

        # labeling text
        toText = wx.StaticText(self.panel, label="To")
        hbox.Add(toText, 0, wx.LEFT, 10)

        # Date TO MONTH control box
        self.date_to_month = wx.TextCtrl(self.panel, 1, "6", size=(50,20))
        hbox.Add(self.date_to_month, 1, wx.LEFT | wx.RIGHT, 5)

        # Date TO DAY text control box
        self.date_to_day = wx.TextCtrl(self.panel, 0, "25", size=(50,20))
        hbox.Add(self.date_to_day, 1, wx.LEFT | wx.RIGHT, 5)

        return hbox

    def InitUI2(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self, size=(500,500))

        self.matchingfiles = []
        self.filelist = wx.ListBox(self.panel, 0, wx.DefaultPosition, (400,200), [], wx.LB_SINGLE)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.filelist, 1, wx.LEFT | wx.RIGHT | wx.ALL, 10)
        vbox.Add(hbox2, 1, wx.ALIGN_CENTRE)

        # DATEs

        hbox1 = self.dateUI()
        hbox2 = self.pathUI()

        vbox.Add(hbox1, 1, wx.ALIGN_CENTRE | wx.TOP)
        vbox.Add(hbox2, 1, wx.ALIGN_CENTRE | wx.TOP)


        # get button
        getButton = wx.Button(self.panel, label="Apply")
        getButton.Bind(wx.EVT_BUTTON, self.OnGet)
        hbox1.Add(getButton, 0, wx.ALL | wx.LEFT, 10)

        self.SetAutoLayout(True)
        self.SetSizer(vbox)

    def OnGet(self, event):
        date_to_day = int(self.date_to_day.GetLineText(0))
        date_to_month = int(self.date_to_month.GetLineText(0))
        date_to = date(2015, date_to_month, date_to_day)
        date_from_day = int(self.date_from_day.GetLineText(0))
        date_from_month = int(self.date_from_month.GetLineText(0))
        date_from = date(2015, date_from_month, date_from_day)

        log_path = self.log_source.GetLineText(0)
        matchingfiles = logfetcher.main(log_source_path=log_path ,datefrom=date_from, datetto=date_to)

        self.filelist.Clear()
        for file in matchingfiles:
            self.filelist.Append(file[1])

    def InitUITwoVerticalBoxSizer(self):

        vbox = wx.BoxSizer(wx.VERTICAL)
        vboxLeft = wx.BoxSizer(wx.VERTICAL)
        vboxRight = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(vboxLeft, wx.LEFT | wx.ALL, border=10)
        vbox.Add(vboxRight, wx.RIGHT | wx.ALL, border=10)

        panelr = wx.Panel(self)
        panelr.SetBackgroundColour('#000000')
        vboxRight.Add(panelr,flag=wx.RIGHT | wx.ALL, border=10)
        panelr.SetSizer(vboxRight)

        panell = wx.Panel(self)
        panell.SetBackgroundColour('#FFFFFF')
        vboxLeft.Add(panelr,flag=wx.LEFT | wx.ALL, border=10)
        panell.SetSizer(vboxLeft)

        # panel = wx.Panel(self)
        # panel.SetBackgroundColour('#FFFFFF')
        # vboxLeft.Add(panel, flag=wx.ALL, border=10)

        # st_filenames = wx.StaticText(filenames_panel, label="files names")

    def InitUIPanelInside(self):
        menubar = wx.MenuBar()
        filem = wx.Menu()

        menubar.Append(filem, '&File')
        self.SetMenuBar(menubar)

        panel = wx.Panel(self)
        panel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)

        midPan = wx.Panel(panel)
        midPan.SetBackgroundColour('#ededed')

        vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 20)
        panel.SetSizer(vbox)
        # wx.TextCtrl(self)

app = wx.App()
# window = wx.Frame(None, style=wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION |	 wx.CLOSE_BOX)
# window.Show()
ex = Example(None, title="Size")
app.MainLoop()