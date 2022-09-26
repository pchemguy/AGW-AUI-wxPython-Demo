import wx
import wx.aui
import wx.lib.agw.aui as aui

# If MainFrame subclasses wx.Frame, uncomment the following lines
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from gui.main_frame import MainFrame


# TODO: Update code, replace .AddSimpleTool with .AddTool (full version). See:
#       https://docs.wxpython.org/wx.aui.AuiToolBar.html#wx.aui.AuiToolBar.AddTool
#       https://wxpython.org/Phoenix/docs/html/wx.ToolBar.html#wx.ToolBar.AddTool
#       "demo~Core Windows/Controls~Toolbar" (and other tutorials)
# TODO: Each toolbar probably should be handled by a dedicated method.
class ToolBarManager:
    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    toolbar_ids: dict[int, str]  # wx.NewRefId -> Toolbar string id
    toolbars: dict[str, dict]  # {"<key>": {"id": <ref_id>, "item": <aui.AuiToolBar>}}
    item_ids: dict[int, str]  # wx.NewRefId -> Control string id
    items: dict[str, dict]  # {"<key>": {"id": <ref_id>, "item": <aui.AuiToolBarItem>}}

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager) -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager) -> None:
        self.frame = frame
        self.mgr = mgr
        self.toolbar_ids = {}
        self.toolbars = {}
        self.item_ids = {}
        self.items = {}
        self.init_toolbars()

    def init_toolbars(self):
        # If MainFrame subclasses wx.Frame, replace the following line
        # frame: "MainFrame" = self.frame
        frame: wx.Frame = self.frame
        mgr: aui.AuiManager = self.mgr

        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        frame.SetMinSize(wx.Size(400, 300))

        # prepare a few custom overflow elements for the toolbars' overflow buttons
        append_items: list[aui.AuiToolBarItem] = []
        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_SEPARATOR)
        append_items.append(item)

        item_id: int = wx.NewIdRef()
        item = aui.AuiToolBarItem()
        self.item_ids[item_id] = "CustomizeToolbar"
        self.items["CustomizeToolbar"] = {"id": item_id, "item": item}
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(item_id)
        item.SetLabel("Customize...")
        append_items.append(item)
        frame.Bind(wx.EVT_MENU, self.OnCustomizeToolbar, id=self.items["CustomizeToolbar"]["id"])

        # Popup menu id
        # The same popup menu is displayed for multiple toolbars, so
        # a single ref_id is associated with multiple toolbar items.
        item_id: int = wx.NewIdRef()
        self.item_ids[item_id] = "DropDownToolbarItem"
        self.items["DropDownToolbarItem"] = {"id": item_id, "item": None}
        # noinspection PyPep8Naming
        ID_DropDownToolbarItem: int = item_id

        # create some toolbars
        tb_id: int = wx.NewIdRef()
        tb1 = aui.AuiToolBar(frame, tb_id, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        self.toolbar_ids[tb_id] = "tb1"
        self.toolbars["tb1"] = {"id": tb_id, "item": tb1}
        tb1.SetToolBitmapSize(wx.Size(48, 48))
        tb1.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_ERROR))
        tb1.AddSeparator()
        tb1.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_QUESTION))
        tb1.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_INFORMATION))
        tb1.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        tb1.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.SetCustomOverflowItems([], append_items)
        tb1.Realize()
        mgr.AddPane(tb1, aui.AuiPaneInfo().Name("tb1").Caption("Big Toolbar").ToolbarPane().Top())

        tb_id: int = wx.NewIdRef()
        tb2 = aui.AuiToolBar(frame, tb_id, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        self.toolbar_ids[tb_id] = "tb2"
        self.toolbars["tb2"] = {"id": tb_id, "item": tb2}
        tb2.SetToolBitmapSize(wx.Size(16, 16))

        tb2_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSeparator()
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSeparator()
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.AddSimpleTool(wx.NewIdRef(), "Test", tb2_bmp1)
        tb2.SetCustomOverflowItems([], append_items)
        tb2.Realize()
        mgr.AddPane(tb2, aui.AuiPaneInfo().Name("tb2").Caption("Toolbar 2").ToolbarPane().Top().Row(1))

        tb_id: int = wx.NewIdRef()
        tb3 = aui.AuiToolBar(frame, tb_id, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        self.toolbar_ids[tb_id] = "tb3"
        self.toolbars["tb3"] = {"id": tb_id, "item": tb3}
        tb3.SetToolBitmapSize(wx.Size(16, 16))
        tb3_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16))
        tb3.AddSimpleTool(wx.NewIdRef(), "Check 1", tb3_bmp1, "Check 1", aui.ITEM_CHECK)
        tb3.AddSimpleTool(wx.NewIdRef(), "Check 2", tb3_bmp1, "Check 2", aui.ITEM_CHECK)
        tb3.AddSimpleTool(wx.NewIdRef(), "Check 3", tb3_bmp1, "Check 3", aui.ITEM_CHECK)
        tb3.AddSimpleTool(wx.NewIdRef(), "Check 4", tb3_bmp1, "Check 4", aui.ITEM_CHECK)
        tb3.AddSeparator()
        tb3.AddSimpleTool(wx.NewIdRef(), "Radio 1", tb3_bmp1, "Radio 1", aui.ITEM_RADIO)
        tb3.AddSimpleTool(wx.NewIdRef(), "Radio 2", tb3_bmp1, "Radio 2", aui.ITEM_RADIO)
        tb3.AddSimpleTool(wx.NewIdRef(), "Radio 3", tb3_bmp1, "Radio 3", aui.ITEM_RADIO)
        tb3.AddSeparator()
        tb3.AddSimpleTool(wx.NewIdRef(), "Radio 1 (Group 2)", tb3_bmp1, "Radio 1 (Group 2)", aui.ITEM_RADIO)
        tb3.AddSimpleTool(wx.NewIdRef(), "Radio 2 (Group 2)", tb3_bmp1, "Radio 2 (Group 2)", aui.ITEM_RADIO)
        tb3.AddSimpleTool(wx.NewIdRef(), "Radio 3 (Group 2)", tb3_bmp1, "Radio 3 (Group 2)", aui.ITEM_RADIO)
        tb3.SetCustomOverflowItems([], append_items)
        tb3.Realize()
        mgr.AddPane(tb3, aui.AuiPaneInfo().Name("tb3").Caption("Toolbar 3").ToolbarPane().Top().Row(1).Position(1))

        tb_id: int = wx.NewIdRef()
        tb4 = aui.AuiToolBar(frame, tb_id, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_TEXT | aui.AUI_TB_HORZ_TEXT)
        self.toolbar_ids[tb_id] = "tb4"
        self.toolbars["tb4"] = {"id": tb_id, "item": tb4}
        tb4.SetToolBitmapSize(wx.Size(16, 16))
        tb4_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        tb4.AddSimpleTool(ID_DropDownToolbarItem, "Item 1", tb4_bmp1)
        tb4.AddSimpleTool(wx.NewIdRef(), "Item 2", tb4_bmp1)
        tb4.AddSimpleTool(wx.NewIdRef(), "Item 3", tb4_bmp1)
        tb4.AddSimpleTool(wx.NewIdRef(), "Item 4", tb4_bmp1)
        tb4.AddSeparator()
        tb4.AddSimpleTool(wx.NewIdRef(), "Item 5", tb4_bmp1)
        tb4.AddSimpleTool(wx.NewIdRef(), "Item 6", tb4_bmp1)
        tb4.AddSimpleTool(wx.NewIdRef(), "Item 7", tb4_bmp1)
        tb4.AddSimpleTool(wx.NewIdRef(), "Item 8", tb4_bmp1)
        choice = wx.Choice(tb4, -1, choices=["One choice", "Another choice"])
        tb4.AddControl(choice)
        tb4.SetToolDropDown(ID_DropDownToolbarItem, True)
        tb4.Realize()
        mgr.AddPane(tb4, aui.AuiPaneInfo().Name("tb4").Caption("Bookmark Toolbar").ToolbarPane().Top().Row(2))

        tb_id: int = wx.NewIdRef()
        tb5 = aui.AuiToolBar(frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_VERTICAL)
        self.toolbar_ids[tb_id] = "tb5"
        self.toolbars["tb5"] = {"id": tb_id, "item": tb5}
        tb5.SetToolBitmapSize(wx.Size(48, 48))
        tb5.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_ERROR))
        tb5.AddSeparator()
        tb5.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_QUESTION))
        tb5.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_INFORMATION))
        tb5.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        tb5.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
        tb5.SetCustomOverflowItems([], append_items)
        tb5.Realize()
        mgr.AddPane(tb5, aui.AuiPaneInfo().Name("tb5").Caption("Vertical Toolbar").ToolbarPane().Left().GripperTop())

        tb_id: int = wx.NewIdRef()
        tb6 = aui.AuiToolBar(frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_VERT_TEXT)
        self.toolbar_ids[tb_id] = "tb6"
        self.toolbars["tb6"] = {"id": tb_id, "item": tb6}
        tb6.SetToolBitmapSize(wx.Size(48, 48))
        tb6.AddSimpleTool(wx.NewIdRef(), "Clockwise 1",
                          wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_OTHER, wx.Size(16, 16)))
        tb6.AddSeparator()
        tb6.AddSimpleTool(wx.NewIdRef(), "Clockwise 2",
                          wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16)))
        tb6.AddSimpleTool(ID_DropDownToolbarItem, "Clockwise 3",
                          wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_OTHER, wx.Size(16, 16)))
        tb6.SetCustomOverflowItems([], append_items)
        tb6.SetToolDropDown(ID_DropDownToolbarItem, True)
        tb6.Realize()
        mgr.AddPane(tb6, aui.AuiPaneInfo().Name("tb6").Caption("Vertical Clockwise Rotated Toolbar").
                    ToolbarPane().Right().GripperTop().TopDockable(False).BottomDockable(False))

        mgr.AddPane(wx.Button(frame, wx.ID_ANY, "Test Button"),
                    aui.AuiPaneInfo().Name("tb7").ToolbarPane().Top().Row(2).Position(1))

        # Show how to get a custom minimizing behaviour, i.e., to minimize a pane
        # inside an existing AuiToolBar
        tree = self.mgr.GetPane("test8")
        tree.MinimizeMode(aui.AUI_MINIMIZE_POS_TOOLBAR)
        toolbar_pane = self.mgr.GetPane(tb4)
        tree.MinimizeTarget(toolbar_pane)

        # "commit" all changes made to AuiManager
        self.mgr.Update()

    def OnCustomizeToolbar(self, _event: wx.CommandEvent) -> None:
        wx.MessageBox("Customize Toolbar clicked", "AUI Test")
