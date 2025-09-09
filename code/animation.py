import copy

import pygame
from code import boolfield
from code.boolfield import BoolField

import os
# preconditions: state buttons space

MASK_FOLDER = "masks"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



# OPAQUE_WHITE = (255, 255, 255, 255)
# OPAQUE_BLACK = (0, 0, 0, 255)
# TRANSPARENT = (0, 0, 0, 0)

class AnimationPlayer:

    def __init__(self, animation):
        self.animation = animation
        self.frame_index = 0
        self.mirrored = animation.mirrored

    def get_frame(self):
        #print("frame", self.frame_index, "of", self.animation.frame_count)
        frame = self.animation.sprites[self.frame_index]
        self.frame_index += 1
        if self.mirrored:
            frame = pygame.transform.flip(frame, flip_x=True, flip_y=False)
        return frame, self.frame_index >= self.animation.frame_count

class Animation:

    def __init__(self, record, sprites=None):
        self.name= record["name"]
        self.start_state = record["start_state"]
        self.buttons = record["buttons"]
        self.end_state= record["end_state"]
        self.name= record["name"]
        self.mirrored = False    #  record["mirrored"]
        self.frame_count =record["frame_count"]

        if sprites is None:
            self.sprites = sprites_from_sheet(record["sprite_sheet"],
                                              record["frame_size"],
                                              record["frame_count"])
        else:
            self.sprites = sprites

    def get_frame_iterator(self):
        return AnimationPlayer(self)

    def mirror(self):
        result = copy.copy(self)
        result.name = self.name + "-mirrored"
        result.start_state = mirror_state(self.start_state)
        result.end_state = mirror_state(self.end_state)
        result.mirrored = not self.mirrored
        result.buttons = mirror_buttons(self.buttons)
        return result


def mirror_state(state):
    if isinstance(state, str):
        if state == "facing_left":
            return "facing_right"
        elif state == "facing_right":
            return "facing_left"
        else:
            raise ValueError(f"can't mirror state'{state}'")
    raise ValueError(f"{state} is not a string, and I can't handle that yet.")


def mirror_buttons(buttons):
    result = set()
    for button in buttons:
        if button == "left":
            result.add("right")
        elif button == "right":
            result.add("left")
        else:
            result.add(button)
    return result

class SpriteSheetCutter:

    def __init__(self, sheet, frame_size, start_frame=0):
        self.sheet = sheet
        self.frame_size = framesize


def sprites_from_sheet(sprite_sheet_file, sprite_size, frame_count):
    sprite_sheet = pygame.image.load(sprite_sheet_file).convert_alpha()
    frames = []
    sheet_horizontal, sheet_vertical = sprite_sheet.get_size()
    sprite_horizontal, sprite_vertical = sprite_size
    pos_x, pos_y = 0, 0
    for i in range(frame_count):
        rect = pygame.Rect((pos_y, pos_x), sprite_size)
        # print("trying to cut out frame: ", sprite_sheet_file, rect)
        frame = sprite_sheet.subsurface(rect)
        frames.append(frame.copy())

        pos_x += sprite_horizontal
        if pos_x + sheet_horizontal> sheet_horizontal:
            pos_x = 0
            pos_y += sprite_vertical

    print("from file", sprite_sheet_file, "generated", len(frames))
    return frames


def animation_from_annotated_sheet(sprite_sheet_file, record={}):
    print(f"reading sheet ======= {record['name']} =======")
    sprite_sheet = pygame.image.load(sprite_sheet_file).convert_alpha()
    record["opaque"] = boolfield.opaque(sprite_sheet)
    frames = []
    sheet_horizontal, sheet_vertical = sprite_sheet.get_size()
    pos_x, pos_y = 0, 0

    sprite_size = find_frame_size(sprite_sheet, record)

    sprite_horizontal, sprite_vertical = sprite_size

    try:
        buttons_pressed = read_controller(sprite_sheet, record)
        print("COULD find the controller!")
        record["buttons"] = buttons_pressed
    except ValueError as err:
        print("couldn't find the controller.", err)

#    more_frames = True

    while(True):
        rect = pygame.Rect((pos_x, pos_y), sprite_size)
        print("trying to cut out frame: ", sprite_sheet, rect)
        frame = sprite_sheet.subsurface(rect)
        # check if there is something in the frame
        if boolfield.opaque(frame).any():
            print(frame)
            frames.append(frame.copy())

            pos_x += sprite_horizontal
            if pos_x + sprite_horizontal> sheet_horizontal:
                pos_x = 0
                pos_y += sprite_size[1]
                if pos_y + sprite_vertical > sheet_vertical:
                    break
        else:
            break

    frames = frames[1:]   # skip start frame
    record["frame_count"] = len(frames)
    print("from file", sprite_sheet_file, "generated", len(frames))
    print("info:",record)
    return Animation(record, sprites=frames)


def load_mask(filename, file_extension=".png"):
    return boolfield.opaque(pygame.image.load(
        os.path.join(MASK_FOLDER, filename + file_extension)
    ))


def find_frame_size(sheet, info):
    lower_right_corner_mask = load_mask("lower-right-frame-corner")
    opaque = info["opaque"]
    corners = opaque.find(lower_right_corner_mask)
    if not len(corners) == 1:
        raise ValueError(f"The number of corners registered is {len(corners)}, should be 1")
    corner = corners[0]
    frame_size = (corner[0] + lower_right_corner_mask.size()[0], corner[1] + lower_right_corner_mask.size()[1])
    info["frame_size"] = frame_size
    rectangle = pygame.Rect(corner[0], frame_size[0], corner[1], frame_size[1])
    sheet.subsurface(rectangle).set_alpha(0)   # hopen dat dit werkt.
    return frame_size


CONTROLLER_LAYOUT = [
    "       ",
    "  u  b ",
    " l r   ",
    "  d  a ",
    "       "
]

BUTTON_NAMES = {
    "l": "left",
    "r": "right",
    "u": "up",
    "d": "down",
    "a": "a_button",
    "b": "b_button",
}

def read_controller(sheet, info):
    print("in read_controller!")
    layout = boolfield.is_char(CONTROLLER_LAYOUT, " ").negative()
    print(layout)
    opaque = info["opaque"]
    print("opaque:")
    print(opaque)
    positions = opaque.find(layout)
    if len(positions) != 1:
        raise ValueError(f"Found {len(positions)} poitions for the controller mask, hoped to find just 1.")

    rect = pygame.Rect(positions[0], layout.size())
    controller_patch = pygame.Surface.subsurface(sheet, rect).convert_alpha()
    controller_patch_array = pygame.surfarray.pixels3d(controller_patch)
    print(f"controller pach array is {controller_patch_array}")
        # sheet[positions[0][0]:positions[0][0] + layout.size()[0],
        #                     positions[0][1]:positions[0][1] + layout.size()[1]]
    buttons_pressed = set()


    for letter, button in BUTTON_NAMES.items():
        print("in loop")
        index = boolfield.is_char(CONTROLLER_LAYOUT, letter)
        print(f"letter: {letter}, index: {index}")
        button_pixel_color = controller_patch_array[index.array][0]  # how do i extract the pixel color?
        print(f"The color of the button {button} is {button_pixel_color}")
        if (button_pixel_color == WHITE).all():
            buttons_pressed.add(button)
        # take a look at pygame.mask - <later>  not quite what i needed
    # erase the buttons
    print(controller_patch_array)
    controller_patch.set_alpha(0)
    print(f"_____________________________buttons: {buttons_pressed}_____________________________")
    return buttons_pressed


# def rect2range(referent, offset, size):
#    return reverent[]

def find_center_marks(sprite, info):
    sprite_opaque = boolfield.opaque(sprite)
    for dimension, marker in enumerate(["horizontal-center-marker", "vertical-center-marker"]):
        pass
        #boolfield.()  # TODO: HIER VERDER




def erase_mask(surface, position, mask):
    srurface[position[0]: position]


def strings2array(strings):
    return np.array([list(string) for string in strings], dtype="U1")

