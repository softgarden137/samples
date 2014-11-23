from System import * # for Uri
from System.Windows import * 
from System.Windows.Controls import UserControl, Canvas
from System.Windows.Shapes import * # exposes Rectangle to scope since not added by default
from System.Windows.Media.Animation import * # exposes Storyboard
from System.Windows.Media import * # exposes CompositionTarget
#from System.Windows.Media.Imaging import * # for bitmap
from System.Net import * # for WebClient
#from System.Windows.Resources import * # for WebClient
#from System.Xml import *
#from System.Xml.Linq import *
from System.Diagnostics import * # enables outputing to a debug window!
from System.Windows.Markup import * # for XamlReader
#from Microsoft.Scripting.Silverlight.DynamicApplication import MakeUri
    
xaml_SnowFlake_str = """
<UserControl 
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" 
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    Width="20" Height="20">
    <Grid x:Name="LayoutRoot">
        <Ellipse Fill="#FFFFFFFF"></Ellipse>
    </Grid>
</UserControl>
"""
    
class Snowflake(UserControl):
    def __init__(self, xaml, randomNumber):
        self.xaml = xaml
        self.randomNumber = randomNumber
        self.x = 0
        self.y = 0
        self.xSpeed = 0
        self.ySpeed = 0
        self.radius = 0
        self.scale = 0
        self.alpha = 0
        self.stageSize = Point()
        self.Content = XamlReader.Load(self.xaml)
            
        #
        # This method gets called many times a second and is responsible for moving your snowflake around
        #
        def MoveSnowFlake(sender, e):
            self.x = self.x + self.xSpeed
            self.y = self.y + self.ySpeed
    
            Canvas.SetTop(self, self.y)
            Canvas.SetLeft(self, Canvas.GetLeft(self) + self.radius * Math.Cos(self.x))
    
            # Reset the position to go back to the top when the bottom boundary is reached
            if (Canvas.GetTop(self) > self.stageSize.Y):
                Canvas.SetTop(self, - self.ActualHeight - 10)
                self.y = Canvas.GetTop(self)
    
        CompositionTarget.Rendering += MoveSnowFlake
                     
    def SetInitialProperties(self, stageWidth, stageHeight):
        self.xSpeed = self.randomNumber.NextDouble() / 20
        self.ySpeed = .01 + self.randomNumber.NextDouble() * 2
        self.radius = self.randomNumber.NextDouble()
        self.scale = .01 + self.randomNumber.NextDouble() * 2
        self.alpha = .1 + self.randomNumber.NextDouble()
    
        # Setting initial position
        Canvas.SetLeft(self, self.randomNumber.Next(stageWidth))
        Canvas.SetTop(self, self.randomNumber.Next(stageHeight))
    
        self.stageSize = Point(stageWidth, stageHeight)
    
        self.y = Canvas.GetTop(self)
    
        # Setting initial size and opacity
        self.Content.Width = 5 * self.scale
        self.Content.Height = 5 * self.scale
        self.Content.Opacity = self.alpha
       
class Snow(object): 
    def __init__(self):
        _snowflake = xaml_SnowFlake_str

        randomNumber = Random()    
        for i in range(0, 200):
            snowflake = Snowflake(_snowflake, randomNumber);
            # 600 and 300 is the width/height of the application
            snowflake.SetInitialProperties(600, 300);
            me.LayoutRoot.Children.Add(snowflake);

Snow()
