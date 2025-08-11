
# preconditions: state buttons space

class AnimationPlay

class Animation:

    def __init__(self, prestate, buttons, post_state, postcondition, frames):
        self.preconditions = preconditions
        self.buttons = buttons
        self.frames = frames
        self.post_state = post_state
        self.postcondition = postcondition
        self.frames = frames

    def



def sprites(spritesheet, sprite_size, frame_count):
    pygame.image.load(spritesheet).convert_alpha()
    frames = []
    sheet_horizontal, sheet_vertical = surf.get_size()
    sprite_horizontal, sprite_vertical = sprite_size
    pos_x, pos_y = 0, 0
    for i in range (frame_count)
        rect = pygame.Rect((pos_x, pos_y), sprite_size)
        frame = image.subsurface(rect)
        frames.append(frame.copy())

        pos_x += sprite_horizontal
        if pos_x + sheet_horizontal> sheet_horizontal:
            pos_x = 0
            pos_y += sprite_vertical

    return frames
