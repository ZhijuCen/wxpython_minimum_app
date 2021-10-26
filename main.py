
import wx
import wx.grid
import wx.adv

from PIL import Image

import datetime


def pil_to_wxBitmap(image: Image.Image):
    w, h = image.size
    bitmap = wx.Bitmap.FromBuffer(w, h, image.tobytes())
    return bitmap


class TaskIcon(wx.adv.TaskBarIcon):

    def __init__(self, icon, tooltip, iconType=wx.adv.TBI_DEFAULT_TYPE):
        super().__init__(iconType=iconType)
        self.SetIcon(icon, tooltip)
    
    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(wx.MenuItem(menu, wx.ID_OPEN, "Show"))
        menu.Append(wx.MenuItem(menu, wx.ID_EXIT, "Exit"))
        return menu


class MainWindow(wx.Frame):

    def __init__(self, window_title="", icon=None, icon_tooltip="", parent=None):
        super().__init__(parent)

        if icon is None:
            icon = wx.Icon()
            icon.CopyFromBitmap(pil_to_wxBitmap(
                Image.new(
                    "RGB",
                    (24, 24),
                    (128, 128, 128)
                )
            ))

        self.SetTitle(window_title)
        self.SetIcon(icon)
        self.Bind(wx.EVT_CLOSE, self.onEventMainWindowClose)

        self.initSysTrayIcon(icon, icon_tooltip)
        self.initUI()
        self.initTimer()

        self.Centre()
        self.Show()
    
    def initTimer(self):
        self.timer = wx.Timer(self.btn_timer)
        self.btn_timer.Bind(wx.EVT_TIMER, self.onEventTimerTimeout)
        self.btn_timer.Bind(wx.EVT_TOGGLEBUTTON, self.onBtnTimerToggled)

    def initUI(self):
        self.SetMinSize(wx.Size(320, 240))
        self.btn_timer = wx.ToggleButton(self, label="Timer")
        self.lable_currentTime = wx.StaticText(self, label="Initialized")
        vbox = wx.BoxSizer(wx.VERTICAL)
        gs = wx.GridSizer(1, 2, 5, 5)
        gs.AddMany([
            (self.btn_timer, 0, wx.EXPAND),
            (self.lable_currentTime, 0, wx.EXPAND)
        ])
        vbox.Add(gs, proportion=0, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def initSysTrayIcon(self, icon: wx.Icon, tooltip=""):
        self.sys_tray_icon = TaskIcon(icon, tooltip)
        self.sys_tray_icon.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.onEventShow)
        self.sys_tray_icon.Bind(wx.EVT_MENU, self.onEventShow, id=wx.ID_OPEN)
        self.sys_tray_icon.Bind(wx.EVT_MENU, self.onEventExit, id=wx.ID_EXIT)

    def onBtnTimerToggled(self, event):
        if self.btn_timer.GetValue() is True:
            self.timer.Start(100)
        else:
            self.timer.Stop()
    
    def onEventTimerTimeout(self, event):
        curr_time = str(datetime.datetime.now())
        self.lable_currentTime.SetLabelText(curr_time)
    
    def onEventMainWindowClose(self, event):
        self.Show(False)

    def onEventShow(self, event):
        self.Show()
    
    def onEventExit(self, event):
        self.sys_tray_icon.Destroy()
        self.Destroy()
    

if __name__ == "__main__":

    app = wx.App()
    main_window = MainWindow("Application")
    app.MainLoop()
