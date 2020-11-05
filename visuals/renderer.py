import pygame
from pygame import Color


class Renderer:

    background = Color(100, 100, 100)
    empty = Color(150, 150, 150)
    hunter = Color(255, 50, 63)
    prey = Color(73, 147, 36)

    pygame.display.set_caption('PreyVSPredator')

    def __init__(self, environment, config):
        # Read configuration parameters.
        self.fill_size = config['fill_size']
        self.square_size = config['square_size']
        self.border = config['border']
        self.offset = (self.square_size - self.fill_size) / 2

        self.env = environment
        self.screen_size = (
            self.square_size * self.env.size_x + 2 * self.border, self.square_size * self.env.size_y + 2 * self.border)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.init()

    def render_state(self):
        # Fill the background
        self.screen.fill(self.background)

        for x in range(self.env.size_x):
            for y in range(self.env.size_y):
                self.draw_square(x, y, self.empty)

        for prey in self.env.preyModel.agents:
            self.draw_square(prey.location[0], prey.location[1], self.prey)

        for hunter in self.env.hunterModel.agents:
            self.draw_square(hunter.location[0], hunter.location[1], self.hunter)

        pygame.display.update()

    def draw_square(self, x, y, color):
        square = pygame.Rect(x * self.square_size + self.offset + self.border,
                             y * self.square_size + self.offset + self.border, self.fill_size, self.fill_size)
        pygame.draw.rect(self.screen, color, square)
