import wx
import wx.aui
import wx.html
import wx.lib.agw.aui as aui
import wx.lib.embeddedimage

from gui.aui_notebook import Notebook
from gui.aui_notebook_options_res import (
    agw_style_flags as agw_flags, agw_tabart_provider as tabarts,
    agw_style_flag_masks as agw_masks, AUI_NB_CLOSE_MASK,
    default_checked_menus as check_menus)
from gui.resources import CUSTOM_TAB_BUTTONS


# noinspection PyPep8Naming
class NotebookOptions:
    frame: wx.Frame
    mgr: aui.AuiManager
    notebook_ctrl: Notebook
    flags: dict[wx.WindowIDRef, int]     # <menu_ref_id> -> AGW Window style flag
    themes: dict[wx.WindowIDRef, dict]   # <menu_ref_id> -> AGW TabArt provider dict
    mb_items: dict                       # menubar.items
    item_ids: dict[wx.WindowIDRef, str]  # menubar.item_ids

    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager, notebook_ctrl: Notebook,
                 menubar_items: dict, item_ids: dict[wx.WindowIDRef, str]) -> None:
        self.frame = frame
        self.mgr = mgr
        self.notebook_ctrl = notebook_ctrl
        self.mb_items = menubar_items
        self.item_ids = item_ids
        self.init_maps()
        self.init_ui_state()
        self.bind_menu()

    def init_maps(self):
        """Generate mappings for source identification in event handlers."""
        key: str
        self.flags = {self.mb_items[key]["id"]: agw_flags[key] for key in agw_flags}
        self.themes = {self.mb_items[key]["id"]: tabarts[key] for key in tabarts}

    def init_ui_state(self):
        """Sets menu items according to default Notebook startup flags.

        See defaults for notebook_ctrl.notebook_style. For simplicity, presently
        not checking for the actual value, but assume the default configuration.
        """
        key: str
        menu_item: wx.MenuItem
        for key in check_menus:
            menu_item = self.mb_items[key]["item"]
            menu_item.Check()

    def bind_menu(self):
        mb_items: dict = self.mb_items
        menu_refid: wx.WindowIDRef
        for menu_refid in self.flags:
            self.frame.Bind(wx.EVT_MENU, self.OnNotebookFlag, menu_refid)
        self.frame.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=mb_items["NotebookNoCloseButton"]["id"])
        for menu_refid in self.themes:
            self.frame.Bind(wx.EVT_MENU, self.OnNotebookTheme, menu_refid)

        self.frame.Bind(wx.EVT_MENU, self.OnNotebookDclickUnsplit, id=mb_items["NotebookDclickUnsplit"]["id"])
        self.frame.Bind(wx.EVT_MENU, self.OnCustomTabButtons, id=mb_items["NotebookCustomButtons"]["id"])
        self.frame.Bind(wx.EVT_MENU, self.OnMinMaxTabWidth, id=mb_items["NotebookMinMaxWidth"]["id"])
        self.frame.Bind(wx.EVT_MENU, self.OnAddMultiLine, id=mb_items["NotebookMultiLine"]["id"])
        self.frame.Bind(wx.EVT_MENU, self.OnPreview, id=mb_items["NotebookPreview"]["id"])
        self.frame.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, self.OnAllowNotebookDnD)
        self.frame.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)

    def OnNotebookTheme(self, event: wx.CommandEvent) -> None:
        """Update notebook theme (TabArt provider)."""
        event_id: wx.WindowIDRef = event.GetId()
        if self.notebook_ctrl.notebook_theme == self.themes[event_id]["rowid"]:
            return
        self.notebook_ctrl.notebook_theme = self.themes[event_id]["rowid"]
        art_provider = self.themes[event_id]["provider"]()

        nb: aui.AuiNotebook
        for nb in self.notebook_ctrl.all_notebooks():
            nb.SetArtProvider(art_provider)
            nb.Refresh()
            nb.Update()

    def OnNotebookFlag(self, event: wx.CommandEvent) -> None:
        """Updates GUI AGW style flag state based on menu events."""
        agwFlags: int = self.notebook_ctrl.notebook_style
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

        self.notebook_ctrl.notebook_style = agwFlags

        nb: aui.AuiNotebook
        for nb in self.notebook_ctrl.all_notebooks():
            # Demonstrate how to reset a close button on a tab. In this case,
            # only reset if one of the AUI_NB_CLOSE_* options is clicked (second
            # conditional) and the old state has the AUI_NB_CLOSE_ON_ALL_TABS.
            if (nb.GetAGWWindowStyleFlag() & aui.AUI_NB_CLOSE_ON_ALL_TABS and
                    flag_mask & AUI_NB_CLOSE_MASK):
                nb.SetCloseButton(page_idx=2, hasCloseButton=True)

            nb.SetAGWWindowStyleFlag(agwFlags)

            # Demonstrate how to remove a close button from a tab.
            # This method is only allowed if SetAGWWindowStyleFlag sets the
            # AUI_NB_CLOSE_ON_ALL_TABS flag ("NotebookCloseButtonAll" event).
            if event_id == self.mb_items["NotebookCloseButtonAll"]["id"]:
                nb.SetCloseButton(page_idx=2, hasCloseButton=False)

            nb.Refresh()
            nb.Update()

    def OnNotebookDclickUnsplit(self, event: wx.CommandEvent) -> None:
        nb: aui.AuiNotebook
        for nb in self.notebook_ctrl.all_notebooks():
            nb.SetSashDClickUnsplit(event.IsChecked())

    def OnCustomTabButtons(self, event: wx.CommandEvent) -> None:
        checked: bool = event.IsChecked()
        self.notebook_ctrl.custom_tab_buttons = checked
        nb: aui.AuiNotebook = self.mgr.GetPane("notebook_content").window

        btn_img: wx.lib.embeddedimage.PyEmbeddedImage
        aui_id: int
        for btn_img, aui_id in CUSTOM_TAB_BUTTONS["Left"]:
            if checked:
                nb.AddTabAreaButton(aui_id, wx.LEFT, btn_img.GetBitmap())
            else:
                nb.RemoveTabAreaButton(aui_id)

        right_btn: dict = CUSTOM_TAB_BUTTONS["Right"]
        for btn_img, aui_id in right_btn:
            if checked:
                nb.AddTabAreaButton(aui_id, wx.RIGHT, btn_img.GetBitmap())
            else:
                nb.RemoveTabAreaButton(aui_id)

        nb.Refresh()
        nb.Update()

    def OnMinMaxTabWidth(self, _event: wx.CommandEvent) -> None:
        nb: aui.AuiNotebook = self.mgr.GetPane("notebook_content").window
        min_tab_width, max_tab_width = nb.GetMinMaxTabWidth()
        dlg = wx.TextEntryDialog(self.frame, "Enter the minimum and maximum tab widths, separated by a comma:",
                                 "AuiNotebook Tab Widths")
        dlg.SetValue(f"{min_tab_width},{max_tab_width}")
        if dlg.ShowModal() != wx.ID_OK:
            return
        value: str = dlg.GetValue()
        dlg.Destroy()

        try:
            min_tab_width, max_tab_width = value.split(",")
            min_tab_width, max_tab_width = int(min_tab_width), int(max_tab_width)
        except:
            dlg = wx.MessageDialog(self.frame, "Invalid minimum/maximum tab width. Tab widths "
                                               "should be 2 integers separated by a comma.",
                                   "Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        if min_tab_width > max_tab_width:
            dlg = wx.MessageDialog(self, "Invalid minimum/maximum tab width. Minimum tab width "
                                         "should be less of equal than maximum tab width.",
                                   "Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        nb.SetMinMaxTabWidth(min_tab_width, max_tab_width)

        nb.Refresh()
        nb.Update()

    def OnAddMultiLine(self, _event: wx.CommandEvent) -> None:
        nb: aui.AuiNotebook = self.mgr.GetPane("notebook_content").window
        nb.InsertPage(1, wx.TextCtrl(nb, -1, "Some more text", wx.DefaultPosition,
                                     wx.DefaultSize, wx.TE_MULTILINE | wx.NO_BORDER),
                      "Multi-Line\nTab Labels", True)
        nb.SetPageTextColour(1, wx.BLUE)

    def OnPreview(self, _event: wx.CommandEvent) -> None:
        nb: aui.AuiNotebook = self.mgr.GetPane("notebook_content").window
        nb.NotebookPreview()

    def OnAllowNotebookDnD(self, event: aui.AuiNotebookEvent) -> None:
        # for the purpose of this test application, explicitly
        # allow all notebook drag and drop events
        event.Allow()

    def OnNotebookPageClose(self, event: aui.AuiNotebookEvent) -> None:
        ctrl = event.GetEventObject()
        if isinstance(ctrl.GetPage(event.GetSelection()), wx.html.HtmlWindow):
            res = wx.MessageBox("Are you sure you want to close/hide this notebook page?",
                                "AUI", wx.YES_NO, self.frame)
            if res != wx.YES:
                event.Veto()
