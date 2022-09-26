import sys
import wx
import wx.lib.agw.aui as aui

from gui.main_frame import MainFrame
from gui.main_menu import MainMenu
from gui.toolbars import ToolBarManager
from gui.context_menu import PopupMenu
from gui.controls import SizeReportCtrl, TextCtrl, TreeCtrl, HTMLCtrl, GridCtrl
from gui.aui_notebook import Notebook
from gui.aui_notebook_options import NotebookOptions
from gui.aui_manager_options import ManagerOptions
from gui.aui_dockart_options import DockArtOptions
from gui.base_panes import PaneManager
from gui.perspective import LayoutManager
from settings.gui import SettingsPanel


class MainApp:
    # If subclassing wx.App [class MainApp(wx.App):], remove the next line.
    app: wx.App

    def __init__(self):
        # If subclassing wx.App, uncomment the next line.
        # super().__init__(redirect=False)
        # If subclassing wx.App, remove the next two lines.
        self.app = wx.App(False)
        self.OnInit()

    # If subclassing wx.App, remove this method.
    def MainLoop(self):
        self.app.MainLoop()

    def OnInit(self):
        # If subclassing wx.App, this methods is envoked automatically by the framework.
        mgr: aui.AuiManager = aui.AuiManager()

        # If MainFrame subclasses wx.Frame and MainFrame().frame is not set to self,
        # remove the second line and rename main_frame -> frame.
        main_frame: MainFrame = MainFrame(None, wx.ID_ANY, "AUI Test Frame", size=wx.Size(800, 600))
        frame: wx.Frame = main_frame.frame

        mgr.SetManagedWindow(frame)  # tell FrameManager to manage this frame

        menubar = MainMenu(frame, mgr)
        tbman: ToolBarManager = ToolBarManager(frame, mgr)
        popup: PopupMenu = PopupMenu(frame)
        popup.bind_DropDownToolbarItem(tbman.items["DropDownToolbarItem"]["id"])

        ID_SizeReportCtrl: wx.WindowIDRef = menubar.items["CreateSizeReport"]["id"]
        size_reporter: SizeReportCtrl = SizeReportCtrl(frame, mgr, ID_SizeReportCtrl)
        ID_TextCtrl: wx.WindowIDRef = menubar.items["CreateText"]["id"]
        text_ctrl: TextCtrl = TextCtrl(frame, mgr, ID_TextCtrl)
        ID_TreeCtrl: wx.WindowIDRef = menubar.items["CreateTree"]["id"]
        tree_ctrl: TreeCtrl = TreeCtrl(frame, mgr, ID_TreeCtrl)
        ID_HTMLCtrl: wx.WindowIDRef = menubar.items["CreateHTML"]["id"]
        html_ctrl: HTMLCtrl = HTMLCtrl(frame, mgr, ID_HTMLCtrl)
        ID_GridCtrl: wx.WindowIDRef = menubar.items["CreateGrid"]["id"]
        grid_ctrl: GridCtrl = GridCtrl(frame, mgr, ID_GridCtrl)
        ID_NotebookCtrl: wx.WindowIDRef = menubar.items["CreateNotebook"]["id"]
        notebook_ctrl: Notebook = Notebook(frame, mgr, ID_NotebookCtrl, html_ctrl)
        _notebook_options: NotebookOptions = NotebookOptions(
            frame, mgr, notebook_ctrl, menubar.items, menubar.item_ids)
        _manager_options: ManagerOptions = ManagerOptions(
            frame, mgr, menubar.items, menubar.item_ids)
        _dockart_options: DockArtOptions = DockArtOptions(
            frame, mgr, menubar.items, menubar.item_ids)

        paneman: PaneManager = PaneManager(
            frame, mgr, menubar.items, menubar.item_ids, html_ctrl, text_ctrl,
            tree_ctrl, grid_ctrl, size_reporter, notebook_ctrl)
        paneman.build_panes()
        paneman.request_menu()
        layman: LayoutManager = LayoutManager(frame, mgr, menubar.items)
        layman.save("All Panes")
        paneman.default_layout()
        layman.save("Default Startup")
        setman: SettingsPanel = SettingsPanel(frame, mgr)
        setman.build_panel(menubar.items)

        main_frame.init_man(mgr)
        frame.CenterOnScreen()
        frame.Show()
        return True


if __name__ == "__main__":
    sys.path.insert(0, '.')
    app = MainApp()
    app.MainLoop()
