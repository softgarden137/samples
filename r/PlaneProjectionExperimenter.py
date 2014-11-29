#
# PlaneProjectionExperimenter
#
from System import Math
from System.Windows import * # for ToString()
#from System.Windows.Controls import *
#from System.Windows.Controls.Primitives import *
#from System.Windows.Input import *

initialized = False

def OnMainPageLayoutUpdated(sender, e):
    global initialized
    if (initialized == False):
        me.thumbTranslate.X = me.projectedElement.ActualWidth / 2
        me.thumbTranslate.Y = me.projectedElement.ActualHeight / 2
        initialized = True

def OnThumbDragDelta(sender, args):
    me.thumbTranslate.X += args.HorizontalChange
    me.thumbTranslate.Y += args.VerticalChange

    me.planeProjection.CenterOfRotationX = me.thumbTranslate.X / me.projectedElement.ActualWidth
    me.planeProjection.CenterOfRotationY = me.thumbTranslate.Y / me.projectedElement.ActualHeight

    me.xCenterText.Text = me.planeProjection.CenterOfRotationX.ToString("F3")
    me.yCenterText.Text = me.planeProjection.CenterOfRotationY.ToString("F3")

def OnMouseWheel(sender, args):
    me.planeProjection.CenterOfRotationZ += args.Delta / 12.0
    me.thumbScale.ScaleX = me.thumbScale.ScaleY = Math.Pow(2, me.planeProjection.CenterOfRotationZ / 100)
    me.zCenterText.Text = me.planeProjection.CenterOfRotationZ.ToString("F1")

class App:
    def __init__(self):
        #me.LayoutUpdated += OnMainPageLayoutUpdated
        #me.Loaded += OnMainPageLayoutUpdated # NG
        me.thumb.DragDelta += OnThumbDragDelta
        me.MouseWheel += OnMouseWheel

        me.rotationXSlider.ValueChanged += self.OnXSliderChanged
        me.rotationYSlider.ValueChanged += self.OnYSliderChanged
        me.rotationZSlider.ValueChanged += self.OnZSliderChanged

        #OnMainPageLayoutUpdated()
        me.thumbTranslate.X = me.projectedElement.ActualWidth / 2
        me.thumbTranslate.Y = me.projectedElement.ActualHeight / 2
        initialized = True

    def OnXSliderChanged(self, sender, args):
        me.RotaionX_TB.Text = me.rotationXSlider.Value.ToString("F")

    def OnYSliderChanged(self, sender, args):
        me.RotaionY_TB.Text = me.rotationYSlider.Value.ToString("F")

    def OnZSliderChanged(self, sender, args):
        me.RotaionZ_TB.Text = me.rotationZSlider.Value.ToString("F")

App()