import pygame
# preconditions: state buttons space

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

    def __init__(self, record):
        self.name= record["name"]
        self.start_state = record["start_state"]
        self.buttons = record["buttons"]
        self.end_state= record["end_state"]
        self.name= record["name"]
        self.mirrored = record["mirrored"]
        self.frame_count =record["frame_count"]

        self.sprites = sprites_from_sheet(record["sprite_sheet"],
                                          record["frame_size"],
                                          record["frame_count"])

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
