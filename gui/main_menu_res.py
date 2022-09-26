"""Main menu definition.

All keys/item_ids should be unique within entire structure.
"""
import wx


if wx.Platform == "__WXMAC__":
    switcher_accel = "Alt+Tab"
elif wx.Platform == "__WXGTK__":
    switcher_accel = "Ctrl+/"
else:
    switcher_accel = "Ctrl+Tab"

main_menu_items = {
    "File": {
        "label": "&File",
        "children": {}
    },
    "View": {
        "label": "&View",
        "children": {
            "CreateText":           {"label": "Create &Text Control"},
            "CreateHTML":           {"label": "Create &HTML Control"},
            "CreateTree":           {"label": "Create T&ree"},
            "CreateGrid":           {"label": "Create &Grid"},
            "CreateNotebook":       {"label": "Create &Notebook"},
            "CreateSizeReport":     {"label": "Create &Size Reporter"},
            "separator10":          {"label": ""},
            "GridContent":          {"label": "Use a Grid for the Content Pane"},
            "TextContent":          {"label": "Use a Text Control for the Content Pane"},
            "HTMLContent":          {"label": "Use an HTML Control for the Content Pane"},
            "TreeContent":          {"label": "Use a Tree Control for the Content Pane"},
            "NotebookContent":      {"label": "Use a AuiNotebook control for the Content Pane"},
            "SizeReportContent":    {"label": "Use a Size Reporter for the Content Pane"},
            "separator11":          {"label": ""},
            "SwitchPane":           {"label": f"S&witch Window...\t{switcher_accel}"}
        }
    },
    "Options": {
        "label": "&Options",
        "children": {
            "TransparentHint":      {"type": "radio", "label": "Transparent Hint"},
            "VenetianBlindsHint":   {"type": "radio", "label": "Venetian Blinds Hint"},
            "RectangleHint":        {"type": "radio", "label": "Rectangle Hint"},
            "NoHint":               {"type": "radio", "label": "No Hint"},
            "separator30":          {"label": ""},
            "HintFade":             {"type": "check", "label": "Hint Fade-in"},
            "NoVenetianFade":       {"type": "check", "label": "Disable Venetian Blinds Hint Fade-in"},
            "AllowFloating":        {"type": "check", "label": "Allow Floating"},
            "TransparentDrag":      {"type": "check", "label": "Transparent Drag"},
            "AllowActivePane":      {"type": "check", "label": "Allow Active Pane"},
            "LiveUpdate":           {"type": "check", "label": "Live Resize Update"},
            "NativeMiniframes":     {"type": "check", "label": "Use Native wx.MiniFrames"},
            "separator31":          {"label": ""},
            "MinimizePosSmart":     {"type": "radio", "label": "Minimize in Smart mode"},
            "MinimizePosTop":       {"type": "radio", "label": "Minimize on Top"},
            "MinimizePosLeft":      {"type": "radio", "label": "Minimize on the Left"},
            "MinimizePosRight":     {"type": "radio", "label": "Minimize on the Right"},
            "MinimizePosBottom":    {"type": "radio", "label": "Minimize at the Bottom"},
            "separator32":          {"label": ""},
            "MinimizeCaptHide":     {"type": "radio", "label": "Hidden Minimized Caption"},
            "MinimizeCaptSmart":    {"type": "radio", "label": "Smart Minimized Caption"},
            "MinimizeCaptHorz":     {"type": "radio", "label": "Horizontal Minimized Caption"},
            "separator33":          {"label": ""},
            "PaneIcons":            {"type": "check", "label": "Set Icons On Panes"},
            "AnimateFrames":        {"type": "check", "label": "Animate Dock/Close/Minimize Of Floating Panes"},
            "SmoothDocking":        {"type": "check", "label": "Smooth Docking Effects (PyQT Style)"},
            "separator34":          {"label": ""},
            "TransparentPane":      {"label": "Set Floating Panes Transparency"},
            "separator35":          {"label": ""},
            "DefaultDockArt":       {"type": "radio", "label": "Default DockArt"},
            "ModernDockArt":        {"type": "radio", "label": "Modern Dock Art"},
            "separator36":          {"label": ""},
            "SnapToScreen":         {"label": "Snap To Screen"},
            "SnapPanes":            {"type": "check", "label": "Snap Panes To Managed Window"},
            "FlyOut":               {"type": "check", "label": "Use Fly-Out Floating Panes"},
            "separator37":          {"label": ""},
            "CustomPaneButtons":    {"type": "check", "label": "Set Custom Pane Button Bitmaps"},
            "separator38":          {"label": ""},
            "NoGradient":           {"type": "radio", "label": "No Caption Gradient"},
            "VerticalGradient":     {"type": "radio", "label": "Vertical Caption Gradient"},
            "HorizontalGradient":   {"type": "radio", "label": "Horizontal Caption Gradient"},
            "separator39":          {"label": ""},
            "PreviewMinimized":     {"type": "check", "label": "Preview Minimized Panes"},
            "separator310":         {"label": ""},
            "Settings":             {"label": "&Settings\tCtrl-O"},
        }
    },
    "Notebook": {
        "label": "&Notebook",
        "children": {
            "NotebookArtGloss":             {"type": "radio", "label": "Glossy Theme (Default)"},
            "NotebookArtSimple":            {"type": "radio", "label": "Simple Theme"},
            "NotebookArtVC71":              {"type": "radio", "label": "VC71 Theme"},
            "NotebookArtFF2":               {"type": "radio", "label": "Firefox 2 Theme"},
            "NotebookArtVC8":               {"type": "radio", "label": "VC8 Theme"},
            "NotebookArtChrome":            {"type": "radio", "label": "Chrome Theme"},
            "separator40":                  {"label": ""},
            "NotebookNoCloseButton":        {"type": "radio", "label": "No Close Button"},
            "NotebookCloseButton":          {"type": "radio", "label": "Close Button At Right"},
            "NotebookCloseButtonAll":       {"type": "radio", "label": "Close Button On All Tabs"},
            "NotebookCloseButtonActive":    {"type": "radio", "label": "Close Button On Active Tab"},
            "separator41":                  {"label": ""},
            "NotebookCloseOnLeft":          {"type": "check", "label": "Close Button On The Left Of Tabs"},
            "separator42":                  {"label": ""},
            "NotebookAllowTabMove":         {"type": "check", "label": "Allow Tab Move"},
            "NotebookAllowTabExternalMove": {"type": "check", "label": "Allow External Tab Move"},
            "NotebookAllowTabSplit":        {"type": "check", "label": "Allow Notebook Split"},
            "NotebookTabFloat":             {"type": "check", "label": "Allow Single Tab Floating"},
            "separator43":                  {"label": ""},
            "NotebookDclickUnsplit":        {"type": "check", "label": "Unsplit On Sash Double-Click"},
            "NotebookTabDrawDnd":           {"type": "check", "label": "Draw Tab Image On Drag 'n' Drop"},
            "separator44":                  {"label": ""},
            "NotebookScrollButtons":        {"type": "check", "label": "Scroll Buttons Visible"},
            "NotebookWindowList":           {"type": "check", "label": "Window List Button Visible"},
            "NotebookTabFixedWidth":        {"type": "check", "label": "Fixed-Width Tabs"},
            "separator45":                  {"label": ""},
            "NotebookHideSingle":           {"type": "check", "label": "Hide On Single Tab"},
            "NotebookSmartTab":             {"type": "check", "label": "Use Smart Tabbing"},
            "NotebookUseImagesDropDown":    {"type": "check", "label": "Use Tab Images In Dropdown Menu"},
            "NotebookCustomButtons":        {"type": "check", "label": "Show Custom Buttons In Tab Area"},
            "separator46":                  {"label": ""},
            "NotebookAlignTop":             {"type": "radio", "label": "Tab Top Alignment"},
            "NotebookAlignBottom":          {"type": "radio", "label": "Tab Bottom Alignment"},
            "separator47":                  {"label": ""},
            "NotebookMinMaxWidth":          {"label": "Set Min/Max Tab Widths"},
            "NotebookMultiLine":            {"label": "Add A Multi-Line Label Tab"},
            "separator48":                  {"label": ""},
            "NotebookPreview":              {"label": "Preview Of All Notebook Pages"},
        }
    },
    "Perspectives": {
        "label": "&Perspectives",
        "children": {
            "FramePerspectives": {
                "type": "submn",
                "label": "&Frame Perspectives",
                "children": {
                    "CreatePerspective":        {"label": "Create Perspective"},
                    "CopyPerspectiveCode":      {"label": "Copy Perspective Data To Clipboard"},
                },
            },
            "separator50": {"label": ""},
            "DockingGuides": {
                "type": "submn",
                "label": "&Docking Guides",
                "children": {
                    "StandardGuides":           {"type": "radio", "label": "Standard Docking Guides"},
                    "AeroGuides":               {"type": "radio", "label": "Aero-Style Docking Guides"},
                    "WhidbeyGuides":            {"type": "radio", "label": "Whidbey-Style Docking Guides"},
                },
            },
        }
    },
    "Actions": {
        "label": "&Actions",
        "children": {
            "VetoTree":         {"type": "check", "label": "Veto Floating Of Tree Pane"},
            "VetoText":         {"type": "check", "label": "Veto Docking Of Fixed Pane"},
            "separator60":      {"label": ""},
            "UserAttention":    {
                "type": "submn",
                "label": "Request User Attention For",
                "children": {}
            },
        }
    },
    "Help": {
        "label": "&Help",
        "children": {}
    }
}
