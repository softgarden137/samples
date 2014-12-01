from System import * # for Convert
from System.Windows import * # for NameProperty
from System.Windows.Controls import UserControl, Canvas
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

xaml_Dot3_str = """
<UserControl xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <UserControl.Resources>
    <Storyboard x:Name="spin">
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="sat" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[2].(RotateTransform.Angle)">
        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="1"></SplineDoubleKeyFrame>
        <SplineDoubleKeyFrame KeyTime="00:00:01.7000000" Value="359"></SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
      <PointAnimationUsingKeyFrames BeginTime="00:00:00" Duration="00:00:00.0010000" Storyboard.TargetName="sat" Storyboard.TargetProperty="(UIElement.RenderTransformOrigin)">
        <SplinePointKeyFrame KeyTime="00:00:00" Value="-0.744000017642975,-0.669000029563904"></SplinePointKeyFrame>
      </PointAnimationUsingKeyFrames>
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Duration="00:00:00.0010000" Storyboard.TargetName="sat" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[3].(TranslateTransform.X)">
        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="0.071"></SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Duration="00:00:00.0010000" Storyboard.TargetName="sat" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[3].(TranslateTransform.Y)">
        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="-0.073"></SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="sat" Storyboard.TargetProperty="(UIElement.Opacity)">
        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="1"></SplineDoubleKeyFrame>
        <SplineDoubleKeyFrame KeyTime="00:00:00.3000000" Value="1"></SplineDoubleKeyFrame>
        <SplineDoubleKeyFrame KeyTime="00:00:01.7000000" Value="0"></SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="_base" Storyboard.TargetProperty="(UIElement.Opacity)">
        <SplineDoubleKeyFrame KeyTime="00:00:00.3000000" Value="1"></SplineDoubleKeyFrame>
        <SplineDoubleKeyFrame KeyTime="00:00:01.7000000" Value="0"></SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
      <PointAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="_base" Storyboard.TargetProperty="(UIElement.RenderTransformOrigin)">
        <SplinePointKeyFrame KeyTime="00:00:00" Value="0.30799999833107,0.30799999833107"></SplinePointKeyFrame>
        <SplinePointKeyFrame KeyTime="00:00:00.3000000" Value="0,0"></SplinePointKeyFrame>
      </PointAnimationUsingKeyFrames>
      <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="_base" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[2].(RotateTransform.Angle)">
        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="1"></SplineDoubleKeyFrame>
        <SplineDoubleKeyFrame KeyTime="00:00:00.3000000" Value="0"></SplineDoubleKeyFrame>
        <SplineDoubleKeyFrame KeyTime="00:00:01.7000000" Value="180"></SplineDoubleKeyFrame>
      </DoubleAnimationUsingKeyFrames>
    </Storyboard>
  </UserControl.Resources>
  <Canvas x:Name="LayoutRoot">
    <Ellipse Height="20" Width="20" Canvas.Left="-4.5" Canvas.Top="-4.5" Fill="#FFE67323" Stroke="#FF21E8D4" StrokeDashOffset="0" StrokeDashArray="1 2" x:Name="_base" StrokeThickness="3" RenderTransformOrigin="0.5,0.5">
      <Ellipse.RenderTransform>
        <TransformGroup>
          <ScaleTransform></ScaleTransform>
          <SkewTransform></SkewTransform>
          <RotateTransform></RotateTransform>
          <TranslateTransform></TranslateTransform>
        </TransformGroup>
      </Ellipse.RenderTransform>
    </Ellipse>
    <Ellipse Height="5" Width="5" Canvas.Left="3" Canvas.Top="3" Fill="#FFFFFFFF" x:Name="sat" RenderTransformOrigin="0.5,0.5">
      <Ellipse.RenderTransform>
        <TransformGroup>
          <ScaleTransform></ScaleTransform>
          <SkewTransform></SkewTransform>
          <RotateTransform></RotateTransform>
          <TranslateTransform></TranslateTransform>
        </TransformGroup>
      </Ellipse.RenderTransform>
    </Ellipse>
  </Canvas>
</UserControl>
"""

#
# define class that procedurally creates Tile code instead of XAML
#
class Dot(UserControl):
     def __init__(self, xaml):
          self.xaml = xaml
          
          self.Content = XamlReader.Load(self.xaml)
              
          def spin_Completed(sender, e): # Storyboard is define in XAML
              self.Parent.Children.Remove(self);
                  
          self.Content.spin.Completed += spin_Completed
                  
          self.Content.spin.Begin();
              
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
    client.DownloadStringAsync(MakeUri("dot3.xaml"))

def LoadDot2():
    global _dot
    _dot = xaml_Dot3_str
    Main()

          
def Main():
    x = 0
    layoutRoot.MouseMove += Page_MouseMove 
          
#LoadDot()
LoadDot2()
 


