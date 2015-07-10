__author__ = 'YSawa@DIRECTV.com'
import wx
import config
from FilelistPanel import FilelistPanel
from OptionsPanel import OptionsPanel


class ITXLogFetcher(wx.Frame):
    """Main Frame holding the main panel."""

    def __init__(self, parent, title):
        super(ITXLogFetcher, self).__init__(parent, title = title, size = (700, 800), pos = (500, 100))

        panel = wx.Panel(self)

        self.options_panel = OptionsPanel(panel)
        self.filelist_panel = FilelistPanel(panel)
        self.options_panel.filelist_panel = self.filelist_panel
        self.filelist_panel.options_panel = self.options_panel

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.filelist_panel, 3, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border = 10)
        sizer.Add(self.options_panel, 1, wx.EXPAND | wx.ALL, border = 10)
        panel.SetSizerAndFit(sizer)
        panel.Layout()
        self.Show()

        """ testing methods """
        self.options_panel.testing1()
        self.filelist_panel.testing2()
        print len(self.filelist_panel.matchingfiles)

class App(wx.App):
    def __init__(self):
        wx.App.__init__(self)

    def OnExit(self):
        pass

if __name__ == '__main__':

    app = App()
    frame = ITXLogFetcher(None, title = "ITX Log Fetcher ver 1.0")
    app.MainLoop()
