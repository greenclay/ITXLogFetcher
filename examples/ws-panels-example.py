import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size = (300, 250))

        panel1 = wx.Panel(self, -1, style = wx.SUNKEN_BORDER)
        panel2 = wx.Panel(self, -1, style = wx.SUNKEN_BORDER)

        panel1.SetBackgroundColour("BLUE")
        panel2.SetBackgroundColour("RED")

        box1 = wx.BoxSizer(wx.VERTICAL)
        box2 = wx.BoxSizer(wx.VERTICAL)

        box1.Add(panel1, 2, wx.EXPAND)
        box2.Add(panel2, 1, wx.EXPAND)

        but1 = wx.Button(panel2, label = "Apply")

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        hbox.Add(but1, 1, wx.EXPAND)
        box1.Add()
        self.SetAutoLayout(True)

        self.Layout()


app = wx.PySimpleApp()
frame = MyFrame(None, -1, "Sizer Test")
frame.Show()
app.MainLoop()
