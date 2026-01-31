from photon import Photon
from photon import Theme, Colors

from .core import Config
from .pages import (
    Overlay,
    
    ServerList
)

app = Photon(
    screenX = Config.screenX,
    screenY = Config.screenY,
    root = Overlay.Overlay,
    theme = Theme(
        primary = Colors.BLUE,
        success = Colors.GREEN,
        warning = Colors.YELLOW,
        error = Colors.RED
    )
)

PAGES = [
    ServerList.ServerList
]

for page in PAGES:
    app.register_page(page(app))
    
app.open("ServerList")

app.run()