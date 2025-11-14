from typing import Dict, List

app.background = rgb(255,255,255)

class Menu(Rect):
    def __init__(self, *args, parent = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        if self.parent:
            if type(self.parent) != Menu:
                raise TypeError(f"parent must be of type Menu, not {self.parent.__class__.__name__}")
            else:
                self.centerX = (parent.centerX - self.width/2) + self.centerX
                self.centerY = parent.top + self.centerY
            
    
    class Button(Rect):
        def __init__(self, parent, *args, 
                     textValue: str = "", textFill = rgb(0,0,0), textSize: int|float=12.0, textFont: str = "arial", textOpacity: int|float = 100,
                     textIsBold: bool = False, textIsItalic: bool = False, textIsVisible: bool = True,
                     debug: bool = False, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent  = parent
            if type(self.parent) != Menu:
                raise TypeError(f"parent must be of type Menu, not {self.parent.__class__.__name__}")
            
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
            
        def addEventListener(self, x, y, onclick) -> None:
            if callable(onclick) == False:
                raise TypeError(f"onclick should be a function, not {onclick.__class__.__name__}")
            
            if self.contains(x, y):
                onclick()
    
    class Title(Label):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent = parent
            
            self.centerX = parent.centerX + self.centerX
            self.centerY = parent.top + self.centerY

class Core:
    def __init__(self, startingTemp, startingPsi):
        self.startingTemp = startingTemp
        self.startingPsi  = startingPsi
    
    class Laser:
        def __init__(self, parent, level=2):
            self.parent = parent
            self.level = level
        
        class LaserControlButton(Menu.Button):
            def __init__(self, parent, *args, level=None, **kwargs):
                super().__init__(*args, **kwargs)
                self.parent = parent
                
                self.level = level
                if type(self.level) != int:
                    raise TypeError(f"type of level should be int, not {self.level.__class__.__name__}")

            def setParentLevel(self) -> None:
                self.parent.level = self.level

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
    0
)

#### Sprite
coreInner = Circle(
    325, 100,
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
coreHover = Circle(
    coreInner.centerX, coreInner.centerY,
    coreOuter.radius,
    opacity=2,
    visible=False
)

Sprite_Core = Group( coreInner, coreOuter, coreOuterRim, coreHover )

CoreMonitoring = Group( Sprite_Core )

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
    "Laser 2",
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

Panels = Group( LCP )

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

#******************#

# Defaults

nav_toggleControlRoom()

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

def onMouseMove(x, y):
    if Sprite_Core.contains(x, y):
        coreHover.visible = True
    else:
        coreHover.visible = False
