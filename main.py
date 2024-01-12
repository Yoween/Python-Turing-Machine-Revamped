import wx
from wx import dataview as dv

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, tape_size):
        wx.Frame.__init__(self, None, -1, title, size=(1280, 720))
        
        self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))
        
        self.color_map = {'b': 'WHITE', '0': 'RED', '1': 'BLUE'}
        self.InitTape(tape_size)
        self.len_tape_list = tape_size
        self.selected_circle = self.len_tape_list // 2
        

        splitter = wx.SplitterWindow(self, -1)
        splitter.SetMinimumPaneSize(20)

        panel1 = wx.Panel(splitter, -1)
        panel1.SetBackgroundColour(wx.LIGHT_GREY)

        self.listctrl = dv.DataViewListCtrl(panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dv.DV_SINGLE)

        # setup self.listctrl columns
        for i in range(5):
            self.listctrl.AppendTextColumn(f'col {i}')

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
        self.panel2.SetBackgroundColour(wx.Colour(128, 128, 255))

        self.panel2.Bind(wx.EVT_PAINT, self.InitialDrawCircles)

        # Create a vertical box sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.clear_all_button = wx.Button(self.panel2, label='Clear')
        self.clear_all_button.Bind(wx.EVT_BUTTON, self.ClearPaint)
        sizer.Add(self.clear_all_button)  # Add the button to the sizer
        
        self.set_blank_button = wx.Button(self.panel2, label='b')
        self.set_blank_button.Bind(wx.EVT_BUTTON, self.SetColor(color='b'))
        sizer.Add(self.set_blank_button)  # Add the button to the sizer
        
        self.set_zero_button = wx.Button(self.panel2, label='0')
        self.set_zero_button.Bind(wx.EVT_BUTTON, self.SetColor(color='0'))
        sizer.Add(self.set_zero_button)  # Add the button to the sizer
        
        self.set_one_button = wx.Button(self.panel2, label='1')
        self.set_one_button.Bind(wx.EVT_BUTTON, self.SetColor(color='1'))
        sizer.Add(self.set_one_button)  # Add the button to the sizer


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

    def InitialDrawCircles(self, event):
        dc = wx.PaintDC(event.GetEventObject())
        for i in range(self.len_tape_list):
            value = self.tape_list[i]
            color = self.color_map[value]
            dc.SetBrush(wx.Brush(color))
            dc.SetPen(wx.Pen('BLACK'))
            x = i * 50 + 100
            y = i * 50 + 100
            radius = 20
            dc.DrawCircle(x, y, radius)
        
    def SetColor(self, color, *args):
        self.tape_list[self.selected_circle] = color
        self.panel2.Refresh()
        
    def ClearPaint(self, event):
        self.InitTape()
        self.panel2.Refresh()

    def InitTape(self, size):
        self.tape_list = ["b"] * size

    def MoveRight(self, event):
        # Shift the colors to the right
        self.tape_list = [self.tape_list[-1]] + self.tape_list[:-1]

        # Force a repaint of the panel
        self.panel2.Refresh()
    
    def MoveLeft(self, event):
        # Shift the colors to the left
        self.tape_list = self.tape_list[1:] + [self.tape_list[0]]
    
    # Force a repaint of the panel
        self.panel2.Refresh()
        



class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Python Turing Machine Revamped", 15)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()