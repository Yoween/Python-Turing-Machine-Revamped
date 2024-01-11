import wx
from wx import dataview as dv

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, -1, title, size=(1280, 720))
        
        self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))
        

        splitter = wx.SplitterWindow(self, -1)
        splitter.SetMinimumPaneSize(20)

        panel1 = wx.Panel(splitter, -1)
        panel1.SetBackgroundColour(wx.LIGHT_GREY)

        self.listctrl = dv.DataViewListCtrl(panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dv.DV_SINGLE)

        # setup self.listctrl columns
        for i in range(5):
            col = self.listctrl.AppendTextColumn(f'col {i}')

        # Bind the EVT_SIZE event to a handler
        self.listctrl.Bind(wx.EVT_SIZE, self.OnSize)

        # Create a sizer and add the self.listctrl to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.listctrl, 1, wx.EXPAND)

        # Set the sizer on the panel
        panel1.SetSizer(sizer)
        
        for i in range(50):
            self.listctrl.AppendItem([f'row {i}', f'row {i}', f'row {i}', f'row {i}', f'row {i}'])

        
        
        
        self.panel2 = wx.Panel(splitter, -1)
        self.panel2.SetBackgroundColour(wx.YELLOW)

        self.circle_colors = ['RED'] * 10

        self.panel2.Bind(wx.EVT_PAINT, self.OnPaint)

        # Create a vertical box sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.change_color_button = wx.Button(self.panel2, label='Change Circle Color')
        self.change_color_button.Bind(wx.EVT_BUTTON, self.OnButtonClick)
        sizer.Add(self.change_color_button)  # Add the button to the sizer

        # Variables to store the selected circle and color
        self.selected_circle = None
        self.new_color = 'BLUE'

        self.move_right_button = wx.Button(self.panel2, label='Right')
        self.move_right_button.Bind(wx.EVT_BUTTON, self.MoveRight)
        sizer.Add(self.move_right_button)  # Add the button to the sizer
        
        self.move_left_button = wx.Button(self.panel2, label='Left')
        self.move_left_button.Bind(wx.EVT_BUTTON, self.MoveLeft)
        sizer.Add(self.move_left_button)  # Add the button to the sizer

        # Set the sizer on the panel
        self.panel2.SetSizer(sizer)

        splitter.SplitVertically(panel1, self.panel2)
        splitter.SetSashPosition(self.GetSize().width // 3)

    def OnSize(self, event:wx.Event):
        table_width = self.listctrl.GetSize()[0] #GetSize returns (width, height) tuple
        num_col = self.listctrl.GetColumnCount()
        col_width = table_width/num_col
        for i in range(0, num_col):
            self.listctrl.GetColumn(i).SetWidth(int(col_width))
        event.Skip()  # Skip the event

    def OnButtonClick(self, event):
    # Prompt the user to enter the index of the circle
        dlg = wx.TextEntryDialog(self, 'Enter the index of the circle to change:')
        if dlg.ShowModal() == wx.ID_OK:
            # Update the color of the selected circle
            self.selected_circle = int(dlg.GetValue())
            self.circle_colors[self.selected_circle] = self.new_color
            # Force a repaint of the panel
            self.panel2.Refresh()
        dlg.Destroy()

    def OnPaint(self, event):
        # Create a device context
        dc = wx.PaintDC(event.GetEventObject())

        # Draw some small circles
        for i in range(10):
            # Set the brush and pen
            dc.SetBrush(wx.Brush(self.circle_colors[i]))  # Use the color from the list
            dc.SetPen(wx.Pen('BLACK'))  # Black outline

            x = i * 50  # X position
            y = i * 50  # Y position
            radius = 20  # Radius
            dc.DrawCircle(x, y, radius)
            
    def MoveRight(self, event):
        # Shift the colors to the right
        self.circle_colors = [self.circle_colors[-1]] + self.circle_colors[:-1]

        # Force a repaint of the panel
        self.panel2.Refresh()
        
    def MoveLeft(self, event):
        # Shift the colors to the left
        self.circle_colors = self.circle_colors[1:] + [self.circle_colors[0]]

        # Force a repaint of the panel
        self.panel2.Refresh()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Python Turing Machine Revamped")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()