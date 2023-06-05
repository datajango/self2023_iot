import wx

class DialogBase(wx.Dialog):
    def __init__(self, parent):
        # Load size and position from file
        try:
            with open("window_size_pos.txt", "r") as file:
                x, y, width, height = map(int, file.read().split(','))
                pos = (x, y)
                size = (width, height)
        except Exception:
            pos = (100, 100)
            size = (500, 500)

        super().__init__(parent, title="My Dialog", pos=pos, size=size)

        # Bind the close event
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        # Get size and position
        size = self.GetSize()
        pos = self.GetPosition()

        # Save size and position to file
        with open("window_size_pos.txt", "w") as file:
            file.write(f"{pos.x},{pos.y},{size.width},{size.height}")

        event.Skip()  # Ensure the window actually closes
