import pygame
import pygame.gfxdraw
from pygame import surface

import code.animation
from code.animation import Animation

RESOLUTION = (64, 64)
COLOR = (127, 127, 127)
BLACK = (0, 0, 0)

ANIMATION_FOLDER =  "animaties"

#TURN = ANIMATION_FOLDER + "/lowrez-short-turn-step.png"
TURN = ANIMATION_FOLDER + "/turn(2).png"
WALK = ANIMATION_FOLDER + "/lowrez-short-walk(2).png"
STAND = ANIMATION_FOLDER + "/stand.png"

ANIMAION_STATE_MACHINE = {
    "states" : ["standing", "facing_left", "facing_right"],
    "first_state": "facing_right",
    "animations": [
        {
            "name": "standing_facing_right",
            "start_state": "facing_right",
            "buttons": set(),
            "end_state": "facing_right",
            "sprite_sheet": STAND,
            "frame_size": (8, 8),
            "frame_count": 1,
            "mirrored": False
        },
        {
            "name": "standing_facing_left",
            "start_state": "facing_left",
            "buttons": set(),
            "end_state": "facing_left",
            "sprite_sheet": STAND,
            "frame_size": (8, 8),
            "frame_count": 1,
            "mirrored": True
        },
        {
            "name": "turn_right",
            "start_state": "facing_left",
            "buttons": {"right"},
            "end_state": "facing_right",
            "sprite_sheet": TURN,
            "frame_size": (8,8),
            "frame_count": 4,
            "mirrored": True
        },
        {
            "name": "turn_left",
            "start_state": "facing_right",
            "buttons": {"left"},
            "end_state": "facing_left",
            "sprite_sheet": TURN,
            "frame_size": (8,8),
            "frame_count": 4,
            "mirrored": False
        },
        {
            "name": "step_right",
            "start_state": "facing_right",
            "buttons": {"right"},
            "end_state": "facing_right",
            "sprite_sheet": WALK,
            "frame_size": (8, 8),
            "frame_count": 4,
            "mirrored": False
        },
        {
            "name": "step_left",
            "start_state": "facing_left",
            "buttons": {"left"},
            "end_state": "facing_left",
            "sprite_sheet": WALK,
            "frame_size": (8, 8),
            "frame_count": 4,
            "mirrored": True
        },
    ]
}

class PofP:

    def __init__(self):
        self.canvas = pygame.Surface(RESOLUTION)
        self.canvas.fill(COLOR)
        self.pos_x = 32 - 4
        self.pos_y = 32 - 2
#        self.up_pressed = False
#        self.down_pressed = False
#        self.left_pressed = False
#        self.right_pressed = False
        self.buttons_pressed = set()
        self.state = ANIMAION_STATE_MACHINE["first_state"]
        self.choose_next_animation = True

        self.animations = []
        for animation_info in ANIMAION_STATE_MACHINE["animations"]:
            self.animations.append(Animation(animation_info))
        self.currend_animation_player = self.animations[0].get_frame_iterator()

    def frame(self, input):
        for event in input:
            print("event:", event)
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                key_down = (event.type == pygame.KEYDOWN)
                print(key_down, event.key)
                if event.key == pygame.K_LEFT:
                    if key_down:
                        self.buttons_pressed.add("left")
                    else:
                        self.buttons_pressed.remove("left")
                elif event.key == pygame.K_RIGHT:
                    if key_down:
                        self.buttons_pressed.add("right")
                    else:
                        self.buttons_pressed.remove("right")

        print(self.buttons_pressed)

        if self.choose_next_animation:
            print("new animation starts!")
            state = self.currend_animation_player.animation.end_state
            print("state:", state, ", buttons:", self.buttons_pressed)
            for animation in self.animations:
                print("concidering '", animation.name, "', state_needed:", state )
                if state == animation.start_state:   # check state
                    print("state checks out, buttons pressed:", self.buttons_pressed )
                    if self.buttons_pressed == animation.buttons:
                        print("chosen:", animation.name)
                        self.currend_animation_player = animation.get_frame_iterator()
            print(self.currend_animation_player.animation.name)

 #       print(self.currend_animation_player.animation.name,
 #             self.currend_animation_player.frame_index,
 #             self.currend_animation_player.animation.frame_count)

        frame, self.choose_next_animation = self.currend_animation_player.get_frame()

        self.canvas.fill(COLOR)
        self.canvas.blit(frame, (self.pos_x, self.pos_y))


        return self.canvas
