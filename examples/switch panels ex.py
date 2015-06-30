import wx
import wx.grid as gridlib

########################################################################
class PanelOne(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.s=parent
        self.txt = wx.TextCtrl(self)
        button =wx.Button(self, label="Save", pos=(200, 0))
        button.Bind(wx.EVT_BUTTON, self.Check)

    def Check(self,event):
        passw=self.txt.GetValue()
        if  passw=="1":
            print "true"
            self.s.onSwitchPanels(self)


########################################################################
class PanelTwo(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        grid = gridlib.Grid(self)
        grid.CreateGrid(25,12)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.EXPAND)
        self.SetSizer(sizer)
        button =wx.Button(self, label="Save", pos=(0, 500))
        button.Bind(wx.EVT_BUTTON, parent.onSwitchPanels)
class PanelThree(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        txt = wx.TextCtrl(self)
        button =wx.Button(self, label="Save", pos=(200, 325))
        button.Bind(wx.EVT_BUTTON, parent.onSwitchPanels)

########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Panel Switcher Tutorial",
                          size=(800,600))

        self.panel_one = PanelOne(self)
        self.panel_two = PanelTwo(self)
        self.panel_three = PanelThree(self)
        self.panel_two.Hide()
        self.panel_three.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY,
                                                  "Switch Panels",
                                                  "Some text")
        self.Bind(wx.EVT_MENU, self.onSwitchPanels,
                  switch_panels_menu_item)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    #----------------------------------------------------------------------
    def onSwitchPanels(self, event):

        if self.panel_one.IsShown():
           self.SetTitle("Panel Two Showing")
           self.panel_one.Hide()
           self.panel_two.Show()
           self.panel_three.Hide()
        elif self.panel_two.IsShown() or self.panel_three.IsShown():

           self.SetTitle("Panel One Showing")
           self.panel_one.Show()
           self.panel_two.Hide()
           self.panel_three.Hide()
        else:
             self.SetTitle("Panel Three Showing")
             self.panel_one.Hide()
             self.panel_two.Hide()
             self.panel_three.Show()


        self.Layout()

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()