import wx.lib.agw.aui as aui

"""AGW manager style flags.

https://docs.wxpython.org/wx.lib.agw.aui.framemanager.AuiManager.html
Also see "resources.xls/MGR_agwStyle".

{"<key>": <flag>}
"""
agw_style_flags: dict[str, int] = {
    "AeroGuides":           aui.AUI_MGR_AERO_DOCKING_GUIDES,
    "WhidbeyGuides":        aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES,
    "TransparentHint":      aui.AUI_MGR_TRANSPARENT_HINT,
    "VenetianBlindsHint":   aui.AUI_MGR_VENETIAN_BLINDS_HINT,
    "RectangleHint":        aui.AUI_MGR_RECTANGLE_HINT,
    "HintFade":             aui.AUI_MGR_HINT_FADE,
    "NoVenetianFade":       aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE,
    "AllowFloating":        aui.AUI_MGR_ALLOW_FLOATING,
    "TransparentDrag":      aui.AUI_MGR_TRANSPARENT_DRAG,
    "AllowActivePane":      aui.AUI_MGR_ALLOW_ACTIVE_PANE,
    "LiveUpdate":           aui.AUI_MGR_LIVE_RESIZE,
    "NativeMiniframes":     aui.AUI_MGR_USE_NATIVE_MINIFRAMES,
    "AnimateFrames":        aui.AUI_MGR_ANIMATE_FRAMES,
    "SmoothDocking":        aui.AUI_MGR_SMOOTH_DOCKING,
    "PreviewMinimized":     aui.AUI_MGR_PREVIEW_MINIMIZED_PANES
}
AUI_MGR_DOCKING_GUIDES_MASK: int = \
    aui.AUI_MGR_AERO_DOCKING_GUIDES | aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES
AUI_MGR_HINT_MASK: int = \
    aui.AUI_MGR_TRANSPARENT_HINT | aui.AUI_MGR_VENETIAN_BLINDS_HINT | aui.AUI_MGR_RECTANGLE_HINT

"""RADIO groups flag masks.

This dictionary should only include flags which are members of a RADIO group. For
each flag key, indicate the associated mask. Some groups use the cleared state as
a valid base state without a separate flag. Include such keys as well!

{"<key>": <RADIO group mask>}
"""
agw_style_flag_masks: dict[str, int] = {
    "StandardGuides":       AUI_MGR_DOCKING_GUIDES_MASK,  # Cleared flag state
    "AeroGuides":           AUI_MGR_DOCKING_GUIDES_MASK,
    "WhidbeyGuides":        AUI_MGR_DOCKING_GUIDES_MASK,
    "NoHint":               AUI_MGR_HINT_MASK,            # Cleared flag state
    "TransparentHint":      AUI_MGR_HINT_MASK,
    "VenetianBlindsHint":   AUI_MGR_HINT_MASK,
    "RectangleHint":        AUI_MGR_HINT_MASK,
}

"""Menu state for default Manager startup style.

AUI_MGR_DEFAULT == 
AUI_MGR_ALLOW_FLOATING
AUI_MGR_TRANSPARENT_HINT
AUI_MGR_HINT_FADE
AUI_MGR_NO_VENETIAN_BLINDS_FADE
"""
default_checked_menus: list[str] = [
    "AllowFloating", "TransparentHint", "HintFade", "NoVenetianFade"
]
