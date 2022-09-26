import wx
import wx.aui
import wx.lib.agw.aui as aui
from typing import TypeAlias

from .resources import sids, cids, pallet_from_color, pallets_from_color

wxControl: TypeAlias = wx.BitmapButton | wx.SpinCtrl | wx.CheckBox


# noinspection PyPep8Naming
class SettingsPanel:
    frame: wx.Frame
    mgr: aui.AuiManager
    panel: wx.Panel
    mb_items: dict  # menubar.items
    sizers: list[wx.Sizer]
    sid_ctrls: dict[wx.WindowIDRef, str]
    cid_ctrls: dict[wx.WindowIDRef, str]
    sash_grip: dict

    def __init__(self, frame: wx.Frame, mgr: aui.AuiManager) -> None:
        self.frame = frame
        self.mgr = mgr
        self.panel = wx.Panel(frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        self.sizers = []

    def build_panel(self, mb_items: dict) -> None:
        panel: wx.Panel = self.panel
        label: str
        sizer: wx.Sizer
        spinner: wx.SpinCtrl
        ctrl_id: wx.WindowIDRef
        self.sid_ctrls = {}
        for ctrl_name in sids:
            label = sids[ctrl_name]["label"]
            ctrl_id = wx.NewIdRef()
            sids[ctrl_name]["ctrl_id"] = ctrl_id
            self.sid_ctrls[ctrl_id] = ctrl_name
            spinner: wx.SpinCtrl = wx.SpinCtrl(panel, ctrl_id, "", wx.DefaultPosition, wx.Size(50, 20))
            sids[ctrl_name]["ctrl"] = spinner
            self.add_basic_box_sizer(spinner, label)
            spinner.SetValue(self.art_provider().GetMetric(sids[ctrl_name]["aui_id"]))
            panel.Bind(wx.EVT_SPINCTRL, self.OnChangeSize, id=ctrl_id)

        button: wx.BitmapButton
        ctrl_name: str
        self.cid_ctrls = {}
        for ctrl_name in cids:
            label = cids[ctrl_name]["label"]
            ctrl_id = wx.NewIdRef()
            cids[ctrl_name]["ctrl_id"] = wx.NewIdRef()
            self.cid_ctrls[ctrl_id] = ctrl_name
            button: wx.BitmapButton = wx.BitmapButton(
                panel, ctrl_id, pallet_from_color(wx.BLACK), wx.DefaultPosition, wx.Size(50, 25))
            cids[ctrl_name]["ctrl"] = button
            self.add_basic_box_sizer(button, label)
            panel.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ctrl_id)

        ctrl_id = wx.NewIdRef()
        checkbox: wx.CheckBox = wx.CheckBox(panel, ctrl_id, "", wx.DefaultPosition, wx.Size(50, 20))
        self.sash_grip = {"DrawSashGrip": {
            "ctrl_id": ctrl_id,
            "aui_id": aui.AUI_DOCKART_DRAW_SASH_GRIP,
            "label": "Draw Sash Grip:",
            "ctrl": checkbox
        }}
        ctrl_dict = self.sash_grip["DrawSashGrip"]
        self.add_basic_box_sizer(ctrl_dict["ctrl"], ctrl_dict["label"])
        ctrl_dict["ctrl"].SetValue(self.art_provider().GetMetric(ctrl_dict["aui_id"]))
        self.panel.Bind(wx.EVT_CHECKBOX, self.OnDrawSashGrip, id=ctrl_dict["ctrl_id"])

        grid_sizer = wx.GridSizer(rows=0, cols=2, vgap=5, hgap=5)
        grid_sizer.SetHGap(5)
        s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15 = self.sizers
        sizers = [s1, s4, s2, s5, s3, s13, s15, (1, 1), s12, s6, s9, s7, s10, s8, s11, s14]
        for sizer in sizers:
            grid_sizer.Add(sizer)

        cont_sizer = wx.BoxSizer(wx.VERTICAL)
        cont_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(cont_sizer)
        panel.GetSizer().SetSizeHints(panel)
        self.update_colors()
        self.mgr.AddPane(
            panel, aui.AuiPaneInfo().Name("settings").Caption("Dock Manager Settings").
            Dockable(False).Float().Hide().CloseButton(True).MaximizeButton(True))
        self.mgr.Update()

        self.frame.Bind(wx.EVT_MENU, self.OnSettings, id=mb_items["Settings"]["id"])

    def update_colors(self):
        aui_id: wx.aui.AuiPaneDockArtSetting
        button: wx.BitmapButton
        for ctrl_name in cids:
            aui_id = cids[ctrl_name]["aui_id"]
            colour = self.art_provider().GetColour(aui_id)
            button = cids[ctrl_name]["ctrl"]
            button.SetBitmapLabel(pallets_from_color(colour))

    def add_basic_box_sizer(self, ctrl: wxControl, ctrl_label: str) -> None:
        sizer: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((1, 1), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self.panel, -1, ctrl_label))
        sizer.Add(ctrl)
        sizer.Add((1, 1), 1, wx.EXPAND)
        sizer.SetItemMinSize(1, (180, 20))
        self.sizers.append(sizer)

    def art_provider(self) -> aui.AuiDefaultDockArt:
        return self.mgr.GetArtProvider()

    def OnSettings(self, _event: wx.CommandEvent):
        # show the settings pane, and float it
        floating_pane: aui.AuiPaneInfo = self.mgr.GetPane("settings").Float().Show()
        if floating_pane.floating_pos == wx.DefaultPosition:
            floating_pane.FloatingPosition(wx.Point(500, 500))
        self.mgr.Update()

    def OnChangeSize(self, event: wx.SpinEvent) -> None:
        aui_id: wx.aui.AuiPaneDockArtSetting
        ctrl_id: wx.WindowIDRef = event.GetId()
        ctrl_name = self.sid_ctrls[ctrl_id]
        aui_id = sids[ctrl_name]["aui_id"]
        self.art_provider().SetMetric(aui_id, event.GetInt())
        self.mgr.Update()

    def OnDrawSashGrip(self, event: wx.CommandEvent) -> None:
        self.art_provider().SetMetric(aui.AUI_DOCKART_DRAW_SASH_GRIP, event.GetInt())
        self.mgr.Update()

    def OnSetColor(self, event: wx.CommandEvent) -> None:
        aui_id: wx.aui.AuiPaneDockArtSetting
        dlg: wx.ColourDialog
        dlg = wx.ColourDialog(self.frame)
        dlg.SetTitle("Color Picker")
        if dlg.ShowModal() != wx.ID_OK:
            return
        ctrl_id: wx.WindowIDRef = event.GetId()
        ctrl_name = self.cid_ctrls[ctrl_id]
        aui_id = cids[ctrl_name]["aui_id"]
        self.art_provider().SetColour(aui_id, dlg.GetColourData().GetColour())
        self.update_colors()
        self.mgr.Update()
