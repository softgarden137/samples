from System import * # for Convert
from System.Windows.Controls import Canvas, UserControl
from System.Windows.Shapes import * # exposes Rectangle to scope since not added by default
from System.Windows.Media import *
from System.Windows.Media.Animation import * # exposes Storyboard
#from System.Windows.Media.Imaging import * # for bitmap
from System.Windows import Point
from System.Diagnostics import * # enables outputing to a debug window!

layoutRoot = me.LayoutRoot
tiles = me.tiles
mouse = Point(0, 0)

#
# define class that procedurally creates Tile code instead of XAML
#
class Tile(Canvas): # inherits from Canvas
    def __init__(self):

        self.targetAngle = 0
        layoutRoot = Canvas()
        self.Children.Add(layoutRoot)

        self.bkg = Canvas()
        self.bkg.Width = 30
        self.bkg.Height = 10
        self.bkg.Background = SolidColorBrush(Colors.White)
        self.bkg.RenderTransformOrigin = Point (0.5,0.5)
        Canvas.SetLeft(self.bkg, -15)
        Canvas.SetTop (self.bkg, -5)
        layoutRoot.Children.Add(self.bkg)

        self.scale = ScaleTransform()
        self.scale.ScaleX = 1.0
        self.scale.ScaleY = 1.0

        self.rotation = RotateTransform()
        self.rotation.Angle = 0

        transformGroup = TransformGroup()
        transformGroup.Children.Add(self.scale)
        transformGroup.Children.Add(self.rotation)
        self.bkg.RenderTransform = transformGroup

        dc = DoubleCollection();
        dc.Add(1);
        dc.Add(2);

        ellipse = Ellipse()
        ellipse.Stroke = SolidColorBrush(Color.FromArgb(0xFF,0xFF,0x00,0xFF))
        ellipse.StrokeDashArray = dc

        ellipse.Width = 10
        ellipse.Height = 10
        Canvas.SetLeft(ellipse, -5)
        Canvas.SetTop (ellipse, -5)
        layoutRoot.Children.Add(ellipse)

        def sb_Completed(sender, e):
            self.rotation.Angle = self.rotation.Angle + ( self.targetAngle - self.rotation.Angle)*.08
            sb.Begin()

        sb = Storyboard()
        sb.Completed += sb_Completed
        layoutRoot.Resources.Add("sb",sb)
        sb.Begin()

    def SetX(self, value):
        self.SetValue(Canvas.LeftProperty, Convert.ToDouble(value))
    def GetX(self):
        return self.GetValue(Canvas.LeftProperty)
    X = property(GetX, SetX)

    def SetY(self, value):
        self.SetValue(Canvas.TopProperty, Convert.ToDouble(value))
    def GetY(self):
        return self.GetValue(Canvas.TopProperty)
    Y = property(GetY, SetY)

    def SetBackground(self, value):
        self.bkg.Background = value
    def GetBackground(self):
        return self.bkg.Background
    background = property(GetBackground, SetBackground)

def Page_MouseMove(sender, e):
    global mouse
    global layoutRoot
    mouse = e.GetPosition(layoutRoot)

def sb_Completed(sender, e):
    global tiles
    global sb
    global mouse
    for s in tiles.Children:
        _y = s.Y - mouse.Y
        _x = s.X - mouse.X
        distance = Math.Sqrt((_y * _y) + (_x * _x))
        rad = Math.Atan2(_y, _x)
        angle = rad * (180/Math.PI)
        s.scale.ScaleX = .6 + ((distance / 300.0))
        s.scale.ScaleY = s.scale.ScaleX
        if distance < 200:
            s.targetAngle = angle - 180
        else: 
            s.targetAngle = 0
    sb.Begin()    
      
layoutRoot.MouseMove += Page_MouseMove
      
for x in range(0,15):
    for y in range(0, 10):
        s = Tile()
        s.background = SolidColorBrush(Color.FromArgb(0xcc,Convert.ToByte((100 + (x*10))),0,Convert.ToByte((100 + (y*15)))))
        s.X = 115 + (x * 25)
        s.Y = 25 + (y * 25)
        tiles.Children.Add(s)
      
sb = Storyboard()
sb.Completed += sb_Completed
layoutRoot.Resources.Add("sb", sb)
sb.Begin()
