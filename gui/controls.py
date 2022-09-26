import wx
import wx.grid
import wx.html
import wx.lib.agw.aui as aui

# If MainFrame subclasses wx.Frame, uncomment the following lines
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from gui.main_frame import MainFrame

from gui.resources import overview


class Singleton(type):
    """Singleton metaclass."""

    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class GridCtrl(metaclass=Singleton):
    """Factory for a grid control."""

    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    create_menu_id: wx.WindowIDRef
    counter: int = 0

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager,
    #              create_menu_id: wx.WindowIDRef) -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 create_menu_id: wx.WindowIDRef) -> None:
        self.frame = frame
        self.mgr = mgr
        self.create_menu_id = create_menu_id
        frame.Bind(wx.EVT_MENU, self.OnCreate, id=self.create_menu_id)

    def start_position(self) -> wx.Point:
        return self.frame.ClientToScreen(wx.Point(0, 0)) + (wx.Point(20, 20) * self.__class__.counter)

    def create_ctrl(self) -> wx.grid.Grid:
        self.__class__.counter += 1
        grid = wx.grid.Grid(self.frame, wx.ID_ANY, wx.Point(0, 0), wx.Size(150, 250),
                            wx.NO_BORDER | wx.WANTS_CHARS)
        grid.CreateGrid(50, 20)
        return grid

    def OnCreate(self, _event: wx.CommandEvent) -> None:
        ctrl: wx.grid.Grid = self.create_ctrl()
        caption = "Grid"
        self.mgr.AddPane(ctrl, aui.AuiPaneInfo().Caption(caption).Float().
                         FloatingPosition(self.start_position()).FloatingSize(wx.Size(300, 200)).
                         CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        self.mgr.Update()
        ctrl.Refresh()


class TextCtrl(metaclass=Singleton):
    """Factory for a text control."""

    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    create_menu_id: wx.WindowIDRef
    counter: int = 0

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager,
    #              create_menu_id: wx.WindowIDRef) -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 create_menu_id: wx.WindowIDRef) -> None:
        self.frame = frame
        self.mgr = mgr
        self.create_menu_id = create_menu_id
        frame.Bind(wx.EVT_MENU, self.OnCreate, id=self.create_menu_id)

    def start_position(self) -> wx.Point:
        return self.frame.ClientToScreen(wx.Point(0, 0)) + (wx.Point(20, 20) * self.__class__.counter)

    def create_ctrl(self, text: str = "", width: int = 150, height: int = 90) -> wx.TextCtrl:
        self.__class__.counter += 1
        if text.strip():
            text_ctrl = text
        else:
            text_ctrl = f"This is text box #{self.__class__.counter}."
        return wx.TextCtrl(self.frame, wx.ID_ANY, text_ctrl, wx.DefaultPosition,
                           wx.Size(width, height), style=wx.NO_BORDER | wx.TE_MULTILINE)

    def OnCreate(self, _event: wx.CommandEvent) -> None:
        ctrl: wx.TextCtrl = self.create_ctrl()
        caption = "Text Control"
        self.mgr.AddPane(ctrl, aui.AuiPaneInfo().Caption(caption).Float().
                         FloatingPosition(self.start_position()).MinimizeButton(True))
        self.mgr.Update()
        ctrl.Refresh()

        self.mgr.Update()


class TreeCtrl(metaclass=Singleton):
    """Factory for a tree control."""

    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    create_menu_id: wx.WindowIDRef
    counter: int = 0

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager,
    #              create_menu_id: wx.WindowIDRef) -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 create_menu_id: wx.WindowIDRef) -> None:
        self.frame = frame
        self.mgr = mgr
        self.create_menu_id = create_menu_id
        frame.Bind(wx.EVT_MENU, self.OnCreate, id=self.create_menu_id)

    def start_position(self) -> wx.Point:
        return self.frame.ClientToScreen(wx.Point(0, 0)) + (wx.Point(20, 20) * self.__class__.counter)

    def create_ctrl(self) -> wx.TreeCtrl:
        self.__class__.counter += 1
        tree: wx.TreeCtrl = wx.TreeCtrl(self.frame, wx.ID_ANY, wx.Point(0, 0), wx.Size(160, 250),
                                        wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        imglist: wx.ImageList = wx.ImageList(16, 16, True, 2)
        icons = [wx.ART_FOLDER, wx.ART_FILE_OPEN, wx.ART_NORMAL_FILE]
        for icon in icons:
            imglist.Add(wx.ArtProvider.GetBitmap(icon, wx.ART_OTHER, wx.Size(16, 16)))
        tree.AssignImageList(imglist)
        root: wx.TreeItemId = tree.AddRoot("AUI Project", 0)
        tree.SetItemImage(root, 1, wx.TreeItemIcon_Expanded)
        node_id: wx.TreeItemId
        for i in range(1, 6):
            node_id = tree.AppendItem(root, "Item " + str(i), 0)
            tree.SetItemImage(node_id, 1, wx.TreeItemIcon_Expanded)
            [tree.AppendItem(node_id, "Item " + str(j), 2) for j in range(1, 6)]
        tree.Expand(root)
        return tree

    def OnCreate(self, _event: wx.CommandEvent) -> None:
        ctrl: wx.TreeCtrl = self.create_ctrl()
        caption = "Tree Control"
        self.mgr.AddPane(ctrl, aui.AuiPaneInfo().Caption(caption).Float().
                         FloatingPosition(self.start_position()).CloseButton(True).
                         MaximizeButton(True).MinimizeButton(True))
        self.mgr.Update()
        ctrl.Refresh()


class HTMLCtrl(metaclass=Singleton):
    """Factory for an html control."""

    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    create_menu_id: wx.WindowIDRef
    counter: int = 0

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager,
    #              create_menu_id: wx.WindowIDRef) -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 create_menu_id: wx.WindowIDRef) -> None:
        self.frame = frame
        self.mgr = mgr
        self.create_menu_id = create_menu_id
        frame.Bind(wx.EVT_MENU, self.OnCreate, id=self.create_menu_id)

    def start_position(self) -> wx.Point:
        return self.frame.ClientToScreen(wx.Point(0, 0)) + (wx.Point(20, 20) * self.__class__.counter)

    def create_ctrl(self, parent: wx.Frame = None, width: int = 400, height: int = 300) -> wx.html.HtmlWindow:
        self.__class__.counter += 1
        if not parent:
            parent = self.frame
        ctrl = wx.html.HtmlWindow(parent, wx.ID_ANY, wx.DefaultPosition, wx.Size(width, height))
        ctrl.SetPage(overview)
        return ctrl

    def OnCreate(self, _event: wx.CommandEvent) -> None:
        ctrl: wx.html.HtmlWindow = self.create_ctrl()
        caption = "HTML Control"
        self.mgr.AddPane(ctrl, aui.AuiPaneInfo().Caption(caption).Float().
                         FloatingPosition(self.start_position()).FloatingSize(wx.Size(300, 200)).
                         CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        self.mgr.Update()
        ctrl.Refresh()


# noinspection PyPep8Naming
class SizeReportCtrl(metaclass=Singleton):
    """Factory for a utility control reporting its client size."""

    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    create_menu_id: wx.WindowIDRef
    counter: int = 0

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager,
    #              create_menu_id: wx.WindowIDRef) -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 create_menu_id: wx.WindowIDRef) -> None:
        self.frame = frame
        self.mgr = mgr
        self.create_menu_id = create_menu_id
        frame.Bind(wx.EVT_MENU, self.OnCreate, id=self.create_menu_id)

    def create_ctrl(self, width: int = 80, height: int = 80) -> wx.Control:
        self.__class__.counter += 1
        ctrl = wx.Control(self.frame, wx.ID_ANY, wx.DefaultPosition,
                          wx.Size(width, height), style=wx.NO_BORDER)
        ctrl.Bind(wx.EVT_PAINT, self.OnPaint)
        ctrl.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        ctrl.Bind(wx.EVT_SIZE, self.OnSize)
        return ctrl

    def start_position(self) -> wx.Point:
        return self.frame.ClientToScreen(wx.Point(0, 0)) + (wx.Point(20, 20) * self.__class__.counter)

    def OnCreate(self, _event: wx.CommandEvent) -> None:
        ctrl: wx.Control = self.create_ctrl()
        caption = "Client Size Reporter"
        self.mgr.AddPane(ctrl, aui.AuiPaneInfo().Caption(caption).Float().
                         FloatingPosition(self.start_position()).CloseButton(True).
                         MaximizeButton(True).MinimizeButton(True))
        self.mgr.Update()
        ctrl.Refresh()

    def OnEraseBackground(self, _event: wx.EraseEvent) -> None:
        pass  # intentionally empty

    def OnSize(self, event: wx.SizeEvent) -> None:
        ctrl: wx.Control = event.GetEventObject()
        ctrl.Refresh()

    def OnPaint(self, event: wx.PaintEvent) -> None:
        ctrl: wx.Control = event.GetEventObject()
        dc = wx.PaintDC(ctrl)
        dc.SetFont(wx.NORMAL_FONT)
        dc.SetBrush(wx.WHITE_BRUSH)

        size = ctrl.GetClientSize()
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)

        pi = self.mgr.GetPane(self)

        s = f"Size: {size.x} x {size.y}"
        w, height = dc.GetTextExtent(s)
        height += 3
        dc.DrawText(s, (size.x - w) // 2, (size.y - height * 5) // 2)

        s = f"Layer: {pi.dock_layer}"
        w, h = dc.GetTextExtent(s)
        dc.DrawText(s, (size.x - w) // 2, (size.y - height * 5) // 2 + height * 1)

        s = f"Dock: {pi.dock_direction} Row: {pi.dock_row}"
        w, h = dc.GetTextExtent(s)
        dc.DrawText(s, (size.x - w) // 2, (size.y - height * 5) // 2 + height * 2)

        s = f"Position: {pi.dock_pos}"
        w, h = dc.GetTextExtent(s)
        dc.DrawText(s, (size.x - w) // 2, (size.y - height * 5) // 2 + height * 3)

        s = f"Proportion: {pi.dock_proportion}"
        w, h = dc.GetTextExtent(s)
        dc.DrawText(s, (size.x - w) // 2, (size.y - height * 5) // 2 + height * 4)
