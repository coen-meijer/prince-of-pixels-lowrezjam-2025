import copy

import pygame
from code import boolfield
from code.boolfield import BoolField

import os
# preconditions: state buttons space

MASK_FOLDER = "masks"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
    sprite_sheet = pygame.image.load(sprite_sheet_file).convert_alpha()
    record["opaque"] = boolfield.opaque(sprite_sheet)
    frames = []
    sheet_horizontal, sheet_vertical = sprite_sheet.get_size()
    pos_x, pos_y = 0, 0

    sprite_size = find_frame_size(sprite_sheet, record)

    sprite_horizontal, sprite_vertical = sprite_size

    more_frames = True

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
        raise ValueError(f"The number of corners registered is {len(corners)}, shoule be 1")
    corner = corners[0]
    frame_size = (corner[0] + lower_right_corner_mask.size()[0], corner[1] + lower_right_corner_mask.size()[1])
    info["frame_size"] = frame_size
    return frame_size


def mirror_state(state):
    if isinstance(state, str):
        if state == "facing_left":
            return "facing_right"
        elif state == "facing_right":
            return "facing_left"
        else:
            raise ValueError(f"cant mirror state'{state}'")
    raise ValueError(f"{state} is not a string, and I can't handle that yet.")



CONTROLLER_LAYOUT = [
    "       ",
    "  u  b ",
    " l r   ",
    "  d  a ",
    "       "
]

def read_controller():
    pass


def strings2array(strings):
    return np.array([list(string) for string in strings], dtype="U1")

