import wx
from math import sqrt
from wx import dataview as dv

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, tape_size):
        wx.Frame.__init__(self, None, -1, title, size=(1280, 720))
        
        self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))
        
        self.color_map = {'b': 'WHITE', '0': 'RED', '1': 'BLUE'}
        self.tape_size = tape_size
        self.selected_circle = self.tape_size // 2
        self.InitTape()
        
        

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

        self.panel2.Bind(wx.EVT_PAINT, self.ResizeDrawCircles)

        # Create a vertical box sizer
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(3,3)
        box_sizer.AddStretchSpacer()
        
        self.set_blank_button = wx.Button(self.panel2, label='b')
        self.set_blank_button.Bind(wx.EVT_BUTTON,  lambda x: [self.SetColor(color='b')])
        grid_sizer.Add(self.set_blank_button, pos=(0, 0))  # Add the button to the sizer
        
        self.set_zero_button = wx.Button(self.panel2, label='0')
        self.set_zero_button.Bind(wx.EVT_BUTTON,  lambda x: [self.SetColor(color='0')])
        grid_sizer.Add(self.set_zero_button, pos=(0, 1))  # Add the button to the sizer
        
        self.set_one_button = wx.Button(self.panel2, label='1')
        self.set_one_button.Bind(wx.EVT_BUTTON, lambda x: [self.SetColor(color='1')])
        grid_sizer.Add(self.set_one_button, pos=(0, 2))  # Add the button to the sizer

        
        self.clear_all_button = wx.Button(self.panel2, label='Clear')
        self.clear_all_button.Bind(wx.EVT_BUTTON, self.ClearPaint)
        grid_sizer.Add(self.clear_all_button, pos=(1, 0))  # Add the button to the sizer
        
        self.move_left_button = wx.Button(self.panel2, label='Left')
        self.move_left_button.Bind(wx.EVT_BUTTON, self.MoveLeft)
        grid_sizer.Add(self.move_left_button, pos=(1, 1))  # Add the button to the sizer

        self.move_right_button = wx.Button(self.panel2, label='Right')
        self.move_right_button.Bind(wx.EVT_BUTTON, self.MoveRight)
        grid_sizer.Add(self.move_right_button, pos=(1, 2))  # Add the button to the sizer
        
        self.reset_button = wx.Button(self.panel2, label='Reset')
        self.reset_button.Bind(wx.EVT_BUTTON, lambda x: [self.InitTape(), self.ResizeDrawCircles()])
        grid_sizer.Add(self.reset_button, pos=(2, 0), span=(1, 3), flag=wx.EXPAND)  # Make the button span 3 columns

        box_sizer.Add(grid_sizer, 0, wx.ALIGN_CENTER)
        box_sizer.AddStretchSpacer()
        
        # Set the sizer on the panel
        self.panel2.SetSizer(box_sizer)

        splitter.SplitVertically(panel1, self.panel2)
        splitter.SetSashPosition(self.GetSize().width // 3)

    def OnSize(self, event:wx.Event):
        table_width = self.listctrl.GetSize()[0] #GetSize returns (width, height) tuple
        num_col = self.listctrl.GetColumnCount()
        col_width = table_width/num_col
        for i in range(0, num_col):
            self.listctrl.GetColumn(i).SetWidth(int(col_width))
        event.Skip()  # Skip the event

    def ResizeDrawCircles(self, *args):
        dc = wx.ClientDC(self.panel2)
        dc.Clear()  # Clear the drawing area

        panel2_width = self.panel2.GetSize()[0]
        panel2_height = self.panel2.GetSize()[1]
        radius = int(panel2_width/80)

        for i in range(25):
            value = self.tape_list[self.position-12+i]
            color = self.color_map[value]

            dc.SetBrush(wx.Brush(color))  # Set the color of the circle
            dc.SetPen(wx.Pen('BLACK'))  # Set the color of the border
            
            x = i * panel2_width / 26 + ((i+1) * (panel2_width/ (26*25))) + radius*1.5
            y =  i * panel2_height / 26 + ((i+1) * (panel2_height/ (26*25))) + radius*1.5

            dc.DrawCircle(int(x), int(y), radius)

    def SetColor(self, color, *args):
        print(color)
        self.tape_list[self.position] = color
        self.ResizeDrawCircles()
        
    def ClearPaint(self, event):
        for i in range(self.tape_size):
            self.tape_list[i] = 'b'
        self.ResizeDrawCircles()

    def InitTape(self):
        self.tape_list = ["b"] * self.tape_size
        self.position = self.tape_size//2

    def MoveLeft(self, event):
    # Shift the colors to the right
        self.position += 1
        print(self.position)

        # If we're at the edge of the tape, add a 'b' at the end
        if self.position >= self.tape_size-13:
            self.tape_list.append('b')
            self.tape_size += 1

        self.ResizeDrawCircles()

    def MoveRight(self, event):
        self.position -= 1

        # If we're at the edge of the tape, add a 'b' at the start
        if self.position < 0:
            self.tape_list.insert(0, 'b')
            self.position = 0  # Reset position to start of the tape

        self.ResizeDrawCircles()



class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Python Turing Machine Revamped", 25)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()