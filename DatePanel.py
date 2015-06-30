import wx


class DatePanelBoxSizer(wx.BoxSizer):
    def __init__(self, parent, panel):
        """Constructor"""
        # wx.Panel.__init__(self, parent, size=(500,100))
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        # self.panel = wx.BoxSizer(self)

        self.panel = panel
        self.datepick = wx.DatePickerCtrl(self.panel, -1, pos = (20, 15),
                                          style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.datepick.Bind(wx.EVT_DATE_CHANGED, self.onAction)
        self.label = wx.StaticText(self.panel, -1, "", pos = (20, 50))

        self.Add(self.datepick, 0)
        self.Add(self.label, 0)

    def onAction(self, event):
        '''Process data from picked date'''
        selected = self.datepick.GetValue()
        month = selected.Month + 1
        day = selected.Day
        year = selected.Year
        date_str = "%02d/%02d/%4d" % (month, day, year)
        self.label.SetLabel("Date selected = {}".format(date_str))


class DatePanel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        # wx.Panel.__init__(self, parent, size=(500,100))
        wx.Panel.__init__(self, parent, size = wx.DefaultSize)
        # self.panel = wx.Panel(self)
        self.datepick = wx.DatePickerCtrl(self, -1, pos = (20, 15),
                                          style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.datepick.Bind(wx.EVT_DATE_CHANGED, self.onAction)
        self.label = wx.StaticText(self, -1, "", pos = (20, 50))
        self.BackgroundColour = "red"

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.datepick, 0)
        sizer.Add(self.label, 0)
        self.SetSizer(sizer)

    def onAction(self, event):
        '''Process data from picked date'''
        selected = self.datepick.GetValue()
        month = selected.Month + 1
        day = selected.Day
        year = selected.Year
        date_str = "%02d/%02d/%4d" % (month, day, year)
        self.label.SetLabel("Date selected = {}".format(date_str))


class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, size = mysize)
        # --Panel so it look good on all platforms
        self.panel = wx.Panel(self)
        self.datepick = wx.DatePickerCtrl(self.panel, -1, pos = (20, 15),
                                          style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.datepick.Bind(wx.EVT_DATE_CHANGED, self.onAction)
        self.label = wx.StaticText(self.panel, -1, "", pos = (20, 50))

    def onAction(self, event):
        '''Process data from picked date'''
        selected = self.datepick.GetValue()
        month = selected.Month + 1
        day = selected.Day
        year = selected.Year
        date_str = "%02d/%02d/%4d" % (month, day, year)
        self.label.SetLabel("Date selected = {}".format(date_str))

        # app = wx.App()
        # MyFrame(None, 'DatePickerCtrl', (350, 240)).Show()
        # app.MainLoop()
