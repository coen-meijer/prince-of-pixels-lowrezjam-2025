import pygame
import pygame.surface as surface
import pygame.gfxdraw


RESOLUTION = (64, 64)
COLOR = (64, 64, 64)
BLACK = (0, 0, 0)

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
