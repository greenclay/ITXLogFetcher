import wx
class ProgressDialog:
    def __init__(self, panel):
        print "__INIT__"
        message = "Copying files..."
        max = 100
        self.abort = False
        self.panel = panel
        self.dialog = wx.ProgressDialog("Running...",
                                message,
                                maximum = max,
                                parent = self.panel,
                                style =
                                          wx.PD_APP_MODAL
                                        | wx.PD_CAN_ABORT
                                        | wx.PD_CAN_SKIP
                                        | wx.PD_ELAPSED_TIME
                                # | wx.PD_ESTIMATED_TIME
                                # | wx.PD_REMAINING_TIME
                                # | wx.PD_AUTO_HIDE
                                )

        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(250)
            wx.Yield()
            print "Yielding"
            if count >= max / 2:
                (keepGoing, skip) = self.dialog.Pulse()
            else:
                (keepGoing, skip) = self.dialog.Pulse()
            # self.dialog.Destroy()

            if self.abort == True:
                break
        self.dialog.Destroy()

    def destroy(self):
        print "DESTROY"
        self.dialog.Destroy()
