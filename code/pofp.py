import pygame
import pygame.gfxdraw

RESOLUTION = (64, 64)
COLOR = (64, 64, 64)
BLACK = (0, 0, 0)

ANIMAION_STATE_MACHINE = {
    "states" = ["standing", "facing_left", "facing_right"],
    "animations" = [
        {
            "name": "turn_right",
            "start_state": "facing_left",
            "button": ["right"]
            "end_state": "facing_right",
            "animation_sheet": "turning.png",
            "framesize": (8,8),
            "mirrored": False
        },
        {
            "name": "turn_left",
            "start_state": "facing_right",
            "button": ["left"]
            "end_state": "facing_left",
            "animation_sheet": "turning.png",
            "framesize": (8,8),
            "mirrored": True
        },
        {
            "name": "step_right",
            "start_state": "facing_right",
            "button": ["right"]
            "end_state": "facing_right",
            "animation_sheet": "step.png",
            "framesize": (8, 8),
            "mirrored": False
        },
        {
            "name": "step_left",
            "start_state": "facing_left",
            "button": ["left"]
            "end_state": "facing_left",
            "animation_sheet": "step.png",
            "framesize": (8, 8),
            "mirrored": True
        },
        {
            "name": "standing_facing_left",
            "start_state": "facing_left",
            "button": []
            "end_state": "facing_left",
            "animation_sheet": "stand.png",
            "framesize": (8, 8),
            "mirrored": False
        },
        {
            "name": "standing_facing_right",
            "start_state": "facing_right",
            "button": []
            "end_state": "facing_right",
            "animation_sheet": "stand.png",
            "framesize": (8, 8),
            "mirrored": False
        },
    ]
}

class PofP:

    def __init__(self):
        self.canvas = pygame.Surface(RESOLUTION)
#        print("1", self.canvas)
        self.canvas.fill(COLOR)
        self.pos_x = 32
        self.pos_y = 32
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False


    def frame(self, input):
        for event in input:
            print("event:", event)
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                key_down = (event.type == pygame.KEYDOWN)
                print(key_down, event.key)
                if event.key == pygame.K_LEFT:
                    self.left_pressed = key_down
                elif event.key == pygame.K_RIGHT:
                    self.right_pressed = key_down
                elif event.key == pygame.K_UP:
                    self.up_pressed = key_down
                elif event.key == pygame.K_DOWN:
                    self.down_pressed = key_down

        if self.left_pressed:
            self.pos_x = (self.pos_x - 1) % RESOLUTION[0]
        if self.right_pressed:
            self.pos_x = (self.pos_x + 1) % RESOLUTION[0]
        if self.up_pressed:
            self.pos_y = (self.pos_y - 1) % RESOLUTION[1]
        if self.down_pressed:
            self.pos_y = (self.pos_y + 1) % RESOLUTION[1]



        pygame.gfxdraw.pixel(self.canvas, self.pos_x, self.pos_y, BLACK)
#        print("3", self.canvas)
        return self.canvas
        # should return a pygame surface with dimensions 64 x 64
