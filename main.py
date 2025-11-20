from typing import Dict, List
from random import randrange
from math import sqrt, cbrt, pow

app.background = rgb(255,255,255)

class Menu(Rect):
    MENUS = []
    
    def __init__(self, *args, parent = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        if self.parent:
            if type(self.parent) != Menu:
                raise TypeError(f"parent must be of type Menu, not {self.parent.__class__.__name__}")
            else:
                self.centerX = (parent.centerX - self.width/2) + self.centerX
                self.centerY = parent.top + self.centerY
        
        self.data = {
            "Class": self.__class__.__name__,
            "Parent": self.parent,
            "Dimensions": {
                "TopLeft": (self.left, self.top),
                "TopRight": (self.right, self.top),
                "BottomLeft": (self.left, self.bottom),
                "BottomRight": (self.right, self.bottom),
                "Width": self.width,
                "Height": self.height,
            },
            "BackgroundFill": self.fill,
            "BorderFill": self.border,
            "BorderWidth": self.borderWidth,
            "Opacity": self.opacity,
            "IsVisible": self.visible
        }
        
        Menu.MENUS.append(self.data)
            
    class Button(Rect):
        BUTTONS = []
        
        def __init__(self, parent, *args, 
                     textValue: str = "", textFill = rgb(0,0,0), textSize: int|float=12.0, textFont: str = "arial", textOpacity: int|float = 100,
                     textIsBold: bool = False, textIsItalic: bool = False, textIsVisible: bool = True,
                     debug: bool = False, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent  = parent
            
            self.centerX = (self.parent.centerX - self.width/2) + self.centerX
            self.centerY = self.parent.top + self.centerY
            
            self.textValue = textValue
            self.textFill  = textFill
            self.textSize  = textSize
            self.textFont  = textFont
            self.textIsBold = textIsBold
            self.textIsItalic = textIsItalic
            self.textOpacity = textOpacity
            self.textIsVisible = textIsVisible
            self.text = Label(
                self.textValue,
                self.centerX, self.centerY,
                fill=self.textFill,
                size=self.textSize,
                font=self.textFont,
                bold=self.textIsBold,
                italic=self.textIsItalic,
                opacity=self.textOpacity,
                visible=self.textIsVisible
            )
            
            self.data = {
                "Class": self.__class__.__name__,
                "Parent": self.parent,
                "BoundingBox": {
                    "Dimensions": {
                        "TopLeft": (self.left, self.top),
                        "TopRight": (self.right, self.top),
                        "BottomLeft": (self.left, self.bottom),
                        "BottomRight": (self.right, self.bottom),
                        "Width": self.width,
                        "Height": self.height
                    },
                    "BackgroundFill": self.fill,
                    "BorderFill": self.border,
                    "BorderWidth": self.borderWidth,
                    "Opacity": self.opacity,
                    "IsVisible": self.visible
                },
                "Text": {
                    "Position": (self.text.centerX, self.text.centerY),
                    "Color": self.text.fill,
                    "Font": self.text.font,
                    "Size": self.text.size,
                    "IsBold": self.text.bold,
                    "IsItalic": self.text.italic,
                    "Opacity": self.text.opacity,
                    "IsVisible": self.text.visible
                }
            }
            
            Menu.Button.BUTTONS.append(self.data)
            
        def addEventListener(self, x, y, onclick) -> None:
            if callable(onclick) == False:
                raise TypeError(f"onclick should be a function, not {onclick.__class__.__name__}")
            
            if self.contains(x, y):
                onclick()
    
    class Title(Label):
        TITLES = []
        
        def __init__(self, parent, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent = parent
            
            self.centerX = parent.centerX + self.centerX
            self.centerY = parent.top + self.centerY
            
            self.data = {
                "Class": self.__class__.__name__,
                "Parent": self.parent,
                "Dimensions": {
                    "TopLeft": (self.left, self.top),
                    "TopRight": (self.right, self.top),
                    "BottomLeft": (self.left, self.bottom),
                    "BottomRight": (self.right, self.bottom),
                    "Width": self.width,
                    "Height": self.height,
                },
                "Position": (self.centerX, self.centerY),
                "Color": self.fill,
                "Font": self.font,
                "Size": self.size,
                "IsBold": self.bold,
                "IsItalic": self.italic,
                "Opacity": self.opacity,
                "IsVisible": self.visible
            }
            
            Menu.Title.TITLES.append(self.data)

class TitledMenu(Menu):
    def __init__(self, titleValue, titleXAlign, titleYAlign, *args, titleSize=15, bold=True, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.titleValue = titleValue
        self.titleXAlign = titleXAlign
        self.titleYAlign = titleYAlign
        self.titleSize = titleSize
        self.bold = bold
        self.title = Menu.Title(
            self,
            self.titleValue,
            self.titleXAlign, self.titleYAlign,
            size=self.titleSize,
            bold=self.bold
        )
        self.title.left = self.left + 6
        
        self.titleDividerLine = Line(
            self.left, self.title.bottom+7,
            self.right, self.title.bottom+7
        )

class Core:
    def __init__(self, startingTemp, startingPsi):
        self.temp = startingTemp
        self.psi  = startingPsi
        
        self.tempFlux = 0
        self.psiFlux  = 0
        
        # when a new Laser object is created, it is added to this list
        # same with pvents
        self.lasers = []
        self.pvents = []
        
        self.activeVents = 0
    
    class Laser:
        FLUXTEMP = 2.5
        FLUXPSI  = 1.5
        
        LEVELC = {
            0: rgb(235,235,235),
            1: rgb(255,248,98),
            2: rgb(255,200,90),
            3: rgb(255,140,41),
            4: rgb(255,70,70)
        }
        
        def __init__(self, parent, level=2):
            self.parent = parent
            if type(self.parent) != Core:
                raise TypeError(f"type of parent should be Core, not {self.parent.__class__.__name__}")
            
            self.level = level
            if type(self.level) != int:
                raise TypeError(f"type of level should be int, not {self.level.__class__.__name__}")
            if self.level < 1 or self.level > 5:
                raise ValueError("level should be in range 1 to 5")
            
            self.buttons = []
            self.sprite = None
            
            self.parent.lasers.append(self)
        
        class LaserControlButton(Menu.Button):
            def __init__(self, parent, *args, level=None, **kwargs):
                super().__init__(*args, **kwargs)
                self.parent = parent
                if type(self.parent) != Core.Laser:
                    raise TypeError(f"type of parent should be Core.Laser, not {self.parent.__class__.__name__}")
                
                self.level = level
                if type(self.level) != int:
                    raise TypeError(f"type of level should be int, not {self.level.__class__.__name__}")
                if self.level < 1 or self.level > 5:
                    raise ValueError("level should be in range 1 to 5")
                
                self.parent.buttons.append(self)
            
            def setParentLevel(self) -> None:
                self.parent.level = self.level
                self.parent.sprite.level = self.level
                match self.parent.sprite.level:
                    case 1:
                        self.parent.sprite.border = Core.Laser.LEVELC[0]
                        self.parent.sprite.label.fill = Core.Laser.LEVELC[0]
                        self.parent.sprite.label.value = self.level
                    case 2:
                        self.parent.sprite.border = Core.Laser.LEVELC[1]
                        self.parent.sprite.label.fill = Core.Laser.LEVELC[1]
                        self.parent.sprite.label.value = self.level
                    case 3:
                        self.parent.sprite.border = Core.Laser.LEVELC[2]
                        self.parent.sprite.label.fill = Core.Laser.LEVELC[2]
                        self.parent.sprite.label.value = self.level
                    case 4:
                        self.parent.sprite.border = Core.Laser.LEVELC[3]
                        self.parent.sprite.label.fill = Core.Laser.LEVELC[3]
                        self.parent.sprite.label.value = self.level
                    case 5:
                        self.parent.sprite.border = Core.Laser.LEVELC[4]
                        self.parent.sprite.label.fill = Core.Laser.LEVELC[4]
                        self.parent.sprite.label.value = self.level
        
        class Sprite(Rect):
            def __init__(self, parentLaser, parentMenu, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
                self.parent = parentLaser
                self.parentMenu = parentMenu
                
                self.centerX = (self.parentMenu.centerX - self.width/2) + self.centerX
                self.centerY = self.parentMenu.top + self.centerY
            
                self.fill = rgb(120,120,120)
                
                self.border = Core.Laser.LEVELC[self.parent.buttons[1].level-1] # the best dict access you've ever seen
                self.borderWidth = 3
                
                self.label = Label(
                    self.parent.level,
                    self.centerX, self.centerY,
                    size=15,
                    fill=self.border,
                    bold=True
                )
                
                if self.parent.sprite is None:
                    self.parent.sprite = self
                else:
                    raise ValueError("self.parent.sprite already exists")
    
    class PressureVent:
        FLUXPSI = 8.5
        
        TOGGLEC = {
            "on": rgb(120,230,70),
            "off": rgb(255,100,90)
        }
        
        def __init__(self, parent, on=True):
            self.parent = parent
            self.on = on
            
            if type(self.parent) != Core:
                raise TypeError(f"type of parent should be Core, not {self.parent.__class__.__name__}")
            
            self.sprite = None
            
            self.parent.pvents.append(self)
        
        class PressureVentButton(Menu.Button):
            def __init__(self, parent, *args, onclickType=True, **kwargs):
                super().__init__(*args, **kwargs)
                
                self.parent = parent
                if type(self.parent) != Core.PressureVent:
                    raise TypeError(f"type of parent should be Core.PressureVent, not {self.parent.__class__.__name__}")
                
                self.onclickType = onclickType
                
                if self.onclickType == True:
                    self.parent.parent.activeVents += 1
                
            def togglePV(self) -> None:
                if self.onclickType == True:
                    self.parent.on = self.onclickType
                    if self.parent.parent.activeVents < 4:
                        self.parent.parent.activeVents += 1
                    
                    self.parent.sprite.border = Core.PressureVent.TOGGLEC["on"]
                    for _ in range(len(self.parent.sprite.lines)):
                        self.parent.sprite.lines.children[_].fill = Core.PressureVent.TOGGLEC["on"]
                
                if self.onclickType == False and self.parent.parent.activeVents > 0:
                    self.parent.on = self.onclickType
                    self.parent.parent.activeVents -= 1
                    
                    self.parent.sprite.border = Core.PressureVent.TOGGLEC["off"]
                    for _ in range(len(self.parent.sprite.lines)):
                        self.parent.sprite.lines.children[_].fill = Core.PressureVent.TOGGLEC["off"]
        
        class Sprite(Rect):
            def __init__(self, parentVent, parentMenu, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
                self.parent = parentVent
                self.parentMenu = parentMenu
                
                self.centerX = (self.parentMenu.centerX - self.width/2) + self.centerX
                self.centerY = self.parentMenu.top + self.centerY
                
                self.fill = rgb(100,100,100)
                self.border = Core.PressureVent.TOGGLEC["on"]
                self.borderWidth = 3
                
                self.lines = Group(  )
                for _ in range(3):
                    self.lines.add(
                        Line(
                            self.left+12+self.width/4*_, self.top,
                            self.left+12+self.width/4*_, self.bottom,
                            fill=self.border,
                            lineWidth=5
                        )
                    )
                
                if self.parent.sprite is None:
                    self.parent.sprite = self
                else:
                    raise ValueError("self.parent.sprite already exists")
                
#******************#

# UI
## topbar
topbarBorderColor = rgb(80,80,80)
menu_topbar = Menu(
    0, 0,
    400, 30,
    fill=app.background,
)
topbarBorderBottom = Line(
    menu_topbar.left, menu_topbar.bottom,
    menu_topbar.right, menu_topbar.bottom,
    fill=topbarBorderColor,
    lineWidth=4
)

nav_ControlRoom = Menu.Button(
    menu_topbar,
    -153, 0,
    95, menu_topbar.height-menu_topbar.borderWidth,
    fill=app.background,
    border=rgb(235,235,235),
    borderWidth=3,
    textValue="Control Room",
    textIsBold=True
)
nav_CoolantRoom = Menu.Button(
    menu_topbar,
    -55, 0,
    95, menu_topbar.height-menu_topbar.borderWidth,
    fill=app.background,
    border=rgb(235,235,235),
    borderWidth=3,
    textValue="Coolant Room",
    textIsBold=True
)
nav_CoreMonitoring = Menu.Button(
    menu_topbar,
    48, 0,
    105, menu_topbar.height-menu_topbar.borderWidth,
    fill=app.background,
    border=rgb(235,235,235),
    borderWidth=3,
    textValue="Core Monitoring",
    textIsBold=True
)

topbarDivider1 = Line(
    nav_ControlRoom.right+2, nav_ControlRoom.top,
    nav_ControlRoom.right+2, nav_ControlRoom.bottom,
    fill=topbarBorderColor,
    lineWidth=3 
)
topbarDivider2 = Line(
    nav_CoolantRoom.right+2, nav_CoolantRoom.top,
    nav_CoolantRoom.right+2, nav_CoolantRoom.bottom,
    fill=topbarBorderColor,
    lineWidth=3 
)
topbarDivider3 = Line(
    nav_CoreMonitoring.right+2, nav_CoreMonitoring.top,
    nav_CoreMonitoring.right+2, nav_CoreMonitoring.bottom,
    fill=topbarBorderColor,
    lineWidth=3
)

## UI Functions
def nav_toggleControlRoom():
    ControlRoom.visible = True
    CoolantRoom.visible = False
    CoreMonitoring.visible = False

def nav_toggleCoolantRoom():
    ControlRoom.visible = False
    CoolantRoom.visible = True
    CoreMonitoring.visible = False

def nav_toggleCoreMonitoring():
    ControlRoom.visible = False
    CoolantRoom.visible = False
    CoreMonitoring.visible = True

#******************#

# Game Areas
## Core Monitoring
### Core
core = Core(
    1000,
    100
)

#### Core Sprite
coreInner = Circle(
    200, 90,
    20,
    fill=rgb(50,220,250),
    opacity=70
)
coreOuter = Circle(
    coreInner.centerX, coreInner.centerY,
    coreInner.radius*1.625,
    fill=gradient(coreInner.fill, rgb(80,225,235), rgb(100,235,255)),
    opacity=40
)
coreOuterRim = Circle(
    coreOuter.centerX, coreOuter.centerY,
    coreOuter.radius,
    fill=None,
    border=rgb(100,235,255),
    borderWidth=coreOuter.radius/10,
    opacity=30
)

Sprite_Core = Group( coreInner, coreOuter, coreOuterRim )

### Monitors
monitorDividerLine = Line(
    0, 155,
    400, 155
)

#### Temp Monitor
menu_TempMonitor = TitledMenu(
    "Temperature (°C)",
    0, 10,
    10, 165,
    160, 80,
    fill=rgb(170,170,170),
    border=rgb(40,40,40)
)
title_CurrentTemperatureFormat = Menu.Title(
    menu_TempMonitor,
    "C. Temp",
    0, 35,
    size=13,
    bold=True
)
title_CurrentTemperatureFormat.left = menu_TempMonitor.left + 6
title_CurrentTemperature = Menu.Title(
    menu_TempMonitor,
    f"{core.temp}",
    menu_TempMonitor.right/5, 35,
    size=13,
    bold=True
)

CurrentTemperature = Group( title_CurrentTemperatureFormat, title_CurrentTemperature )

title_TempFluxFormat = Menu.Title(
    menu_TempMonitor,
    "Temp Flux.",
    0, 60,
    size=13,
    bold=True
)
title_TempFluxFormat.left = menu_TempMonitor.left + 6
title_TempFlux = Menu.Title(
    menu_TempMonitor,
    f"{core.tempFlux}",
    menu_TempMonitor.right/5, 60,
    size=13,
    bold=True
)

TempFlux = Group( title_TempFluxFormat, title_TempFlux )

TempMonitor = Group( 
    menu_TempMonitor, menu_TempMonitor.title, menu_TempMonitor.titleDividerLine,
    CurrentTemperature,
    TempFlux
)

#### Pressure Monitor
menu_PressureMonitor = TitledMenu(
    "Pressure (PSI)",
    0, 10,
    menu_TempMonitor.left, menu_TempMonitor.bottom+10,
    menu_TempMonitor.width, menu_TempMonitor.height,
    fill=menu_TempMonitor.fill,
    border=menu_TempMonitor.border
)
title_CurrentPressureFormat = Menu.Title(
    menu_PressureMonitor,
    "C. PSI",
    0, 35,
    size=13,
    bold=True
)
title_CurrentPressureFormat.left = menu_PressureMonitor.left + 6
title_CurrentPressure = Menu.Title(
    menu_PressureMonitor,
    f"{core.psi}",
    menu_TempMonitor.right/5, 35,
    size=13,
    bold=True
)

CurrentPressure = Group( title_CurrentPressureFormat, title_CurrentPressure )

title_PressureFluxFormat = Menu.Title(
    menu_PressureMonitor,
    "PSI Flux.",
    0, 60,
    size=13,
    bold=True
)
title_PressureFluxFormat.left = menu_PressureMonitor.left + 6
title_PressureFlux = Menu.Title(
    menu_PressureMonitor,
    f"{core.psiFlux}",
    menu_PressureMonitor.right/5, 60,
    size=13,
    bold=True
)

PressureFlux = Group( title_PressureFluxFormat, title_PressureFlux )

PressureMonitor = Group( 
    menu_PressureMonitor, menu_PressureMonitor.title, menu_PressureMonitor.titleDividerLine,
    CurrentPressure,
    PressureFlux
)

CoreMonitoring = Group( Sprite_Core, monitorDividerLine, TempMonitor, PressureMonitor )

## Control Room
### Panels
#### Lasers
laser1 = Core.Laser(
    core
)

laser2 = Core.Laser(
    core
)

laser3 = Core.Laser(
    core
)

Lasers = ( laser1, laser2, laser3 )

#### Laser Control
def LCPButtonArgs() -> List:
    args = [
        55, 15
    ]
    return args

def LCPButtonKwargs(text: str = "", border = rgb(60,60,60), level: int|None = None) -> Dict:
    kwargs = {
        "fill": rgb(80,80,80),
        "border": border,
        "textValue": text,
        "textFill": border,
        "textSize": 10,
        "textIsBold": True,
        "level": level
    }
    
    if text == "Minimum":
        kwargs["textFill"] = rgb(235,235,235)
        kwargs["border"] = rgb(235,235,235)
        
    return kwargs

menu_LaserControlPanel = Menu(
    10, 40,
    215, 140,
    fill=rgb(170,170,170),
    border=rgb(40,40,40)
)

LCPnMenuFill = rgb(200,200,200)

##### LC Panel 1

menu_LCP1 = Menu(
    -70, 5,
    65, 130,
    fill=LCPnMenuFill,
    border=rgb(0,0,0),
    parent=menu_LaserControlPanel
)
LCP1_Label = Menu.Title(
    menu_LCP1,
    "Laser 1",
    0, 15,
    bold=True
)
LCP1_l1 = Core.Laser.LaserControlButton(
    laser1,
    menu_LCP1,
    0, 30,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Minimum", level=1)
)
LCP1_l2 = Core.Laser.LaserControlButton(
    laser1,
    menu_LCP1,
    0, 50,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 2", border=rgb(255,248,98), level=2)
)
LCP1_l3 = Core.Laser.LaserControlButton(
    laser1,
    menu_LCP1,
    0, 70,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 3", border=rgb(255,200,90), level=3)
)
LCP1_l4 = Core.Laser.LaserControlButton(
    laser1,
    menu_LCP1,
    0, 90,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 4", border=rgb(255,140,41), level=4)
)
LCP1_l5 = Core.Laser.LaserControlButton(
    laser1,
    menu_LCP1,
    0, 110,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Maximum", border=rgb(255,70,70), level=5)
)

LCP1 = Group(
    menu_LCP1,
    LCP1_Label,
    LCP1_l1, LCP1_l1.text,
    LCP1_l2, LCP1_l2.text,
    LCP1_l3, LCP1_l3.text,
    LCP1_l4, LCP1_l4.text,
    LCP1_l5, LCP1_l5.text
)

##### LC Panel 2

menu_LCP2 = Menu(
    0, 5,
    65, 130,
    fill=LCPnMenuFill,
    border=rgb(0,0,0),
    parent=menu_LaserControlPanel
)
LCP2_Label = Menu.Title(
    menu_LCP2,
    "Laser 2",
    0, 15,
    bold=True
)
LCP2_l1 = Core.Laser.LaserControlButton(
    laser2,
    menu_LCP2,
    0, 30,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Minimum", level=1)
)
LCP2_l2 = Core.Laser.LaserControlButton(
    laser2,
    menu_LCP2,
    0, 50,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 2", border=rgb(255,248,98), level=2)
)
LCP2_l3 = Core.Laser.LaserControlButton(
    laser2,
    menu_LCP2,
    0, 70,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 3", border=rgb(255,200,90), level=3)
)
LCP2_l4 = Core.Laser.LaserControlButton(
    laser2,
    menu_LCP2,
    0, 90,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 4", border=rgb(255,140,41), level=4)
)
LCP2_l5 = Core.Laser.LaserControlButton(
    laser2,
    menu_LCP2,
    0, 110,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Maximum", border=rgb(255,70,70), level=5)
)

LCP2 = Group( 
    menu_LCP2,
    LCP2_Label,
    LCP2_l1, LCP2_l1.text,
    LCP2_l2, LCP2_l2.text,
    LCP2_l3, LCP2_l3.text,
    LCP2_l4, LCP2_l4.text,
    LCP2_l5, LCP2_l5.text
)

##### LC Panel 3

menu_LCP3 = Menu(
    70, 5,
    65, 130,
    fill=LCPnMenuFill,
    border=rgb(0,0,0),
    parent=menu_LaserControlPanel
)
LCP3_Label = Menu.Title(
    menu_LCP3,
    "Laser 3",
    0, 15,
    bold=True
)
LCP3_l1 = Core.Laser.LaserControlButton(
    laser3,
    menu_LCP3,
    0, 30,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Minimum", level=1)
)
LCP3_l2 = Core.Laser.LaserControlButton(
    laser3,
    menu_LCP3,
    0, 50,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 2", border=rgb(255,248,98), level=2)
)
LCP3_l3 = Core.Laser.LaserControlButton(
    laser3,
    menu_LCP3,
    0, 70,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 3", border=rgb(255,200,90), level=3)
)
LCP3_l4 = Core.Laser.LaserControlButton(
    laser3,
    menu_LCP3,
    0, 90,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Level 4", border=rgb(255,140,41), level=4)
)
LCP3_l5 = Core.Laser.LaserControlButton(
    laser3,
    menu_LCP3,
    0, 110,
    *LCPButtonArgs(),
    **LCPButtonKwargs(text="Maximum", border=rgb(255,70,70), level=5)
)

LCP3 = Group(
    menu_LCP3,
    LCP3_Label,
    LCP3_l1, LCP3_l1.text,
    LCP3_l2, LCP3_l2.text,
    LCP3_l3, LCP3_l3.text,
    LCP3_l4, LCP3_l4.text,
    LCP3_l5, LCP3_l5.text
)

LCP = Group( menu_LaserControlPanel, LCP1, LCP2, LCP3 )

### Pressure Vents
pvent1 = Core.PressureVent(core)
pvent2 = Core.PressureVent(core)
pvent3 = Core.PressureVent(core)
pvent4 = Core.PressureVent(core)

menu_PressureVentPanel = Menu(
    menu_LaserControlPanel.right+10, menu_LaserControlPanel.top,
    155, menu_LaserControlPanel.height,
    fill=rgb(170,170,170),
    border=rgb(40,40,40)
)

#### PV 1
menu_PV1 = TitledMenu(
    "P. Vent 1",
    0, 8,
    -35,10,
    55,55,
    parent=menu_PressureVentPanel,
    fill=LCPnMenuFill,
    border=rgb(0,0,0),
    titleSize=10,
    bold=True
)
menu_PV1.title.centerX = menu_PV1.centerX
menu_PV1.titleDividerLine.y1 -= 3
menu_PV1.titleDividerLine.y2 -= 3

PV1_on = Core.PressureVent.PressureVentButton(
    pvent1,
    menu_PV1,
    -14, 20,
    20, 30,
    border=Core.PressureVent.TOGGLEC["on"],
    textValue="ON",
    textFill=Core.PressureVent.TOGGLEC["on"],
    textSize=10,
    textIsBold=True,
    onclickType=True
)
PV1_off = Core.PressureVent.PressureVentButton(
    pvent1,
    menu_PV1,
    12, 20,
    25, 30,
    border=Core.PressureVent.TOGGLEC["off"],
    textValue="OFF",
    textFill=Core.PressureVent.TOGGLEC["off"],
    textSize=10,
    textIsBold=True,
    onclickType=False
)

PV1 = Group(
    menu_PV1, menu_PV1.title, menu_PV1.titleDividerLine,
    PV1_on, PV1_on.text,
    PV1_off, PV1_off.text
)

#### PV 2
menu_PV2 = TitledMenu(
    "P. Vent 2",
    0, 8,
    35,10,
    55,55,
    parent=menu_PressureVentPanel,
    fill=LCPnMenuFill,
    border=rgb(0,0,0),
    titleSize=10,
    bold=True
)
menu_PV2.title.centerX = menu_PV2.centerX
menu_PV2.titleDividerLine.y1 -= 3
menu_PV2.titleDividerLine.y2 -= 3

PV2_on = Core.PressureVent.PressureVentButton(
    pvent2,
    menu_PV2,
    -14, 20,
    20, 30,
    border=Core.PressureVent.TOGGLEC["on"],
    textValue="ON",
    textFill=Core.PressureVent.TOGGLEC["on"],
    textSize=10,
    textIsBold=True,
    onclickType=True
)
PV2_off = Core.PressureVent.PressureVentButton(
    pvent2,
    menu_PV2,
    12, 20,
    25, 30,
    border=Core.PressureVent.TOGGLEC["off"],
    textValue="OFF",
    textFill=Core.PressureVent.TOGGLEC["off"],
    textSize=10,
    textIsBold=True,
    onclickType=False
)

PV2 = Group(
    menu_PV2, menu_PV2.title, menu_PV2.titleDividerLine,
    PV2_on, PV2_on.text,
    PV2_off, PV2_off.text
)

#### PV 3
menu_PV3 = TitledMenu(
    "P. Vent 3",
    0, 8,
    -35,75,
    55,55,
    parent=menu_PressureVentPanel,
    fill=LCPnMenuFill,
    border=rgb(0,0,0),
    titleSize=10,
    bold=True
)
menu_PV3.title.centerX = menu_PV3.centerX
menu_PV3.titleDividerLine.y1 -= 3
menu_PV3.titleDividerLine.y2 -= 3

PV3_on = Core.PressureVent.PressureVentButton(
    pvent3,
    menu_PV3,
    -14, 20,
    20, 30,
    border=Core.PressureVent.TOGGLEC["on"],
    textValue="ON",
    textFill=Core.PressureVent.TOGGLEC["on"],
    textSize=10,
    textIsBold=True,
    onclickType=True
)
PV3_off = Core.PressureVent.PressureVentButton(
    pvent3,
    menu_PV3,
    12, 20,
    25, 30,
    border=Core.PressureVent.TOGGLEC["off"],
    textValue="OFF",
    textFill=Core.PressureVent.TOGGLEC["off"],
    textSize=10,
    textIsBold=True,
    onclickType=False
)

PV3 = Group(
    menu_PV3, menu_PV3.title, menu_PV3.titleDividerLine,
    PV3_on, PV3_on.text,
    PV3_off, PV3_off.text
)

#### PV 4
menu_PV4 = TitledMenu(
    "P. Vent 4",
    0, 8,
    35,75,
    55,55,
    parent=menu_PressureVentPanel,
    fill=LCPnMenuFill,
    border=rgb(0,0,0),
    titleSize=10,
    bold=True
)
menu_PV4.title.centerX = menu_PV4.centerX
menu_PV4.titleDividerLine.y1 -= 3
menu_PV4.titleDividerLine.y2 -= 3

PV4_on = Core.PressureVent.PressureVentButton(
    pvent4,
    menu_PV4,
    -14, 20,
    20, 30,
    border=Core.PressureVent.TOGGLEC["on"],
    textValue="ON",
    textFill=Core.PressureVent.TOGGLEC["on"],
    textSize=10,
    textIsBold=True,
    onclickType=True
)
PV4_off = Core.PressureVent.PressureVentButton(
    pvent4,
    menu_PV4,
    12, 20,
    25, 30,
    border=Core.PressureVent.TOGGLEC["off"],
    textValue="OFF",
    textFill=Core.PressureVent.TOGGLEC["off"],
    textSize=10,
    textIsBold=True,
    onclickType=False
)

PV4 = Group(
    menu_PV4, menu_PV4.title, menu_PV4.titleDividerLine,
    PV4_on, PV4_on.text,
    PV4_off, PV4_off.text
)

PVCP = Group(
    menu_PressureVentPanel,
    PV1, PV2,
    PV3, PV4
)

Panels = Group( LCP, PVCP )

ControlRoom = Group( Panels )

## Coolant Room

notImplemented = Label(
    "! NOT IMPLEMENTED !",
    200,200,
    size=25,
    fill=rgb(255,0,0),
    bold=True
)

CoolantRoom = Group( notImplemented )

# Sprites
## Laser Sprites
menu_LaserSprites = Menu(
    10, 40,
    140, 105,
    fill=rgb(170,170,170),
    border=rgb(80,80,80),
    borderWidth=2
)

sprite_Laser1 = Core.Laser.Sprite(
    laser1,
    menu_LaserSprites,
    -45, 5,
    30, 95,
)

sprite_Laser2 = Core.Laser.Sprite(
    laser2,
    menu_LaserSprites,
    0, 5,
    30, 95,
)

sprite_Laser3 = Core.Laser.Sprite(
    laser3,
    menu_LaserSprites,
    45, 5,
    30, 95,
)

CoreMonitoring.add(
    menu_LaserSprites,
    sprite_Laser1, sprite_Laser1.label,
    sprite_Laser2, sprite_Laser2.label,
    sprite_Laser3, sprite_Laser3.label
)

## Pressure Vents
menu_PressureVents = Menu(
    250, 40,
    140, 105,
    fill=rgb(170,170,170),
    border=rgb(80,80,80),
    borderWidth=2
)
sprite_pvent1 = Core.PressureVent.Sprite(
    pvent1,
    menu_PressureVents,
    -35, 5,
    45, 45
)
sprite_pvent2 = Core.PressureVent.Sprite(
    pvent2,
    menu_PressureVents,
    35, 5,
    45, 45
)
sprite_pvent3 = Core.PressureVent.Sprite(
    pvent3,
    menu_PressureVents,
    -35, 54,
    45, 45
)
sprite_pvent4 = Core.PressureVent.Sprite(
    pvent4,
    menu_PressureVents,
    35, 54,
    45, 45
)

CoreMonitoring.add(
    menu_PressureVents,
    sprite_pvent1, sprite_pvent1.lines,
    sprite_pvent2, sprite_pvent2.lines,
    sprite_pvent3, sprite_pvent3.lines,
    sprite_pvent4, sprite_pvent4.lines
)

#******************#

# Defaults

nav_toggleCoreMonitoring()

# Event Listeners
def onMousePress(x, y):
    # topbar
    nav_ControlRoom.addEventListener(x, y, onclick=nav_toggleControlRoom)
    nav_CoolantRoom.addEventListener(x, y, onclick=nav_toggleCoolantRoom)
    nav_CoreMonitoring.addEventListener(x, y, onclick=nav_toggleCoreMonitoring)
    
    # Control Room
    ## LCP
    ### Laser 1
    LCP1_l1.addEventListener(x, y, LCP1_l1.setParentLevel)
    LCP1_l2.addEventListener(x, y, LCP1_l2.setParentLevel)
    LCP1_l3.addEventListener(x, y, LCP1_l3.setParentLevel)
    LCP1_l4.addEventListener(x, y, LCP1_l4.setParentLevel)
    LCP1_l5.addEventListener(x, y, LCP1_l5.setParentLevel)
    ### Laser 2
    LCP2_l1.addEventListener(x, y, LCP2_l1.setParentLevel)
    LCP2_l2.addEventListener(x, y, LCP2_l2.setParentLevel)
    LCP2_l3.addEventListener(x, y, LCP2_l3.setParentLevel)
    LCP2_l4.addEventListener(x, y, LCP2_l4.setParentLevel)
    LCP2_l5.addEventListener(x, y, LCP2_l5.setParentLevel)
    ### Laser 3
    LCP3_l1.addEventListener(x, y, LCP3_l1.setParentLevel)
    LCP3_l2.addEventListener(x, y, LCP3_l2.setParentLevel)
    LCP3_l3.addEventListener(x, y, LCP3_l3.setParentLevel)
    LCP3_l4.addEventListener(x, y, LCP3_l4.setParentLevel)
    LCP3_l5.addEventListener(x, y, LCP3_l5.setParentLevel)
    
    ## PV
    ### PV 1
    PV1_on.addEventListener(x, y, PV1_on.togglePV)
    PV1_off.addEventListener(x, y, PV1_off.togglePV)
    ### PV 2
    PV2_on.addEventListener(x, y, PV2_on.togglePV)
    PV2_off.addEventListener(x, y, PV2_off.togglePV)
    ### PV 3
    PV3_on.addEventListener(x, y, PV3_on.togglePV)
    PV3_off.addEventListener(x, y, PV3_off.togglePV)
    ### PV 4
    PV4_on.addEventListener(x, y, PV4_on.togglePV)
    PV4_off.addEventListener(x, y, PV4_off.togglePV)

app.stepsPerSecond = 0.75
app.totalSteps = 0

def onStep():
    # Core
    ## Temp/PSI
    core.psiFlux -= Core.PressureVent.FLUXPSI * core.activeVents + randrange(3, 6) - sqrt(core.temp)/10
    
    for laser in core.lasers:
        core.psiFlux += Core.Laser.FLUXPSI * laser.level
        core.psiFlux += (randrange(-1*laser.level, 4*laser.level)/4) * pow(cbrt(core.temp), 1.1)/1.8
        
        core.tempFlux += Core.Laser.FLUXTEMP * laser.level
        core.tempFlux += (randrange(-3*laser.level, 5*laser.level)/3) * pow(sqrt(core.temp), 1.1)/10
        core.tempFlux += pow(core.psi, 1.08)/10

    core.tempFlux = rounded(core.tempFlux)
    core.temp += core.tempFlux
    
    core.psiFlux = rounded(core.psiFlux)
    core.psi += core.psiFlux
    if core.psi < 0:
        core.psiFlux = 0
        core.psi = 0
    
    title_CurrentTemperature.value = core.temp
    if core.temp >= 35500:
        title_CurrentTemperature.fill = rgb(240,30,70)
    elif core.temp >= 26500:
        title_CurrentTemperature.fill = rgb(220,100,50)
    elif core.temp >= 17500:
        title_CurrentTemperature.fill = rgb(220,220,50)
    else:
        title_CurrentTemperature.fill = rgb(0,0,0)
    
    if core.tempFlux > 0:
        title_TempFlux.value = f"+{core.tempFlux}"
        title_TempFlux.fill = rgb(240,30,70)
    elif core.tempFlux < 0:
        title_TempFlux.value = f"{core.tempFlux}"
        title_TempFlux.fill = rgb(70,30,240)
    elif core.tempFlux == 0:
        title_TempFlux.value = f"{core.tempFlux}"
        title_TempFlux.fill = rgb(0,0,0)
    
    title_CurrentPressure.value = core.psi
    if core.psi >= 31000:
        title_CurrentPressure.fill = rgb(240,30,70)
    elif core.psi >= 21500:
        title_CurrentPressure.fill = rgb(220,100,50)
    elif core.psi >= 12000:
        title_CurrentPressure.fill = rgb(220,220,50)
    else:
        title_CurrentPressure.fill = rgb(0,0,0)
    
    if core.psiFlux > 0:
        title_PressureFlux.value = f"+{core.psiFlux}"
        title_PressureFlux.fill = rgb(240,30,70)
    elif core.psiFlux < 0:
        title_PressureFlux.value = f"{core.psiFlux}"
        title_PressureFlux.fill = rgb(70,30,240)
    elif core.psiFlux == 0:
        title_PressureFlux.value = f"{core.psiFlux}"
        title_PressureFlux.fill = rgb(0,0,0)
    
    core.tempFlux = 0
    core.psiFlux  = 0
    
    app.totalSteps += 1
