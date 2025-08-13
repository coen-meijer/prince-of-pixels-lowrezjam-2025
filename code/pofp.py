import pygame
import pygame.gfxdraw
from pygame import surface

import code.animation
from code.animation import animation_from_annotated_sheet
from code.animation import Animation
from code.animation_state_machine import ANIMAION_STATE_MACHINE

RESOLUTION = (64, 64)
COLOR = (127, 127, 127)
BLACK = (0, 0, 0)

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
            # self.animations.append(Animation(animation_info))
            self.animations.append(animation_from_annotated_sheet(
                animation_info["sprite_sheet"], record=animation_info))
        self.currend_animation_player = self.animations[0].get_frame_iterator()

    def frame(self, input):
        for event in input:
            #print("event:", event)
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                key_down = (event.type == pygame.KEYDOWN)
                # print(key_down, event.key)
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

        #print(self.buttons_pressed)

        if self.choose_next_animation:
            #print("new animation starts!")
            state = self.currend_animation_player.animation.end_state
            #print("state:", state, ", buttons:", self.buttons_pressed)
            for animation in self.animations:
                if state == animation.start_state:   # check state
                    if self.buttons_pressed == animation.buttons:
                        self.currend_animation_player = animation.get_frame_iterator()

 #       print(self.currend_animation_player.animation.name,
 #             self.currend_animation_player.frame_index,
 #             self.currend_animation_player.animation.frame_count)

        frame, self.choose_next_animation = self.currend_animation_player.get_frame()

        self.canvas.fill(COLOR)
        self.canvas.blit(frame, (self.pos_x, self.pos_y))

        return self.canvas
