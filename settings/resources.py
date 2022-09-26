import wx
import wx.lib.agw.aui as aui


sids = {
    "PaneBorderSize": {
        "aui_id": aui.AUI_DOCKART_PANE_BORDER_SIZE,
        "label": "Pane Border Size:"
    },
    "SashSize": {
        "aui_id": aui.AUI_DOCKART_SASH_SIZE,
        "label": "Sash Size:"
    },
    "CaptionSize": {
        "aui_id": aui.AUI_DOCKART_CAPTION_SIZE,
        "label": "Caption Size:"
    }
}


cids = {
    "BackgroundColour": {
        "aui_id": aui.AUI_DOCKART_BACKGROUND_COLOUR,
        "label": "Background Color:"
    },
    "SashColour": {
        "aui_id": aui.AUI_DOCKART_SASH_COLOUR,
        "label": "Sash Color:"
    },
    "InactiveCaptionColour": {
        "aui_id": aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,
        "label": "Normal Caption:"
    },
    "InactiveCaptionGradientColour": {
        "aui_id": aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR,
        "label": "Normal Caption Gradient:"
    },
    "InactiveCaptionTextColour": {
        "aui_id": aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR,
        "label": "Normal Caption Text:"
    },
    "ActiveCaptionColour": {
        "aui_id": aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR,
        "label": "Active Caption:"
    },
    "ActiveCaptionGradientColour": {
        "aui_id": aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR,
        "label": "Active Caption Gradient:"
    },
    "ActiveCaptionTextColour": {
        "aui_id": aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR,
        "label": "Active Caption Text:"
    },
    "BorderColour": {
        "aui_id": aui.AUI_DOCKART_BORDER_COLOUR,
        "label": "Border Color:"
    },
    "GripperColour": {
        "aui_id": aui.AUI_DOCKART_GRIPPER_COLOUR,
        "label": "Gripper Color:"
    },
    "HintColour": {
        "aui_id": aui.AUI_DOCKART_HINT_WINDOW_COLOUR,
        "label": "Hint Window Colour:"
    },
}


def pallet_from_color(pallet_color: wx.Colour = wx.BLACK,
                      pallet_width: int = 25,
                      pallet_height: int = 14,
                      border_thickness: int = 1,
                      border_color: wx.Colour = wx.BLACK) -> wx.Bitmap:
    """
    wx.Bitmap.FromBuffer(data: bytearray) takes bytearray argument as the source.
    This format can be produced from a binary string: bytearray(b"..."). The same
    format is used by wx.Image.<Get/Set>Data. This byte array encodes a rectangular
    image as a line-wise 1D-array. data[0], data[1], and data[2] encode red, green,
    and blue components of the top-left pixel and data[-1] is the blue component of
    the bottom-right pixel.
    """
    pallet_rgb: bytes = pallet_color.GetRGB().to_bytes(length=3, byteorder="little")
    frame_rgb: bytes = border_color.GetRGB().to_bytes(length=3, byteorder="little")
    horizontal_border: bytes = frame_rgb * pallet_width * border_thickness
    inner_line: bytes = (frame_rgb * border_thickness +
                         pallet_rgb * (pallet_width - border_thickness * 2) +
                         frame_rgb * border_thickness)
    pallet_data = bytearray(
        horizontal_border +
        inner_line * (pallet_height - border_thickness * 2) +
        horizontal_border
    )
    return wx.Bitmap.FromBuffer(pallet_width, pallet_height, pallet_data)


def pallets_from_color(pallet_color: wx.Colour = wx.BLACK) -> wx.BitmapBundle:
    return wx.BitmapBundle.FromBitmap(pallet_from_color(pallet_color))
