import wx
import wx.aui
import wx.lib.agw.aui as aui

# If MainFrame subclasses wx.Frame, uncomment the following lines
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from gui.main_frame import MainFrame


# noinspection PyPep8Naming
class PopupMenu:
    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", tbman: "ToolBarManager") -> None:
    def __init__(self, frame: wx.Frame) -> None:
        self.frame = frame

    def bind_DropDownToolbarItem(self, ref_id: wx.WindowIDRef) -> None:
        self.frame.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN,
                        self.OnDropDownToolbarItem, id=ref_id)

    def OnDropDownToolbarItem(self, event: wx.aui.AuiToolBarEvent) -> None:
        if not event.IsDropDownClicked():
            return

        ref_id: wx.WindowIDRef = event.GetId()
        tb: wx.aui.AuiToolBar = event.GetEventObject()
        tb.SetToolSticky(ref_id, True)

        # create the popup menu
        menu_popup: wx.Menu = wx.Menu()
        bmp: wx.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))

        icon: wx.Bitmap
        label: str
        items: list[tuple[str, wx.Bitmap]]
        items = [("Drop Down Item 1", bmp), ("Drop Down Item 2", bmp),
                 ("Drop Down Item 3", bmp), ("Drop Down Item 4", bmp)]
        menu_item: wx.MenuItem
        for label, icon in items:
            menu_item = menu_popup.Append(wx.NewIdRef(), label)
            menu_item.SetBitmap(icon)

        self.frame.PopupMenu(menu_popup)

        # make sure the button is "un-stuck"
        tb.SetToolSticky(ref_id, False)
