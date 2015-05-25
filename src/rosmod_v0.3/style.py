import wx
import os,sys
from collections import OrderedDict

import drawable

exeName = sys.argv[0]
dirName = os.path.abspath(exeName)
head,tail = os.path.split(dirName)
editorPath=head
rootIconPath= editorPath + '/icons'
modelIconPath= rootIconPath + '/model'

activeOverlay = "YELLOW"
nodeDownOverlay = "RED"
nodeUpOverlay = "GREEN"
referenceOverlay = "BLUE"
similarOverlay = "BLACK"

def BuildStyleDict(self):
    self.styleDict = OrderedDict()
    font = OrderedDict()
    minSize = (50,50)
    padding = (10,10)
    pkgOffset = (50,50)
    msgIcon = wx.Bitmap(modelIconPath + '/msgIcon.png')
    srvIcon = wx.Bitmap(modelIconPath + '/srvIcon.png')
    tmrIcon = wx.Bitmap(modelIconPath + '/tmrIcon.png')
    pubIcon = wx.Bitmap(modelIconPath + '/pubIcon.png')
    subIcon = wx.Bitmap(modelIconPath + '/subIcon.png')
    clientIcon = wx.Bitmap(modelIconPath + '/clientIcon.png')
    serverIcon = wx.Bitmap(modelIconPath + '/serverIcon.png')
    compInstIcon = wx.Bitmap(modelIconPath + '/compInstIcon.png')
    hostIcon = wx.Bitmap(modelIconPath + '/bbb.png')
    hostInstIcon = wx.Bitmap(modelIconPath + '/bbb.png')
    '''
    STYLES USED FOR HARDWARE CONFIGURATION OBJECTS
    '''
    rhwStyle = drawable.Draw_Style(icon=None, 
                                   font={'pointSize' : 20,
                                         'color' : "black",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.SQUARE,
                                   offset = pkgOffset,
                                   placement=drawable.Text_Placement.TOP,
                                   overlay = OrderedDict() )
    HardwareStyle = drawable.Draw_Style(icon=hostIcon,
                                        font={'pointSize' : 20,
                                              'color' : "black",
                                              'prefix' : "",
                                              'weight' : wx.NORMAL}, 
                                        method=drawable.Draw_Method.ICON, 
                                        childLayout=drawable.Child_Layout.HIDDEN,
                                        minSize = minSize,
                                        placement=drawable.Text_Placement.TOP,
                                        overlay = OrderedDict() )
    '''
    STYLES USED FOR DEPLOYMENT CONFIGURATION OBJECTS
    '''
    DeploymentStyle = drawable.Draw_Style(icon=None, 
                                          font={'pointSize' : 20,
                                                'color' : "#9A3334",
                                                'prefix' : "Deployment: ",
                                                'weight' : wx.BOLD}, 
                                          method=drawable.Draw_Method.ICON, 
                                          childLayout=drawable.Child_Layout.SQUARE,
                                          offset = pkgOffset,
                                          placement=drawable.Text_Placement.TOP,
                                          overlay = OrderedDict() )
    NodeStyle = drawable.Draw_Style(icon=None,
                                    font={'pointSize' : 20,
                                          'color' : "#217C7E",
                                          'prefix' : "Node: ",
                                          'weight' : wx.BOLD}, 
                                    method=drawable.Draw_Method.ROUND_RECT, 
                                    childLayout=drawable.Child_Layout.STACK,     
                                    minSize = minSize,
                                    placement=drawable.Text_Placement.TOP,
                                    overlay = OrderedDict([('fillColor','#217C7E')]) )
    CompInstStyle = drawable.Draw_Style(icon=compInstIcon,
                                        font={'pointSize' : 20,
                                              'color' : "white",
                                              'prefix' : "",
                                              'weight' : wx.NORMAL}, 
                                        method=drawable.Draw_Method.ROUND_RECT, 
                                        childLayout=drawable.Child_Layout.STACK,
                                        minSize = minSize,
                                        placement=drawable.Text_Placement.RIGHT,
                                        overlay = OrderedDict([('fillColor','#F3EFE0')]) )
    PortInstStyle = drawable.Draw_Style(icon=None,
                                        font={'pointSize' : 20,
                                              'color' : "black",
                                              'prefix' : "",
                                              'weight' : wx.NORMAL}, 
                                        method=drawable.Draw_Method.ROUND_RECT, 
                                        childLayout=drawable.Child_Layout.HIDDEN,
                                        minSize = minSize,
                                        placement=drawable.Text_Placement.RIGHT,
                                        overlay = OrderedDict([('fillColor','#9A3334')]) )
    '''
    STYLES USED FOR SOFTWARE CONFIGURATION OBJECTS
    '''
    WrkStyle = drawable.Draw_Style(icon=None, 
                                   font={'pointSize' : 20,
                                         'color' : "black",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.STACK,                       
                                   offset = pkgOffset,
                                   placement=drawable.Text_Placement.TOP,
                                   overlay = OrderedDict() )
    PkgStyle = drawable.Draw_Style(icon=None, 
                                   font={'pointSize' : 20,
                                         'color' : "black",
                                         'prefix' : "Package: ",
                                         'weight' : wx.BOLD}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.COLUMNS,                      
                                   placement=drawable.Text_Placement.TOP,
                                   overlay = OrderedDict(),
                                   minSize = minSize,
                                   padding = (50,25),
                                   offset = pkgOffset )
    MsgStyle = drawable.Draw_Style(icon=msgIcon, 
                                   font={'pointSize' : 20,
                                         'color' : "black",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.HIDDEN,      
                                   placement=drawable.Text_Placement.TOP,
                                   minSize = minSize,
                                   overlay = OrderedDict() )
    SrvStyle = drawable.Draw_Style(icon=srvIcon,
                                   font={'pointSize' : 20,
                                         'color' : "black",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.HIDDEN,  
                                   placement=drawable.Text_Placement.TOP,
                                   minSize = minSize,
                                   overlay = OrderedDict() )
    CompStyle = drawable.Draw_Style(icon=None,
                                    font={'pointSize' : 20,
                                          'color' : "black",
                                          'prefix' : "",
                                          'weight' : wx.NORMAL}, 
                                    method=drawable.Draw_Method.ROUND_RECT, 
                                    childLayout=drawable.Child_Layout.STACK,    
                                    placement=drawable.Text_Placement.TOP,
                                    minSize = minSize,
                                    overlay = OrderedDict([('fillColor','white')]) )
    TmrStyle = drawable.Draw_Style(icon=tmrIcon,
                                   font={'pointSize' : 20,
                                         'color' : "white",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.HIDDEN,
                                   minSize = minSize,
                                   placement=drawable.Text_Placement.RIGHT,
                                   overlay = OrderedDict() )
    PubStyle = drawable.Draw_Style(icon=pubIcon,
                                   font={'pointSize' : 20,
                                         'color' : "white",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.HIDDEN,
                                   minSize = minSize,
                                   placement=drawable.Text_Placement.RIGHT,
                                   overlay = OrderedDict() )
    SubStyle = drawable.Draw_Style(icon=subIcon,
                                   font={'pointSize' : 20,
                                         'color' : "white",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.HIDDEN,
                                   minSize = minSize,
                                   placement=drawable.Text_Placement.RIGHT,
                                   overlay = OrderedDict() )
    CliStyle = drawable.Draw_Style(icon=clientIcon,
                                   font={'pointSize' : 20,
                                         'color' : "white",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.HIDDEN,
                                   minSize = minSize,
                                   placement=drawable.Text_Placement.RIGHT,
                                   overlay = OrderedDict() )
    SerStyle = drawable.Draw_Style(icon=serverIcon,
                                   font={'pointSize' : 20,
                                         'color' : "white",
                                         'prefix' : "",
                                         'weight' : wx.NORMAL}, 
                                   method=drawable.Draw_Method.ICON, 
                                   childLayout=drawable.Child_Layout.HIDDEN,
                                   minSize = minSize,
                                   placement=drawable.Text_Placement.RIGHT,
                                   overlay = OrderedDict() )

    self.styleDict["rml"] = WrkStyle

    self.styleDict["Package"] = PkgStyle
    self.styleDict["Message"] = MsgStyle
    self.styleDict["Service"] = SrvStyle
    self.styleDict["Component"] = CompStyle
    self.styleDict["Timer"] = TmrStyle
    self.styleDict["Publisher"] = PubStyle
    self.styleDict["Subscriber"] = SubStyle
    self.styleDict["Client"] = CliStyle
    self.styleDict["Server"] = SerStyle

    self.styleDict["rhw"] = rhwStyle
    self.styleDict["Hardware"] = HardwareStyle

    self.styleDict["rdp"] = DeploymentStyle
    self.styleDict["Node"] = NodeStyle
    self.styleDict["Component_Instance"] = CompInstStyle
    self.styleDict["Port_Instance"] = PortInstStyle

