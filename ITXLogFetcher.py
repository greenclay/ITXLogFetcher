__author__ = 'Yuki Sawa, yukisawa@gmail.com'
import wx
from FilelistPanel import FilelistPanel
from OptionsPanel import OptionsPanel
from DataModel import DataModel


class ITXLogFetcher(wx.Frame):
    """ Main file that holds the main wxPython panel.
        intializes
    """

    def __init__(self, parent, title):
        super(ITXLogFetcher, self).__init__(parent, title=title, size=(750, 900), pos = (400, 100))

        panel = wx.Panel(self)

        self.options_panel = OptionsPanel(panel)
        self.filelist_panel = FilelistPanel(panel)
        self.options_panel.filelist_panel = self.filelist_panel
        self.filelist_panel.options_panel = self.options_panel
        DataModel.options_panel = self.options_panel

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.filelist_panel, 3, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        sizer.Add(self.options_panel, 1, wx.EXPAND | wx.ALL, border=10)
        panel.SetSizerAndFit(sizer)
        panel.Layout()
        self.Show()

        # self.testing()

    def testing(self):
        print "Running ITXLogFetcher.testing()"
        """ testing methods """
        DataModel.testing()
        # logfetcher.testing3()
        self.options_panel.testing1()
        self.filelist_panel.testing2()
        print len(self.filelist_panel.matchingfiles)
        print "FINISHED ITXLogFetcher.testing()"


class App(wx.App):
    def __init__(self):
        wx.App.__init__(self)

    def OnExit(self):
        pass


if __name__ == '__main__':
    app = App()
    frame = ITXLogFetcher(None, title = "ITX Log Fetcher ver 1.1")
    app.MainLoop()

