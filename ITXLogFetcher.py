__author__ = 'YSawa@DIRECTV.com'
import wx
from FilelistPanel import FilelistPanel
from OptionsPanel import OptionsPanel

class MainFrame(wx.Frame):
    """Main Frame holding the main panel."""
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(700,800), pos=(500,100))
        panel = wx.Panel(self)

        self.a = "a"
        self.options_panel = OptionsPanel(panel)
        self.filelist_panel = FilelistPanel(panel, self.options_panel)
        self.options_panel.filelist_panel = self.filelist_panel

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.filelist_panel, 3, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border = 10)
        sizer.Add(self.options_panel, 1, wx.EXPAND | wx.ALL, border = 10)
        panel.SetSizerAndFit(sizer)
        panel.Layout()
        self.Show()


app = wx.App()
ex = MainFrame(None, title="ITX Log Fetcher ver 1.0")
app.MainLoop()