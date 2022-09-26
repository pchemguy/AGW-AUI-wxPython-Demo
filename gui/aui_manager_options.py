import wx
import wx.aui
import wx.lib.agw.aui as aui

from gui.aui_manager_options_res import (
    agw_style_flags as agw_flags, agw_style_flag_masks as agw_masks,
    default_checked_menus as checked_menus)


class ManagerOptions:
    frame: wx.Frame
    mgr: aui.AuiManager
    flags: dict[wx.WindowIDRef, int]     # <menu_ref_id> -> AGW style flag
    mb_items: dict                       # menubar.items
    item_ids: dict[wx.WindowIDRef, str]  # menubar.item_ids

    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 menubar_items: dict, item_ids: dict[wx.WindowIDRef, str]) -> None:
        self.frame = frame
        self.mgr = mgr
        self.mb_items = menubar_items
        self.item_ids = item_ids
        self.init_maps()
        self.init_ui_state()
        self.bind_menu()

    def init_maps(self):
        """Generate mappings for source identification in event handlers."""
        key: str
        self.flags = {self.mb_items[key]["id"]: agw_flags[key] for key in agw_flags}

    def init_ui_state(self):
        """Sets menu items according to default Manager startup flags."""
        key: str
        menu_item: wx.MenuItem
        for key in checked_menus:
            menu_item = self.mb_items[key]["item"]
            menu_item.Check()

    def bind_menu(self):
        mb_items: dict = self.mb_items
        menu_refid: wx.WindowIDRef
        for menu_refid in self.flags:
            self.frame.Bind(wx.EVT_MENU, self.OnManagerFlag, menu_refid)
        self.frame.Bind(wx.EVT_MENU, self.OnManagerFlag, id=mb_items["StandardGuides"]["id"])
        self.frame.Bind(wx.EVT_MENU, self.OnManagerFlag, id=mb_items["NoHint"]["id"])

    def OnManagerFlag(self, event: wx.CommandEvent) -> None:
        """Updates GUI AGW style flag state based on menu events."""
        agwFlags: int = self.mgr.GetAGWFlags()
        event_id: wx.WindowIDRef = event.GetId()
        menu_key: str = self.item_ids[event_id]
        # If menu item is a part of a RADIO group, clear all associated group flags.
        if menu_key in agw_masks:
            agwFlags &= ~agw_masks[menu_key]
        """
        Note that a click toggles the state of a CHECK flag and sets a RADIO flag
        on. The code above checks if the flag is a part of RADIO group and clears
        the group before setting the target flag (only one member of a RADIO
        group can be set at a time). This way, for a RADIO flag, it must be set
        from the pre-cleared state, that is, its state is toggled. Thus, after
        pre-clearing the state of the affected RADIO group, if appropriate, the
        new state is set by toggling the old, but pre-cleared state below. If the
        item is a CHECK flag, its state is also toggled.
        Some RADIO groups use all-cleared-flags state as a separate base state
        (flags are just bits, but RADIO items are menu items, so there is no
        conflict here). This state is not part of the <flags> dict and will set
        the flag_mask to 0. In this case, the previous clear-group operation
        updates the state completely, and no other flag requires updating.   
        """
        flag_mask: int = self.flags.get(event_id, 0)
        if flag_mask:  # Toggle flag state.
            old_flag_state: int = agwFlags & flag_mask
            new_flag_state: int = ~old_flag_state & flag_mask
            agwFlags = agwFlags & ~flag_mask | new_flag_state

        self.mgr.SetAGWFlags(agwFlags)
        self.mgr.DoUpdate()
