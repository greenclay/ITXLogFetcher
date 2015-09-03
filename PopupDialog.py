__author__ = 'Yuki Sawa, yukisawa@gmail.com'

import wx
from DataModel import DataModel
'''
Class that represents pop up windows that appear when there is an error or file operation occuring
'''
"""
ProgressDialog is called when "Search for files" or "Save selected files to folder" button is pressed and displays a progress bar
"""
class ProgressDialog:
    def __init__(self, panel, thread, message):
        self.abort = False
        self.panel = panel
        self.dialog = wx.ProgressDialog(message,
                                message,
                                parent = self.panel,
                                style = wx.PD_APP_MODAL
                                        | wx.PD_CAN_ABORT
                                        | wx.PD_ELAPSED_TIME
                                )

        while 1:
            wx.MilliSleep(250)
            cont, skip = self.dialog.Pulse() #continue, skip.
            # When the "Cancel" button is pressed, Pulse() returns cont=false
            if cont == False:
                thread.abort = True
            if thread.done:
                self.dialog.Destroy()
                break
"""
    ErrorDialog is a pop-up window that shows when the user enters invalid information for the Servername or
    the system can not find the folder paths
"""
class ErrorDialog(object):
    @staticmethod
    def popup(errorcode, path, servername, thread):
        if thread is not None:
            thread.abort = True
        print "\nERROR\n" + errorcode + "\n" + servername + "\n" + path + "\n"
        if "Error 53" in errorcode or "Error 1396" in errorcode:
            dlg = wx.MessageDialog(DataModel.options_panel, errorcode + "\n" + servername, 'Error', wx.OK | wx.ICON_INFORMATION)
        else:
            dlg = wx.MessageDialog(DataModel.options_panel, errorcode + "\n" + path, 'Error', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()