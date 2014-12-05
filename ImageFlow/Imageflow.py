from System import *
from System.Net import *
from System.Windows import * 
from System.Windows.Controls import *
from System.Windows.Input import *
from System.Windows.Media import *
from System.Windows.Shapes import *
from System.Windows.Media.Animation import *
from System.Windows.Media.Imaging import * # for bitmap
from System.Net import * # for WebClient
from System.Windows.Resources import * # for WebClient
from System.Windows.Markup import * # for XamlReader
from System.Collections.Generic import *
from System.Collections.ObjectModel import *
from System.Windows.Browser import *
from Microsoft.Scripting.Silverlight.DynamicApplication import MakeUri


images = ObservableCollection[String]()
_imageflow = None
_imageflowItem = None
c = None


_imageflow_xaml_str = """
<ItemsControl
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" 
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"  
    >
    <ItemsControl.ItemsPanel>
        <ItemsPanelTemplate>
          <Canvas></Canvas>
        </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
</ItemsControl>
"""

_imageflowItem_xaml_str = """
<Grid
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" 
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    >
    <Grid x:Name="LayoutRoot">
        <Grid.Resources>
            <Storyboard x:Name="Animation">
                <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="Rotator" Storyboard.TargetProperty="RotationY">
                    <EasingDoubleKeyFrame x:Name="rotationKeyFrame" KeyTime="00:00:00.9" Value="0">
                        <EasingDoubleKeyFrame.EasingFunction>
                            <CubicEase />
                        </EasingDoubleKeyFrame.EasingFunction>
                    </EasingDoubleKeyFrame>
                </DoubleAnimationUsingKeyFrames>
                <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="Rotator" Storyboard.TargetProperty="LocalOffsetZ">
                    <EasingDoubleKeyFrame x:Name="offestZKeyFrame" KeyTime="00:00:00.9" Value="0">
                        <EasingDoubleKeyFrame.EasingFunction>
                            <CubicEase />
                        </EasingDoubleKeyFrame.EasingFunction>
                    </EasingDoubleKeyFrame>
                </DoubleAnimationUsingKeyFrames>
                <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="scaleTransform" Storyboard.TargetProperty="ScaleX">
                    <EasingDoubleKeyFrame x:Name="scaleXKeyFrame" KeyTime="00:00:00.9" Value="1">
                        <EasingDoubleKeyFrame.EasingFunction>
                            <CubicEase />
                        </EasingDoubleKeyFrame.EasingFunction>
                    </EasingDoubleKeyFrame>
                </DoubleAnimationUsingKeyFrames>
                <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="scaleTransform" Storyboard.TargetProperty="ScaleY">
                    <EasingDoubleKeyFrame x:Name="scaleYKeyFrame" KeyTime="00:00:00.9" Value="1">
                        <EasingDoubleKeyFrame.EasingFunction>
                            <CubicEase />
                        </EasingDoubleKeyFrame.EasingFunction>
                    </EasingDoubleKeyFrame>
                </DoubleAnimationUsingKeyFrames>
            </Storyboard>
        </Grid.Resources>
        <Grid RenderTransformOrigin=".5,.5">
            <Grid.RenderTransform>
                <ScaleTransform x:Name="scaleTransform" ScaleX="1" ScaleY="1" />
            </Grid.RenderTransform>
            <Grid.Projection>
                <PlaneProjection x:Name="Rotator" CenterOfRotationX="0.5" />
            </Grid.Projection>
            <Image x:Name="image" RenderTransformOrigin="0.5,0.5" Cursor="Hand" Source="{Binding}"/>
        </Grid>
    </Grid>
</Grid> 
"""

class ImageFlowItem(Canvas):
    def __init__(self, xaml):
        self.Content = XamlReader.Load(xaml)
        self.Children.Add(self.Content) # Add to VisualTree of Canvas
        self._yRotation = 45.0
        self._zOffset = 0.0
        self._scale = .7
        self._xAnimaton = None
        self._isAnimating = False
        self._x = 0
        self._duration = 0
        self._easingFunction = None
        
        ItemSelected = None # Expose Event
        
        def Animation_Completed(sender, e):
            self._isAnimating = False
            
        def imageElement_MouseLeftButtonUp(sender, e):
            if self.ItemSelected != None:
                self.ItemSelected(None, self.Content)            
        
        if self.Content.Animation != None:
            self._xAnimation = DoubleAnimation()
            self.Content.Animation.Children.Add(self._xAnimation)
            Storyboard.SetTarget(self._xAnimation, self.Content)
            Storyboard.SetTargetProperty(self._xAnimation, PropertyPath("(Canvas.Left)"))
            
        self.Content.Animation.Completed += Animation_Completed
        self.Content.Rotator.RotationY = self._yRotation
        self.Content.Rotator.LocalOffsetZ = self._zOffset
        
        if self.Content.image != None:
            self.Content.image.MouseLeftButtonUp += imageElement_MouseLeftButtonUp

    def get_YRotation(self):
        return self._yRotation
    def set_YRotation(self, value):
        self._yRotation = value
        self.Content.Rotator.RotationY = value
    YRotation = property(get_YRotation, set_YRotation)
    
    def get_ZOffset(self):
        return self._zOffset
    def set_ZOffset(self, value):
        self._zOffset = value
        self.Content.Rotator.LocalOffsetZ = value
    ZOffset = property(get_ZOffset, set_ZOffset)
    
    def get_Scale(self):
        return self._scale
    def set_Scale(self, value):
        self._scale = value
        if self.Content.scaleTransform != None:
            self.Content.scaleTransform.ScaleX = self._scale
            self.Content.scaleTransform.ScaleY = self._scale
    Scale = property(get_Scale, set_Scale)    
    
    def get_X(self):
        return self._x
    def set_X(self, value):
        self._x = value
        Canvas.SetLeft(self, self._x)
    X = property(get_X, set_X)
        
    def SetValues(self, x, zIndex, r, z, s, d, ease):
        if not self._isAnimating and Canvas.GetLeft(self) != x:
            Canvas.SetLeft(self, self._x)
            
        self.Content.rotationKeyFrame.Value = r
        self.Content.offestZKeyFrame.Value = z
        self.Content.scaleYKeyFrame.Value = s
        self.Content.scaleXKeyFrame.Value = s
        
        self._xAnimation.To = x
        if self._duration != d:
            self._duration = d
            self.Content.rotationKeyFrame.KeyTime = KeyTime.FromTimeSpan(d.TimeSpan)
            self.Content.offestZKeyFrame.KeyTime = KeyTime.FromTimeSpan(d.TimeSpan)
            self.Content.scaleYKeyFrame.KeyTime = KeyTime.FromTimeSpan(d.TimeSpan)
            self.Content.scaleXKeyFrame.KeyTime = KeyTime.FromTimeSpan(d.TimeSpan)
            self._xAnimation.Duration = d
        if self._easingFunction != ease:
            self._easingFunction = ease
            self.Content.rotationKeyFrame.EasingFunction = ease
            self.Content.offestZKeyFrame.EasingFunction = ease
            self.Content.scaleYKeyFrame.EasingFunction = ease
            self.Content.scaleXKeyFrame.EasingFunction = ease
            self._xAnimation.EasingFunction = ease
        self._isAnimating = True
        self.Content.Animation.Begin()
        Canvas.SetZIndex(self, zIndex)
        self._x = x
            
class Imageflow(ItemsControl):
    def __init__(self, xaml, imageflowItemXaml):
        self._imageflowItemXaml = imageflowItemXaml
        self._EasingFunction = CubicEase()
        self._items = List[ImageFlowItem]()
        self._objectToItemContainer = Dictionary[object, ImageFlowItem]()
        self._duration = Duration(TimeSpan.FromMilliseconds(600))
        self._selectedIndex = 0
        self.Content = XamlReader.Load(xaml)
        self._k = 140 # SpaceBetweenSelectedItemAndItems
        self._l = 40 # SpaceBetweenItems
        self._r = 50 # RotationAngle
        self._z = 0 # ZDistance
        self._s = 0.6 # Scale
        
        SelectionChanged = None # Expose Event
        
    def get_SelectedIndex(self):
        return self._selectedIndex
    def set_SelectedIndex(self, value):
        self.IndexSelected(value, False, False)
    SelectedIndex = property(get_SelectedIndex, set_SelectedIndex)
    
    def IndexSelected(self, index, mouseclick):
        self.IndexSelected(index, mouseclick, False)
        
    def IndexSelected(self, index, mouseclick, isLayoutChildren):
        if self._items.Count > 0:
            self._selectedIndex = index
            self.LayoutChildren()
            self.SelectionChanged(None, None)
    
    def GetContainerForItemOverride(self):
        return ImageFlowItem(self._imageflowItemXaml)

    def PrepareContainerForItemOverride(self, element, item):
        def item_ItemSelected(sender, e):
            global _items
            item = e.Parent
            if item == None:
                return 
            index = self._items.IndexOf(item)
            if index == self.SelectedIndex:
                Application.Current.Host.Content.IsFullScreen = not Application.Current.Host.Content.IsFullScreen
                me.Width = Application.Current.Host.Content.ActualWidth
                me.Height = Application.Current.Host.Content.ActualHeight
                me.LayoutRoot.Height = Application.Current.Host.Content.ActualHeight
                me.LayoutRoot.Width = Application.Current.Host.Content.ActualWidth
                me.imageflowContainer.Visibility = Visibility.Collapsed
                me.image.Source = BitmapImage(Uri(images[index], UriKind.Absolute))
                me.image.Visibility = Visibility.Visible
            if index >= 0:
                 self.IndexSelected(index, None, False)
                
        def item_SizeChanged(sender, e):
            item = sender
            index = self._items.IndexOf(item)
            self.LayoutChild(item, index)                
                
        item2 = element
        if item2 != item:
            self._objectToItemContainer[item] = item2
        if not self._items.Contains(item2):
            self._items.Add(item2)
            item2.ItemSelected = item_ItemSelected
            item2.SizeChanged += item_SizeChanged
        if self._items.Count == 1:
            self.IndexSelected(0, False, False)
            
    def ClearContainerForItemOverride(self, element, item):
        item2 = element
        if item2 != item:
            self._objectToItemContainer.Remove(item)
        self._items.Remove(item2)            

    def LayoutChildren(self):
        for i in range( 0, self._items.Count):
            self.LayoutChild(self._items[i], i)
            
    def LayoutChild(self, item, index):
        width = self.ActualWidth
        
        m = width / 2
        b = index - self.SelectedIndex
        
        mu = 0
        if b < 0:
            mu = -1
        elif b > 0:
            mu = 1
            
        x = (m + (b * self._l + (self._k * mu))) - (item.Content.ActualWidth / 2)
        
        if mu == 0:
            s = 1.0
        else:
            s = self._s
        
        zindex = self._items.Count - Math.Abs(b)
        
        item.SetValues(x, zindex, self._r * mu, self._z * Math.Abs(mu), s, self._duration, self._EasingFunction)
            
    def ArrangeOverride(self, finalSize):
        height = self.ActualHeight 
        width = self.ActualWidth
        
        m = width / 2
        
        for i in range( 0, self._items.Count):
            self._items[i].Content.Height = height
            item = self._items[i]
            b = i - self.SelectedIndex
            
            mu = 0
            if b < 0:
                mu = -1
            elif b > 0:
                mu = 1
                
            x = (m + (b * self._l + (self._k * mu))) - (width / 2)
            
            if mu == 0:
                s = 1.0
            else:
                s = self._s
            
            zindex = self._items.Count - Math.Abs(b)
            
            item.SetValues(x, zindex, self._r * mu, self._z * Math.Abs(mu), s, self._duration, self._EasingFunction)
            
        return super(ItemsControl, self).ArrangeOverride(finalSize) # equivalent to base.ArrangeOverride(finalSize))
        
    
def ImageflowItemLoaded(sender, e):
    global _imageflowItem
    _imageflowItem = e.Result
    LoadImageflow()
    
def ImageflowLoaded(sender, e):
    global _imageflow
    _imageflow = e.Result
    Main()

def ImageflowItemLoaded2():
    global _imageflowItem
    _imageflowItem = _imageflowItem_xaml_str
    LoadImageflow2()
    
def ImageflowLoaded2():
    global _imageflow
    _imageflow = _imageflow_xaml_str
    Main()
    
    
def BrowserHost_Resize(s, e):
    me.Width = Application.Current.Host.Content.ActualWidth
    me.Height = Application.Current.Host.Content.ActualHeight
    me.LayoutRoot.Height = Application.Current.Host.Content.ActualHeight
    me.LayoutRoot.Width = Application.Current.Host.Content.ActualWidth
    me.image.Visibility = Visibility.Collapsed
    me.imageflowContainer.Visibility = Visibility.Visible    

def LoadImageflow():
    client = WebClient()
    client.DownloadStringCompleted += ImageflowLoaded
    client.DownloadStringAsync(Uri("../samples/imageflow/ImageFlowIC.xaml", UriKind.Relative))

def LoadImageflowItem():
    client = WebClient()
    client.DownloadStringCompleted += ImageflowItemLoaded
    client.DownloadStringAsync(Uri("../samples/imageflow/ImageFlowItem.xaml", UriKind.Relative))

def LoadImageflow2():
    ImageflowLoaded2()

def LoadImageflowItem2():
    ImageflowItemLoaded2()

    
def UpdateSliderPosition(s, e):
    me.slider.Value = c.SelectedIndex    

def Main():
	global c
	className = HtmlPage.Window.Invoke("GetClassName")  

	imgs = document.GetElementsByTagName("img")
	for i in range(0, imgs.Count):
		if imgs[i].className == className:
			src = imgs[i].src
			images.Add(src)

	c = Imageflow(_imageflow, _imageflowItem)
	me.imageflowContainer.Children.Add(c)
	c.ItemsSource = images; # triggers binding

	c.SelectionChanged = UpdateSliderPosition 

	me.loadingControl.Visibility = Visibility.Collapsed
	me.slider.Maximum = images.Count - 1;
	me.InvalidateArrange()


def sliderValueChanged(sender, e):
    c.SelectedIndex = me.slider.Value
    me.slider.Value = Math.Round(me.slider.Value)

me.slider.ValueChanged += sliderValueChanged
Application.Current.Host.Content.Resized += BrowserHost_Resize

#LoadImageflowItem()
LoadImageflowItem2()


