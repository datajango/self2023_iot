import wx
from wx.lib.embeddedimage import PyEmbeddedImage

def create_dot(size=10, color="red"):
    image = wx.Image(size, size)
    if color.lower() == "red":
        image.SetRGB(wx.Rect(0, 0, size, size), 255, 0, 0)
    elif color.lower() == "green":
        image.SetRGB(wx.Rect(0, 0, size, size), 0, 255, 0)
    else:
        raise ValueError(f"Unsupported color: {color}")
    return wx.Bitmap(image)

class ErrorIndicator(wx.StaticBitmap):
    def __init__(self, parent=None, error_state=False):
        super(ErrorIndicator, self).__init__(parent)
        self.error_state = error_state

        self.red_dot = create_dot(10, "red")
        self.green_dot = create_dot(10, "green")

        self.set_error_state(error_state)

    def set_error_state(self, state):
        self.error_state = state

        if self.error_state:
            self.SetBitmap(self.red_dot)    
        else:
            self.SetBitmap(self.green_dot)
