import wx.lib.agw.aui as aui


"""Minimize mode flags.

https://docs.wxpython.org/wx.lib.agw.aui.framemanager.AuiPaneInfo.html

Not implemented
AUI_MINIMIZE_POS_TOOLBAR

{"<key>": <flag>}
"""
minimize_mode_flags: dict[str, int] = {
    "MinimizePosSmart":     aui.AUI_MINIMIZE_POS_SMART,
    "MinimizePosTop":       aui.AUI_MINIMIZE_POS_TOP,
    "MinimizePosLeft":      aui.AUI_MINIMIZE_POS_LEFT,
    "MinimizePosRight":     aui.AUI_MINIMIZE_POS_RIGHT,
    "MinimizePosBottom":    aui.AUI_MINIMIZE_POS_BOTTOM,
    "MinimizeCaptSmart":    aui.AUI_MINIMIZE_CAPT_SMART,
    "MinimizeCaptHorz":     aui.AUI_MINIMIZE_CAPT_HORZ
}

"""RADIO groups flag masks.

This dictionary should only include flags which are members of a RADIO group. For
each flag key, indicate the associated mask. Some groups use the cleared state as
a valid base state without a separate flag. Include such keys as well!

{"<key>": <RADIO group mask>}
"""
minimize_mode_flag_masks: dict[str, int] = {
    "MinimizePosSmart":     aui.AUI_MINIMIZE_POS_MASK,
    "MinimizePosTop":       aui.AUI_MINIMIZE_POS_MASK,
    "MinimizePosLeft":      aui.AUI_MINIMIZE_POS_MASK,
    "MinimizePosRight":     aui.AUI_MINIMIZE_POS_MASK,
    "MinimizePosBottom":    aui.AUI_MINIMIZE_POS_MASK,
    "MinimizeCaptHide":     aui.AUI_MINIMIZE_CAPT_MASK,
    "MinimizeCaptSmart":    aui.AUI_MINIMIZE_CAPT_MASK,
    "MinimizeCaptHorz":     aui.AUI_MINIMIZE_CAPT_MASK
}

"""Menu state for default state."""
default_checked_menus: list[str] = [
    "MinimizePosSmart", "MinimizeCaptHide"
]

content_ctrls: dict[str, str] = {
    "grid_content":         "GridContent",
    "text_content":         "TextContent",
    "tree_content":         "TreeContent",
    "sizereport_content":   "SizeReportContent",
    "html_content":         "HTMLContent",
    "notebook_content":     "NotebookContent"
}
