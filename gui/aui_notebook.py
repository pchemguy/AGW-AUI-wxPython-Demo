import wx
import wx.aui
import wx.lib.agw.aui as aui

from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    # If MainFrame subclasses wx.Frame, uncomment the following line
    # from gui.main_frame import MainFrame
    from controls import HTMLCtrl


class Singleton(type):
    """Singleton metaclass."""

    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class Notebook:
    """Factory for a notebook control."""

    # If MainFrame subclasses wx.Frame, replace the following line
    # frame: "MainFrame"
    frame: wx.Frame

    mgr: aui.AuiManager
    create_menu_id: wx.WindowIDRef
    html_ctrl: "HTMLCtrl"
    notebook_style: int = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
    notebook_theme: int = 0
    custom_tab_buttons: bool
    main_notebook: aui.AuiNotebook
    counter: int = 0

    # If MainFrame subclasses wx.Frame, replace the following line
    # def __init__(self, frame: "MainFrame", mgr: aui.AuiManager,
    #              create_menu_id: wx.WindowIDRef,
    #              html_ctrl: "HTMLCtrl") -> None:
    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager,
                 create_menu_id: wx.WindowIDRef,
                 html_ctrl: "HTMLCtrl") -> None:
        self.frame = frame
        self.mgr = mgr
        self.html_ctrl = html_ctrl
        self.create_menu_id = create_menu_id
        frame.Bind(wx.EVT_MENU, self.OnCreate, id=self.create_menu_id)

    def start_position(self) -> wx.Point:
        return self.frame.ClientToScreen(wx.Point(0, 0)) + (wx.Point(20, 20) * self.__class__.counter)

    def all_notebooks(self) -> list[aui.AuiNotebook]:
        """Returns a list of existing AGW AuiNotebook objects."""
        nbs: list[aui.AuiNotebook] = []
        pane: aui.AuiPaneInfo
        for pane in self.mgr.GetAllPanes():
            if isinstance(pane.window, aui.AuiNotebook):
                nbs.append(pane.window)
        return nbs

    def create_ctrl(self) -> aui.AuiNotebook:
        # If MainFrame subclasses wx.Frame, replace the following line
        # frame: "MainFrame" = self.frame
        frame: wx.Frame = self.frame
        self.__class__.counter += 1

        # create the notebook off-window to avoid flicker
        client_size: wx.Size = frame.GetClientSize()
        ctrl: aui.AuiNotebook = aui.AuiNotebook(frame, wx.ID_ANY, wx.Point(*client_size),
                                                wx.Size(430, 200), agwStyle=self.notebook_style)
        # type: list[Type[wx.aui.AuiTabArt]]
        arts = [aui.AuiDefaultTabArt, aui.AuiSimpleTabArt, aui.VC71TabArt,
                aui.FF2TabArt, aui.VC8TabArt, aui.ChromeTabArt]

        ctrl.SetArtProvider(arts[self.notebook_theme]())

        page_bmp: wx.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,
                                                       wx.ART_OTHER, wx.Size(16, 16))
        ctrl.AddPage(self.html_ctrl.create_ctrl(ctrl), "Welcome to AUI", False, page_bmp)

        panel: wx.Panel = wx.Panel(ctrl, wx.ID_ANY)
        flex: wx.FlexGridSizer = wx.FlexGridSizer(rows=0, cols=2, vgap=2, hgap=2)
        flex.Add((5, 5))
        flex.Add((5, 5))
        flex.Add(wx.StaticText(panel, wx.ID_ANY, "wxTextCtrl:"), 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        flex.Add(wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(100, -1)),
                 1, wx.ALL | wx.ALIGN_CENTRE, 5)
        flex.Add(wx.StaticText(panel, wx.ID_ANY, "wxSpinCtrl:"), 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        flex.Add(wx.SpinCtrl(panel, wx.ID_ANY, "5", wx.DefaultPosition, wx.DefaultSize,
                             wx.SP_ARROW_KEYS, 5, 50, 5), 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        flex.Add((5, 5))
        flex.Add((5, 5))
        flex.AddGrowableRow(0)
        flex.AddGrowableRow(3)
        flex.AddGrowableCol(1)
        panel.SetSizer(flex)
        ctrl.AddPage(panel, "Disabled", False, page_bmp)
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE | wx.NO_BORDER), "DClick Edit!", False, page_bmp)
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some more text", wx.DefaultPosition,
                                 wx.DefaultSize, wx.TE_MULTILINE | wx.NO_BORDER), "Blue Tab")
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some more text", wx.DefaultPosition,
                                 wx.DefaultSize, wx.TE_MULTILINE | wx.NO_BORDER), "A Control")
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some more text", wx.DefaultPosition,
                                 wx.DefaultSize, wx.TE_MULTILINE | wx.NO_BORDER), "wxTextCtrl 4")
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some more text", wx.DefaultPosition,
                                 wx.DefaultSize, wx.TE_MULTILINE | wx.NO_BORDER), "wxTextCtrl 5")
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some more text", wx.DefaultPosition,
                                 wx.DefaultSize, wx.TE_MULTILINE | wx.NO_BORDER), "wxTextCtrl 6")
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE | wx.NO_BORDER), "wxTextCtrl 7 (longer title)")
        ctrl.AddPage(wx.TextCtrl(ctrl, wx.ID_ANY, "Some more text", wx.DefaultPosition,
                                 wx.DefaultSize, wx.TE_MULTILINE | wx.NO_BORDER), "wxTextCtrl 8")

        # Demonstrate how to disable a tab
        if self.__class__.counter == 1:
            ctrl.EnableTab(1, False)

        ctrl.SetPageTextColour(2, wx.RED)
        ctrl.SetPageTextColour(3, wx.BLUE)
        ctrl.SetRenamable(2, True)
        return ctrl

    def OnCreate(self, _event: wx.CommandEvent) -> None:
        ctrl: aui.AuiNotebook = self.create_ctrl()
        caption = "Notebook"
        self.mgr.AddPane(ctrl, aui.AuiPaneInfo().Caption(caption).
                         Float().FloatingPosition(self.start_position()).
                         CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        self.mgr.Update()
        ctrl.Refresh()
