import wx
import wx.lib.agw.aui as aui

from gui.aui_dockart_options_res import gradient_menu


class DockArtOptions:
    frame: wx.Frame
    mgr: aui.AuiManager
    mb_items: dict                       # menubar.items
    item_ids: dict[wx.WindowIDRef, str]  # menubar.item_ids

    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 menubar_items: dict, item_ids: dict[wx.WindowIDRef, str]) -> None:
        self.frame = frame
        self.mgr = mgr
        self.mb_items = menubar_items
        self.item_ids = item_ids

    def bind_menu(self):
        menu_key: str
        for menu_key in gradient_menu:
            self.frame.Bind(wx.EVT_MENU, self.OnGradient, id=self.mb_items[menu_key]["id"])

    def OnGradient(self, event: wx.CommandEvent) -> None:
        gradient_key: str = self.item_ids[event.GetId()]
        self.mgr.GetArtProvider().SetMetric(
            aui.AUI_DOCKART_GRADIENT_TYPE,
            gradient_menu[gradient_key])
        self.mgr.Update()
