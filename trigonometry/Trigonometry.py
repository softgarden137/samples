from System import * # for Convert
from System.Windows import * # for NameProperty
from System.Windows.Controls import UserControl, Canvas
from System.Windows.Media import SolidColorBrush, Color
from System.Windows.Shapes import * # exposes Rectangle to scope since not added by default
from System.Windows.Media.Animation import * # exposes Storyboard
#from System.Windows.Media.Imaging import * # for bitmap
from System.Diagnostics import * # enables outputing to a debug window!

layoutRoot = me.LayoutRoot
Dots = me.Dots

mouse = Point(0, 0)
origin = Point(110, 110);
radius = 100
follow = None
tween = None
curAngle = 0;

class Dot(Canvas):
    def __init__(self):
    
        layoutRoot = Canvas()
        self.Children.Add(layoutRoot)
        self.kill = 100
        
        self.bkg = Ellipse()
        self.bkg.Width = 8
        self.bkg.Height = 8
        self.bkg.Fill = SolidColorBrush(Color.FromArgb(0xFF,0xFF,0x99,0xFF))
        Canvas.SetLeft(self.bkg, -4)
        Canvas.SetTop (self.bkg, -4)
        layoutRoot.Children.Add(self.bkg)
        
        def sb2_Completed(sender, e):
            if self.kill > 0:
                self.bkg.Opacity = self.kill / 100.0
                self.kill = self.kill - 5
                self.sb2.Begin();
            else:
                (self.Parent).Children.Remove(self)
    
        self.sb2 = Storyboard()
        layoutRoot.Resources.Add("sb2", self.sb2)   
        self.sb2.Completed += sb2_Completed
    
    def fade(self):
            self.sb2.Begin()
        
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

def Page_MouseMove(sender, e):
    global mouse
    global layoutRoot
    mouse = e.GetPosition(layoutRoot)
    
def setAngle():
    global mouse
    global targetAngle
    global origin
    global follow
    global radius
    global curAngle
    global Dots
    _x = mouse.X - origin.X
    _y = -1 *(mouse.Y - origin.Y)
    targetAngle = Math.Atan2(_y, _x) / (Math.PI / 180)
    if targetAngle < 0: 
        targetAngle = targetAngle + 360
    # we set follow directly to the calculated value
    follow.X = origin.X + (Math.Cos(targetAngle * (Math.PI / 180)) * radius)
    follow.Y = origin.Y - (Math.Sin(targetAngle * (Math.PI / 180)) * radius)
    # Prevent the tween jump by massaging the angle values...
    distance = targetAngle - curAngle
    if distance > 180:
        distance = distance - 360
    if distance <= -180:
        distance = distance + 360
    step = distance * .1
    curAngle = curAngle + step
    if curAngle < 0: 
        curAngle = curAngle + 360
    if curAngle > 360:
        curAngle = curAngle - 360
    tween.X = origin.X + (Math.Cos(curAngle * (Math.PI / 180)) * radius)
    tween.Y = origin.Y - (Math.Sin(curAngle * (Math.PI / 180)) * radius)
    d =  Dot()
    d.X = tween.X
    d.Y = tween.Y
    d.fade()
    Dots.Children.Add(d)   
    
def sb_Completed(sender, e):
    global sb
    setAngle()
    sb.Begin() 

layoutRoot.MouseMove += Page_MouseMove

d = Dot();
d.X = origin.X;
d.Y = origin.Y;
layoutRoot.Children.Add(d);

follow = Dot()
follow.bkg.Fill = SolidColorBrush(Color.FromArgb(0xcc, 0xff, 0xFF, 0xff))
#follow.SetValue(NameProperty, "follow")
follow.Name = "follow"
follow.X = origin.X + radius
follow.Y = origin.Y
layoutRoot.Children.Add(follow)

tween = Dot()
#tween.SetValue(NameProperty, "tween")
tween.Name = "tween"
tween.X = origin.X + radius
tween.Y = origin.Y
Dots.Children.Add(tween)

sb = Storyboard()
sb.Completed += sb_Completed
layoutRoot.Resources.Add("sb", sb)

sb.Begin()
