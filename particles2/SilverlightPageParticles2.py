from System import * # for Convert
from System.Windows.Controls import UserControl, Canvas
from System.Windows import * # for NameProperty
from System.Windows.Shapes import * # exposes Rectangle to scope since not added by default
from System.Windows.Media.Animation import * # exposes Storyboard
#from System.Windows.Media.Imaging import * # for bitmap
from System.Diagnostics import * # enables outputing to a debug window
from System.Net import * # for WebClient
from System.Windows.Resources import * # for WebClient
from System.Windows.Markup import * # for XamlReader
from Microsoft.Scripting.Silverlight.DynamicApplication import MakeUri

layoutRoot = me.LayoutRoot
_dot = None

_Dot2_xaml_str = """
<UserControl xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <UserControl.Resources>
    <Storyboard x:Name="sbDrop">
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:01" Storyboard.TargetName="ellipse" Storyboard.TargetProperty="(Canvas.Top)">
        <SplineDoubleKeyFrame KeyTime="00:00:00.5" Value="200">
          <SplineDoubleKeyFrame.KeySpline>
            <KeySpline ControlPoint1="0,0" ControlPoint2="1,0"></KeySpline>
          </SplineDoubleKeyFrame.KeySpline>
        </SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:001.25" Storyboard.TargetName="ellipse" Storyboard.TargetProperty="(UIElement.Opacity)">
        <SplineDoubleKeyFrame KeyTime="00:00:00.25" Value="0"></SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
    </Storyboard>
  </UserControl.Resources>
  <Canvas x:Name="LayoutRoot">
    <Ellipse x:Name="ellipse" Fill="#FF00FF" Width="4" Height="4" Canvas.Left="-2" Canvas.Top="-2"></Ellipse>
  </Canvas>
</UserControl>
"""


#
# define class that procedurally creates Tile code instead of XAML
#
class Dot(UserControl):
    def __init__(self, xaml):
        self.xaml = xaml
          
        self.Content = XamlReader.Load(self.xaml)   # Silverligt
        #self.Content = XamlReader.Parse(self.xaml) # WPF
              
        def sbDrop_Completed(sender, e): # Storyboard is define in XAML
            self.Parent.Children.Remove(self);
                  
        self.Content.sbDrop.Completed += sbDrop_Completed
        self.Content.sbDrop.Begin();

        #self.sbDrop = self.Content.FindName("sbDrop") # wpf
        #self.sbDrop.Completed += sbDrop_Completed # wpf
        #self.sbDrop.Begin(); # wpf
              
              
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
          
def DotLoaded(sender, e):
    global _dot
    _dot = e.Result
    Main()
          
def DotLoaded2():
    global _dot
    _dot = _Dot2_xaml_str
    Main()

def Page_MouseMove(sender, e):
    global layoutRoot
    global _dot
    d = Dot(_dot)
    d.X = e.GetPosition(layoutRoot).X;
    d.Y = e.GetPosition(layoutRoot).Y;
    layoutRoot.Children.Add(d);

def LoadDot():
    client = WebClient()
    client.DownloadStringCompleted += DotLoaded
    client.DownloadStringAsync(MakeUri("Dot2.xaml"))

          
def Main():
    layoutRoot.MouseMove += Page_MouseMove 

#LoadDot()
DotLoaded2() # new
