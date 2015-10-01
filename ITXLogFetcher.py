
import wx
from TopPanel import TopPanel
from BottomPanel import BottomPanel
from DataModel import DataModel

'''              CONTAINS MAIN METHOD              '''

class ITXLogFetcher(wx.Frame):
    """ Main file that holds the main wxPython panel.
        intializes BottomPanel and TopPanel and DataModel
    """

    def __init__(self, parent, title):
        super(ITXLogFetcher, self).__init__(parent, title=title, size=(750, 900), pos = (400, 100))

        panel = wx.Panel(self)

        # initialize OptionsPanel and FilelistPanel, pass their references to each other
        # also pass it to DataModel
        self.bottom_panel = BottomPanel(panel)
        self.top_panel = TopPanel(panel)
        self.bottom_panel.top_panel = self.top_panel
        self.top_panel.bottom_panel = self.bottom_panel
        DataModel.bottom_panel = self.bottom_panel

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.top_panel, 3, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        sizer.Add(self.bottom_panel, 1, wx.EXPAND | wx.ALL, border=10)

        # init the panel and layout, then Show() it
        panel.SetSizerAndFit(sizer)
        panel.Layout()
        self.Show()

        # for testing
        # self.testing()


    """ testing methods """
    def testing(self):
        print "Running ITXLogFetcher.testing()"
        DataModel.testing()
        # logfetcher.testing3()
        self.bottom_panel.testing1()
        self.top_panel.testing2()
        print len(self.top_panel.matchingfiles)
        print "FINISHED ITXLogFetcher.testing()"


''' init wx.App class which contains entire app '''
class App(wx.App):
    def __init__(self):
        wx.App.__init__(self)

    def OnExit(self):
        pass

''' __main__ method for entire app '''
if __name__ == '__main__':
    app = App()
    frame = ITXLogFetcher(None, title = "ITX Log Fetcher ver 1.1")
    app.MainLoop()

