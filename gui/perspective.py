import wx
import wx.lib.agw.aui as aui


PERSPECTIVE_BUFFER_SIZE: int = 6


class LayoutManager:
    frame: wx.Frame
    mgr: aui.AuiManager
    mb_items: dict
    # {layout_ref_id: {"name": "<layout_name>", "data": "<layout_data>"}}
    layouts: dict[wx.WindowIDRef, dict[str, str]]
    layout_ids: list[wx.WindowIDRef]

    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 mb_items: dict) -> None:
        self.frame = frame
        self.mgr = mgr
        self.mb_items = mb_items
        self.layouts = {}
        self.layout_ids = wx.NewIdRef(PERSPECTIVE_BUFFER_SIZE)

        frame.Bind(wx.EVT_MENU, self.OnCreate, id=mb_items["CreatePerspective"]["id"])
        frame.Bind(wx.EVT_MENU, self.OnCopy, id=mb_items["CopyPerspectiveCode"]["id"])
        frame.Bind(wx.EVT_MENU, self.OnRestore, id=self.layout_ids[0], id2=self.layout_ids[-1])

    def save(self, name: str = "") -> bool:
        """Saves perspective/layout or copies to clipboard.

        If name is blank, copy layout to clipboard.

        Returns
          True if the buffer is not full.
          False if the buffer is full.
        Raises:
          IndexError if buffer is full.
        """
        if not name:
            clipboard: wx.TheClipboard = wx.TheClipboard
            if not clipboard.Open():
                raise SystemError("Clipboard error.")
            clipboard.SetData(wx.TextDataObject(self.mgr.SavePerspective()))
            clipboard.Close()
            return len(self.layouts) < PERSPECTIVE_BUFFER_SIZE
        layout_index: int = len(self.layouts)
        if layout_index == PERSPECTIVE_BUFFER_SIZE:
            raise IndexError("Cannot save perspective. The buffer is full.")
        layout_id: wx.WindowIDRef = self.layout_ids[layout_index]
        self.layouts[layout_id] = {
            "name": name,
            "data": self.mgr.SavePerspective()
        }
        menu: wx.Menu = self.mb_items["FramePerspectives"]
        if layout_index == 0:
            menu.AppendSeparator()
        menu.Append(self.layout_ids[layout_index], name)
        buffer_available: bool = layout_index + 1 < PERSPECTIVE_BUFFER_SIZE
        if not buffer_available:
            item: wx.MenuItem = self.mb_items["CreatePerspective"]["item"]
            item.Enable(False)
            item.SetHelp("Perspective buffer is full.")
        return buffer_available

    def restore(self, ref_id: wx.WindowIDRef) -> None:
        if ref_id not in self.layouts:
            raise ValueError("Bad perspective ID.")
        self.mgr.LoadPerspective(self.layouts[ref_id]["data"])

    def OnCreate(self, event: wx.CommandEvent) -> None:
        dlg = wx.TextEntryDialog(self.frame, "Enter a name for the new perspective:", "AUI Test")
        dlg.SetValue(f"Perspective {len(self.layouts) + 1}")
        if dlg.ShowModal() != wx.ID_OK:
            return
        name: str = dlg.GetValue()
        self.save(name)

    def OnCopy(self, _event: wx.CommandEvent) -> None:
        self.save()

    def OnRestore(self, event: wx.CommandEvent) -> None:
        self.restore(event.GetId())
