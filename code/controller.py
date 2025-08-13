import boolfield
from boolfield import BoolField

# controllerreader.py

#class controller reader

controller_layout = [
    "       ",
    "  u  b ",
    " l r   ",
    "  d  a ",
    "       "
]


def controller_pattern(layout):
    return boolfield.is_char(layout, " ").negative().transpose()

def find_controller(controller_patern, frame):
    opaque = boolfield.opaque(frame)
    return opaque.find(controller_patern)[0]

def get_buttons(boolfield, window_offset=(0,0)):
    controller_window =
    return
