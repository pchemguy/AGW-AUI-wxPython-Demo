"""Builds menubar.

This class relies on the order-preserving behavior of the stock Python
dictionary for both top-level menu labels and menu items.
"""

import wx
import wx.lib.agw.aui as aui

from gui.main_menu_res import main_menu_items

# If MainFrame subclasses wx.Frame, uncomment the following lines
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from gui.main_frame import MainFrame


# noinspection PyPep8Naming
class MainMenu:
    initialized: bool = False
    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    menubar: wx.MenuBar
    # wx.NewRefId -> Item string id
    item_ids: dict[wx.WindowIDRef, str]
    # {"<key>": Union[{"id": "<ref_id>", "type": "<type>", "item": "<wx.MenuItem>"}, "<wx.Menu>"]}
    items: dict

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager) -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager) -> None:
        self.frame = frame
        self.mgr = mgr
        self.menubar = wx.MenuBar()
        self.item_ids = {}
        self.items = {}
        self.build()
        frame.SetMenuBar(self.menubar)

    def art_provider(self) -> aui.AuiDefaultDockArt:
        return self.mgr.GetArtProvider()

    def build(self) -> wx.MenuBar:
        assert not self.initialized
        self.initialized = True

        menubar = self.menubar
        for child_key, child in main_menu_items.items():
            menu = self.build_menu(child["children"])
            self.items[child_key] = menu
            menubar.Append(menu, child["label"])
        self.build_standard()
        return menubar

    def build_menu(self, children: dict) -> wx.Menu:
        """Builds wx.Menu, including submenus (recursively)

        Args:
          children: {"<child_key>": {"type": "<type>", "label": "<label>", "children": "<children>"}}

        Returns:
          wx.Menu tree.
        """
        menu: wx.Menu = wx.Menu()
        child_key: str
        child: dict
        submenu: wx.Menu
        for child_key, child in children.items():
            child_label: str = child["label"]
            child_type: str = child.get("type", "basic")
            if child_type == "submn":
                submenu = self.build_menu(child["children"])
                self.items[child_key] = submenu
                menu.AppendSubMenu(submenu, child_label)
            else:
                self.append_menu_line(menu, child_key, child_label, child_type)
        return menu

    def append_menu_line(self, menu: wx.Menu, item_key: str, item_label: str,
                         item_type: str, item_id: wx.WindowIDRef = wx.ID_ANY) -> None:
        menu_item: wx.MenuItem
        if not item_label:
            menu_item = menu.AppendSeparator()
            self.items[item_key] = {"id": 0, "type": item_type, "item": menu_item}
            return
        if item_id == wx.ID_ANY:
            item_id = wx.NewIdRef()
        if item_type == "basic":
            menu_item = menu.Append(item_id, item_label)
        elif item_type == "radio":
            menu_item = menu.AppendRadioItem(item_id, item_label)
        elif item_type == "check":
            menu_item = menu.AppendCheckItem(item_id, item_label)
        else:
            raise ValueError(f"Unknown menu item type: <{item_type}>")
        self.item_ids[item_id] = item_key
        self.items[item_key] = {"id": item_id, "type": item_type, "item": menu_item}

    def build_standard(self):
        self.items["File"].Append(wx.ID_EXIT, "E&xit\tAlt-F4")
        self.frame.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.items["Help"].Append(wx.ID_ABOUT)
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

    def OnAbout(self, _event: wx.CommandEvent) -> None:
        msg = "wx.aui Demo\nAn advanced library for wxWidgets"
        dlg = wx.MessageDialog(self.frame, msg, "About wx.aui Demo", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, _event: wx.CommandEvent) -> None:
        self.frame.Close(True)
