from System import * # for Uri
from System.Windows import * 
from System.Windows.Controls import *
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
 
from datetime import datetime
import calculator

_Calc_xaml_str = """
<UserControl
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    mc:Ignorable="d"
    d:DesignHeight="310" d:DesignWidth="230">
    <Canvas Background="LightGray">
        <Canvas Name="Calc">
            <Canvas Name="Layer2">
                <Rectangle Stroke="#FF000000" RadiusX="0" RadiusY="0" StrokeThickness="5" StrokeMiterLimit="2" StrokeEndLineCap="Flat" StrokeStartLineCap="Flat" StrokeLineJoin="Miter" Name="Rectangle1" Width="231" Height="311" Canvas.Left="-1" Canvas.Top="0">
                    <Rectangle.Fill>
                        <LinearGradientBrush StartPoint="0,0.5" EndPoint="1,0.5">
                            <LinearGradientBrush.GradientStops>
                                <GradientStop Color="sc#1.000000, 0.157502, 0.408674, 0.808030" Offset="0"/>
                                <GradientStop Color="#FFFFFFFF" Offset="1"/>
                            </LinearGradientBrush.GradientStops>
                        </LinearGradientBrush>
                    </Rectangle.Fill>
                    <Rectangle.RenderTransform>
                        <TransformGroup>
                            <TranslateTransform X="-115.5" Y="-155.5"/>
                            <ScaleTransform ScaleX="1" ScaleY="1"/>
                            <SkewTransform AngleX="0" AngleY="0"/>
                            <RotateTransform Angle="0"/>
                            <TranslateTransform X="115.5" Y="155.5"/>
                            <TranslateTransform X="0" Y="0"/>
                        </TransformGroup>
                    </Rectangle.RenderTransform>
                </Rectangle>
            </Canvas>
            <Canvas Name="Layer1" >
                <TextBox Name="Result" Width="135" Height="33.5533333333333" Canvas.Left="20" Canvas.Top="65"/>
                <Border Width="191" Height="48" Canvas.Left="18" Canvas.Top="11" BorderThickness="1"  CornerRadius="4" BorderBrush="#FF828282">
                    <TextBlock Name="Title1" HorizontalAlignment="Center" VerticalAlignment="Center" FontFamily="Perpetua Titling MT" FontStyle="Italic" FontWeight="700" FontSize="20" Foreground="sc#1.000000, 0.172911, 0.172911, 0.172910">IronCalc2007</TextBlock>
                </Border>
                <StackPanel x:Name="mySP" Canvas.Left="18" Canvas.Top="11"/>
                <Button Name="One" Content="1" Width="40" Height="40" Canvas.Left="20" Canvas.Top="110"/>
                <Button Name="Nine" Content="9" Width="40" Height="40" Canvas.Left="120" Canvas.Top="210"/>
                <Button Name="Eight" Content="8" Width="40" Height="40" Canvas.Left="70" Canvas.Top="210"/>
                <Button Name="Five" Content="5" Width="40" Height="40" Canvas.Left="70" Canvas.Top="162"/>
                <Button Name="Four" Content="4" Width="40" Height="40" Canvas.Left="20" Canvas.Top="162"/>
                <Button Name="Two" Content="2" Width="40" Height="40" Canvas.Left="70" Canvas.Top="110"/>
                <Button Name="Three" Content="3" Width="40" Height="40" Canvas.Left="120" Canvas.Top="110"/>
                <Button Name="Six" Content="6" Width="40" Height="40" Canvas.Left="120" Canvas.Top="162"/>
                <Button Name="Multiply" Content="*" Width="40" Height="40" Canvas.Left="170" Canvas.Top="162"/>
                <Button Name="Seven" Content="7" Width="40" Height="40" Canvas.Left="20" Canvas.Top="210"/>
                <Button Name="Subtract" Content="-" Width="40" Height="40" Canvas.Left="170" Canvas.Top="210"/>
                <Button Name="Zero" Content="0" Width="40" Height="40" Canvas.Left="20" Canvas.Top="260"/>
                <Button Name="DecimalPoint" Content="." Width="40" Height="40" Canvas.Left="70" Canvas.Top="260"/>
                <Button Name="Equals" Content="=" Width="40" Height="40" Canvas.Left="120" Canvas.Top="260"/>
                <Button Name="Plus" Content="+" Width="40" Height="40" Canvas.Left="170" Canvas.Top="260"/>
                <Button Name="Divide" Content="/" Width="40" Height="40" Canvas.Left="170" Canvas.Top="110"/>
                <Button Name="Clear" Content="C" Width="40" Height="40" Canvas.Left="169" Canvas.Top="62"/>
            </Canvas>
        </Canvas>

    </Canvas>

</UserControl>
"""

_Clock_xaml_str = """
<Canvas
    xmlns="http://schemas.microsoft.com/client/2007"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    Opacity="0" x:Name="parentCanvas">

    <Canvas.Triggers>
        <EventTrigger RoutedEvent="Canvas.Loaded">
            <EventTrigger.Actions>
                <BeginStoryboard>
                    <Storyboard>
                        <DoubleAnimation x:Name="hourAnimation" Storyboard.TargetName="hourHandTransform" Storyboard.TargetProperty="Angle" From="180" To="540" Duration="12:0:0" RepeatBehavior="Forever"/>
                        <DoubleAnimation x:Name="minuteAnimation" Storyboard.TargetName="minuteHandTransform" Storyboard.TargetProperty="Angle" From="180" To="540" Duration="1:0:0" RepeatBehavior="Forever"/>
                        <DoubleAnimation x:Name="secondAnimation" Storyboard.TargetName="secondHandTransform" Storyboard.TargetProperty="Angle" From="180" To="540" Duration="0:1:0" RepeatBehavior="Forever"/>
                        <DoubleAnimation Storyboard.TargetName="parentCanvas" Storyboard.TargetProperty="Opacity" From="0" To="0.7" Duration="0:0:4"/>
                    </Storyboard>
                </BeginStoryboard>
            </EventTrigger.Actions>
        </EventTrigger>
    </Canvas.Triggers>

    <!-- Drop shadow -->
    <Path Data="M 157, 5 a 150,150 0 1,0 1,0 z">
        <Path.Fill>
            <SolidColorBrush Color="Black" Opacity="0.3"/>
        </Path.Fill>
    </Path>

    <!-- Clock bezel -->
    <Path Data="M 150, 0 a 150,150 0 1,0 1,0 z" Fill="black" />
    <Path Data="M 150, 1 a 149,149 0 1,0 1,0 z" >
        <Path.Fill>
            <LinearGradientBrush>
                <LinearGradientBrush.GradientStops>
                    <GradientStopCollection>
                        <GradientStop Color="silver" Offset="0.05"/>
                        <GradientStop Color="#333333" Offset="0.95"/>
                    </GradientStopCollection>
                </LinearGradientBrush.GradientStops>
            </LinearGradientBrush>
        </Path.Fill>
    </Path>
    <Path Data="M 150, 15 a 135,135 0 1,0 1,0 z" Fill="black" Opacity="1"/>
    <Path Data="M 150, 16 a 134,134 0 1,0 1,0 z" Opacity="1">
        <Path.Fill>
            <LinearGradientBrush>
                <LinearGradientBrush.GradientStops>
                    <GradientStopCollection>
                        <GradientStop Color="#333333" Offset="0.05"/>
                        <GradientStop Color="silver" Offset="0.95"/>
                    </GradientStopCollection>
                </LinearGradientBrush.GradientStops>
            </LinearGradientBrush>
        </Path.Fill>
    </Path>

    <!-- Clock face -->
    <Path Data="M 150, 23 a 127,127 0 1,0 1,0 z" Fill="black" Opacity="1"/>
    <!-- Hour hand -->
    <Path Data="M -4, 16 l 3 40 3 0 2 -40 z" Fill="white">
        <Path.RenderTransform>
            <TransformGroup>
                <RotateTransform x:Name="hourHandTransform" Angle="180"/>
                <TranslateTransform X="150.5" Y="145"/>
            </TransformGroup>
        </Path.RenderTransform>
    </Path>

    <!-- Minute hand -->
    <Path Data="M -4, 16 l 3 70 3 0 2 -70 z" Fill="white">
        <Path.RenderTransform>
            <TransformGroup>
                <RotateTransform x:Name="minuteHandTransform" Angle="180"/>
                <TranslateTransform X="150.5" Y="145"/>
            </TransformGroup>
        </Path.RenderTransform>
    </Path>

    <!-- Second hand -->
    <Path Data="M -1, 16 l 0 70 2 0 0 -70 z" Fill="red">
        <Path.RenderTransform>
            <TransformGroup>
                <RotateTransform x:Name="secondHandTransform" Angle="180"/>
                <TranslateTransform X="150.5" Y="145"/>
            </TransformGroup>
        </Path.RenderTransform>
    </Path>

</Canvas>
"""

def Walk(tree):
    yield tree
    if hasattr(tree, 'Children'):
        for child in tree.Children:
            for x in Walk(child):
                yield x
    elif hasattr(tree, 'Child'):
        for x in Walk(tree.Child):
            yield x
    elif hasattr(tree, 'Content'):
        for x in Walk(tree.Content):
            yield x

class Calc(Object):
    def __init__(self):
        #self.Content = LoadXaml('calc.xaml')
        self.Content = XamlReader.Load(_Calc_xaml_str)
        controls = [ n for n in Walk(self.Content) if isinstance(n, Button) or isinstance(n, TextBox) ]
        for c in controls: c.FontSize *=2
        calculator.enliven(self.Content)

class Clock(Object):
    def __init__(self):
        #self.Content = LoadXaml('clock.xaml')
        self.Content = XamlReader.Load(_Clock_xaml_str)
        self.start()

    def _fromAngle(self, time, divisor = 5, offset = 0):
        return ((time / (12.0 * divisor)) * 360) + offset + 180

    def _toAngle(self, time):
        return self._fromAngle(time) + 360

    def start(self):
        d = datetime.now()

        #self.Content.FindName('hourAnimation').From    = self._fromAngle(d.hour, 1, d.minute/2)
        #self.Content.FindName('hourAnimation').To      = self._toAngle(d.hour)
        from_h = self._fromAngle(d.hour, 1, d.minute/2)
        to_h = from_h + 360.0
        self.Content.FindName('hourAnimation').From    = from_h
        self.Content.FindName('hourAnimation').To      = to_h
        self.Content.FindName('minuteAnimation').From  = self._fromAngle(d.minute)
        self.Content.FindName('minuteAnimation').To    = self._toAngle(d.minute)
        self.Content.FindName('secondAnimation').From  = self._fromAngle(d.second)
        self.Content.FindName('secondAnimation').To    = self._toAngle(d.second)

class Drag(object):
    def __init__(self,root,obj):
        self.click = None
        self.obj = obj
        self.root = root

    def OnClick(self,sender, e):
        self.click = e.GetPosition(self.root)
        self.sx = Canvas.GetLeft(self.obj)
        self.sy = Canvas.GetTop(self.obj)
        if (self.sx.IsNaN(self.sx)): self.sx = 0.0
        if (self.sy.IsNaN(self.sy)): self.sy = 0.0
        # NaN (Not a Number)
        self.obj.CaptureMouse()
    
    def OnClick2(self,sender, e):
        if(self.click != None):
            self.obj.ReleaseMouseCapture()
            self.click = None

    def OnClick3(self,sender, e):
        if(self.click != None):
            mouse_pos = e.GetPosition(self.root)
            Canvas.SetLeft(self.obj, (self.sx + mouse_pos.X - self.click.X))
            Canvas.SetTop(self.obj, (self.sy + mouse_pos.Y - self.click.Y))

    def enable(self):
         self.obj.MouseLeftButtonDown += self.OnClick
         self.obj.MouseLeftButtonUp += self.OnClick2
         self.obj.MouseMove += self.OnClick3

    def disable(self):
         self.obj.MouseLeftButtonDown -= self.OnClick
         self.obj.MouseLeftButtonUp -= self.OnClick2
         self.obj.MouseMove -= self.OnClick3


class App(object):
    def __init__(self):
        self.Content = me

        self.calc = Calc().Content
        #self.Content.Children.Add (self.calc)
        me.rootCanvas.Children.Add (self.calc)

        self.clock = Clock().Content
        #self.Content.Children.Add (self.clock)
        me.rootCanvas.Children.Add (self.clock)
        Canvas.SetTop(self.clock, 10)
        Canvas.SetLeft(self.clock, 10)

        #Canvas.SetTop(self.calc, 10)
        #Canvas.SetLeft(self.calc, 350)
        #from System.Windows import DependencyObject
        DependencyObject.SetValue(self.calc, Canvas.TopProperty, 10.0)
        DependencyObject.SetValue(self.calc, Canvas.LeftProperty, 350.0)

        d1 = Drag(root=me.rootCanvas,obj=self.calc )
        d1.enable()

        d2 = Drag(root=me.rootCanvas,obj=self.clock)
        d2.enable()
App()
