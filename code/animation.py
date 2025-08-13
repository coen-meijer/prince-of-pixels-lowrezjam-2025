import pygame
# preconditions: state buttons space

MASK_FOLDER = "masks"

class AnimationPlayer:

    def __init__(self, animation):
        self.animation = animation
        self.frame_index = 0
        self.mirrored = animation.mirrored

    def get_frame(self):
        print("frame", self.frame_index, "of", self.animation.frame_count)
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
        self.mirrored = record["mirrored"]
        self.frame_count =record["frame_count"]

        if sprites is None:
            self.sprites = sprites_from_sheet(record["sprite_sheet"],
                                              record["frame_size"],
                                              record["frame_count"])
        else:
            self.sprites = sprites

    def get_frame_iterator(self):
        return AnimationPlayer(self)


def sprites_from_sheet(sprite_sheet_file, sprite_size, frame_count):
    sprite_sheet = pygame.image.load(sprite_sheet_file).convert_alpha()
    frames = []
    sheet_horizontal, sheet_vertical = sprite_sheet.get_size()
    sprite_horizontal, sprite_vertical = sprite_size
    pos_x, pos_y = 0, 0
    for i in range(frame_count):
        rect = pygame.Rect((pos_y, pos_x), sprite_size)
        print("trying to cut out frame: ", sprite_sheet_file, rect)
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
#    record["frame_size"] = find_frame_size(sprite_sheet)  # TODO: implement
    frames = []
    sprite_size = record["frame_size"]  # TODO: CHANGE TO SOMETHING REGOCNIZED
    frame_count = record["frame_count"]
    sheet_horizontal, sheet_vertical = sprite_sheet.get_size()
    sprite_horizontal, sprite_vertical = sprite_size
    pos_x, pos_y = 0, 0
    for i in range(frame_count):
        rect = pygame.Rect((pos_y, pos_x), sprite_size)
        print("trying to cut out frame: ", sprite_sheet, rect)
        frame = sprite_sheet.subsurface(rect)
        frames.append(frame.copy())

        pos_x += sprite_horizontal
        if pos_x + sheet_horizontal> sheet_horizontal:
            pos_x = 0
            pos_y += sprite_vertical

    print("from file", sprite_sheet_file, "generated", len(frames))
    return Animation(record, sprites=frames)

def load_mask(filename, file_extension=".png"):
    return pygame.image.load(os.join(MASK_FOLDER, filename + file_extension))

def find_frame_size(sheet):
    upper_left_corner_mask = load_mask("upper-left-frame-corner")
    lower_right_corner_mask = load_mask("lower-right-frame-corner")
