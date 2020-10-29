import pygame
from pygame import Color

class Renderer:

    FILL_SIZE = 17
    SQUARE_SIZE = 20
    BORDER = 30
    OFFSET = (SQUARE_SIZE - FILL_SIZE) / 2

    background = Color(100, 100, 100)
    empty = Color(150, 150, 150)
    hunter = Color(255, 50, 63)
    prey = Color(73, 147, 36)

    pygame.display.set_caption('PreyVSPredator')

    def __init__(self, environment):
        self.env = environment
        self.screen_size = (self.SQUARE_SIZE * (self.env.size_x) + 2*self.BORDER, self.SQUARE_SIZE * (self.env.size_y) + 2*self.BORDER )
        self.screen = pygame.display.set_mode( self.screen_size )
        pygame.init()

    def render_state(self):
        # Fill the background
        self.screen.fill( self.background )

        for x in range( self.env.size_x ):
            for y in range (self.env.size_y ):
                self.draw_square(x, y, self.empty)

        for prey in self.env.preyModel.agents:
            self.draw_square(prey.location[0], prey.location[1], self.prey)

        for hunter in self.env.hunterModel.agents:
            self.draw_square(hunter.location[0], hunter.location[1], self.hunter)

        pygame.display.update()

    def draw_square(self, x, y, color):
        square = pygame.Rect(x * self.SQUARE_SIZE + self.OFFSET + self.BORDER, y * self.SQUARE_SIZE + self.OFFSET + self.BORDER, self.FILL_SIZE, self.FILL_SIZE)
        pygame.draw.rect(self.screen, color, square)
