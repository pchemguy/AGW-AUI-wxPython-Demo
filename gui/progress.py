import time
import wx


# ---------------------------------------------------------------------------- #
# Class ProgressGauge
# ---------------------------------------------------------------------------- #
# noinspection PyPep8Naming
class ProgressGauge(wx.Window):
    """ This class provides a visual alternative for wx.Gauge."""

    def __init__(self, parent: wx.Window, winid=wx.ID_ANY,
                 pos: wx.Position = wx.DefaultPosition, size: wx.Size = wx.Size(-1, 30)):
        """ Default class constructor. """
        super().__init__(parent, winid, pos, size, style=wx.BORDER_NONE)

        self.value: int = 0
        self.steps: int = 64
        self.pos: int = 0
        self.current: int = 0
        self.gaugeproportion: float = 0.8
        self.startTime = time.time()

        self.bottomStartColour: wx.Colour = wx.GREEN
        self.bottomEndColour: wx.Colour = self.LightColour(self.bottomStartColour, 30)
        self.topStartColour: wx.Colour = self.LightColour(self.bottomStartColour, 80)
        self.topEndColour: wx.Colour = self.LightColour(self.bottomStartColour, 40)

        self.background = wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, _event: wx.EraseEvent) -> None:
        """ Handles the wx.EVT_ERASE_BACKGROUND event for ProgressGauge. """
        pass

    def OnPaint(self, _event: wx.PaintEvent):
        """ Handles the wx.EVT_PAINT event for ProgressGauge. """
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(self.background)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()

        xsize, ysize = self.GetClientSize()
        interval = xsize / self.steps
        self.pos = interval * self.value
        status = self.current / ((1 - self.gaugeproportion) * self.steps)

        if status % 2 == 0:
            increment = 1
        else:
            increment = -1

        self.value += increment
        self.current += 1

        self.DrawProgress(dc, xsize, ysize, increment)

        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRADIENTINACTIVECAPTION)))
        dc.DrawRectangle(self.GetClientRect())

    def LightColour(self, colour: wx.Colour, percent) -> wx.Colour:
        """
        Return light contrast of colour. The colour returned is from the scale of
        colour -> white. The percent determines how light the colour will be.
        Percent = 100 return white, percent = 0 returns colour.
        """
        end_colour = wx.WHITE
        rd = end_colour.Red() - colour.Red()
        gd = end_colour.Green() - colour.Green()
        bd = end_colour.Blue() - colour.Blue()
        high = 100

        # We take the percent way of the colour from colour -> white
        r = colour.Red() + percent * rd // high
        g = colour.Green() + percent * gd // high
        b = colour.Blue() + percent * bd // high

        return wx.Colour(r, g, b)

    def DrawProgress(self, dc, xsize, _ysize, increment) -> None:
        """ Actually draws the sliding bar. """
        interval: float = self.gaugeproportion * xsize
        gc: wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        clientRect = self.GetClientRect()
        gradientRect = wx.Rect(*clientRect)

        x, y, width, height = clientRect
        x, width = self.pos, interval

        gradientRect.SetHeight(gradientRect.GetHeight() // 2)
        topStart, topEnd = self.topStartColour, self.topEndColour

        rc1 = wx.Rect(int(x), y, int(width), height // 2)
        path1 = self.GetPath(gc, rc1, 8)
        br1 = gc.CreateLinearGradientBrush(x, y, x, y + height // 2, topStart, topEnd)
        gc.SetBrush(br1)
        gc.FillPath(path1)  # draw main

        path4 = gc.CreatePath()
        path4.AddRectangle(x, y + height // 2 - 8, width, 8)
        path4.CloseSubpath()
        gc.SetBrush(br1)
        gc.FillPath(path4)

        gradientRect.Offset((0, gradientRect.GetHeight()))

        bottomStart, bottomEnd = self.bottomStartColour, self.bottomEndColour

        rc3: wx.Rect = wx.Rect(int(x), y + height // 2, int(width), height // 2)
        path3 = self.GetPath(gc, rc3, 8)
        br3 = gc.CreateLinearGradientBrush(x, y + height // 2, x, y + height, bottomStart, bottomEnd)
        gc.SetBrush(br3)
        gc.FillPath(path3)  # draw main

        path4 = gc.CreatePath()
        path4.AddRectangle(x, y + height // 2, width, 8)
        path4.CloseSubpath()
        gc.SetBrush(br3)
        gc.FillPath(path4)

    def GetPath(self, gc: wx.GraphicsContext, rc: wx.Rect, r) -> wx.GraphicsPath:
        """ Returns a rounded GraphicsPath. """
        x, y, w, h = rc
        path: wx.GraphicsPath = gc.CreatePath()
        path.AddRoundedRectangle(x, y, w, h, r)
        path.CloseSubpath()
        return path

    def Pulse(self):
        """ Updates the gauge with a new value. """
        self.Refresh()
