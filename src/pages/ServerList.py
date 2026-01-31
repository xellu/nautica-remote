import photon
from photon.components import *

class ServerList(photon.Page):
    def __init__(self, app):
        self.app = app
        
    def on_render(self, sc):
        return super().on_render(sc)
    
    def on_input(self, key):
        return