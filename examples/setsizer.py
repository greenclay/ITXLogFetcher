import wx

class Frm(wx.Frame):
   # def __init__(self, *args, **kwargs):
   #    super(Frm, self).__init__(*args, **kwargs)
   #    txt = wx.TextCtrl(self)
   #    s = wx.BoxSizer(wx.HORIZONTAL)
   #    s.Add(txt, 1)
   #    self.SetSizer(s)
   #    self.Layout()

   def __init__(self, *args, **kwargs):
      super(Frm, self).__init__(*args, **kwargs)

      sizer = wx.BoxSizer(wx.VERTICAL)

      # paths to copy the log files to
      hsizer3 = wx.BoxSizer(wx.HORIZONTAL)

      folderselect_button = wx.Button(self, -1, "Select folder")
      # self.Bind(wx.EVT_BUTTON, self.OpenFileButton, folderselect_button)

      self.logdestination_text = wx.TextCtrl(self, -1, "/Users/Administrator.ADMINISTRATOR5/Desktop/A", size=(-1,-1))

      hsizer3.Add(wx.StaticText(self, -1, "Folder to copy logs to: "), 0, wx.ALIGN_CENTER_VERTICAL)
      hsizer3.Add(self.logdestination_text, 1, wx.ALIGN_CENTER_VERTICAL)
      hsizer3.Add(folderselect_button, 0)

      sizer.Add(hsizer3, 1, wx.EXPAND)
      self.SetSizer(sizer)
app = wx.PySimpleApp()
frame = Frm(None)
frame.Show()
app.MainLoop()