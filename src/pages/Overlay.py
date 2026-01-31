import time

import photon
from photon import keymap
from photon.theme import Variants
from photon.components import *

class Overlay(photon.Page):
    def __init__(self, app):
        self.app = app
        
        self.shortcuts = {
            "f1": "(F1) Server List"   
        }
        
    def on_render(self, sc):
        return super().on_render(sc)
    
    def on_input(self, key):
        print(f"key: {keymap.get_key(key)}")