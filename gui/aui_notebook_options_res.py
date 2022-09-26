import wx.lib.agw.aui as aui


"""AGW notebook window style flags.
 
https://docs.wxpython.org/wx.lib.agw.aui.auibook.AuiNotebook.html
Also see "resources.xls/NB_agwStyle".

Presently not mapped:
AUI_NB_MIDDLE_CLICK_CLOSE   "Allows to close AuiNotebook tabs by mouse middle button click"
AUI_NB_SUB_NOTEBOOK         "This style is used by AuiManager to create automatic AuiNotebooks"
AUI_NB_ORDER_BY_ACCESS      "Tab navigation order by last access time for the tabs"
AUI_NB_NO_TAB_FOCUS         "Don’t draw tab focus rectangle"
AUI_NB_DEFAULT_STYLE        "Default AGW window style"

{"<key>": <flag>}
"""
agw_style_flags: dict[str, int] = {
    "NotebookCloseButton":          aui.AUI_NB_CLOSE_BUTTON,                    #
    "NotebookCloseButtonActive":    aui.AUI_NB_CLOSE_ON_ACTIVE_TAB,             #
    "NotebookCloseButtonAll":       aui.AUI_NB_CLOSE_ON_ALL_TABS,               #
    "NotebookCloseOnLeft":          aui.AUI_NB_CLOSE_ON_TAB_LEFT,
    "NotebookAlignTop":             aui.AUI_NB_TOP,                             #
    "NotebookAlignBottom":          aui.AUI_NB_BOTTOM,                          #
    "NotebookAllowTabSplit":        aui.AUI_NB_TAB_SPLIT,
    "NotebookAllowTabMove":         aui.AUI_NB_TAB_MOVE,
    "NotebookAllowTabExternalMove": aui.AUI_NB_TAB_EXTERNAL_MOVE,
    "NotebookTabFloat":             aui.AUI_NB_TAB_FLOAT,
    "NotebookTabDrawDnd":           aui.AUI_NB_DRAW_DND_TAB,                    #
    "NotebookTabFixedWidth":        aui.AUI_NB_TAB_FIXED_WIDTH,
    "NotebookScrollButtons":        aui.AUI_NB_SCROLL_BUTTONS,
    "NotebookWindowList":           aui.AUI_NB_WINDOWLIST_BUTTON,
    "NotebookHideSingle":           aui.AUI_NB_HIDE_ON_SINGLE_TAB,              #
    "NotebookSmartTab":             aui.AUI_NB_SMART_TABS,                      #
    "NotebookUseImagesDropDown":    aui.AUI_NB_USE_IMAGES_DROPDOWN,             #
}
AUI_NB_CLOSE_MASK: int = aui.AUI_NB_CLOSE_BUTTON | aui.AUI_NB_CLOSE_ON_ACTIVE_TAB | aui.AUI_NB_CLOSE_ON_ALL_TABS
AUI_NB_TAB_MASK: int = aui.AUI_NB_TOP | aui.AUI_NB_BOTTOM

"""RADIO groups flag masks.

This dictionary should only include flags which are members of a RADIO group. For
each flag key, indicate the associated mask. Some groups use the cleared state as
a valid base state without a separate flag. Include such keys as well!

{"<key>": <RADIO group mask>}
"""
agw_style_flag_masks: dict[str, int] = {
    "NotebookNoCloseButton":        AUI_NB_CLOSE_MASK,  # Cleared flag state
    "NotebookCloseButton":          AUI_NB_CLOSE_MASK,
    "NotebookCloseButtonActive":    AUI_NB_CLOSE_MASK,
    "NotebookCloseButtonAll":       AUI_NB_CLOSE_MASK,
    "NotebookAlignTop":             AUI_NB_TAB_MASK,
    "NotebookAlignBottom":          AUI_NB_TAB_MASK
}

"""AGW TabArt providers

https://docs.wxpython.org/wx.lib.agw.aui.tabart.html
"""
agw_tabart_provider: dict[str, dict] = {
    "NotebookArtGloss":     {"provider": aui.AuiDefaultTabArt,  "rowid": 0},
    "NotebookArtSimple":    {"provider": aui.AuiSimpleTabArt,   "rowid": 1},
    "NotebookArtVC71":      {"provider": aui.VC71TabArt,        "rowid": 2},
    "NotebookArtFF2":       {"provider": aui.FF2TabArt,         "rowid": 3},
    "NotebookArtVC8":       {"provider": aui.VC8TabArt,         "rowid": 4},
    "NotebookArtChrome":    {"provider": aui.ChromeTabArt,      "rowid": 5}
}

"""Menu state for default Notebook startup style.

See defaults for notebook_ctrl.notebook_style. Presently:
AUI_NB_DEFAULT_STYLE | AUI_NB_TAB_EXTERNAL_MOVE ==

AUI_NB_TOP
AUI_NB_TAB_SPLIT
AUI_NB_TAB_MOVE
AUI_NB_TAB_EXTERNAL_MOVE
AUI_NB_SCROLL_BUTTONS
AUI_NB_CLOSE_ON_ACTIVE_TAB
AUI_NB_MIDDLE_CLICK_CLOSE
AUI_NB_DRAW_DND_TAB
"""
default_checked_menus: list[str] = [
    "NotebookAlignTop",
    "NotebookAllowTabSplit",
    "NotebookAllowTabMove",
    "NotebookAllowTabExternalMove",
    "NotebookScrollButtons",
    "NotebookCloseButtonActive",
    "NotebookTabDrawDnd"
]
