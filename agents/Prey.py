from random import randrange
from agents.Agent import Agent

import numpy as np


class Prey(Agent):

    def __init__(self, environment, location, max_age, birth_rate, name):
        super().__init__(environment, location, max_age, name)
        self.birth_rate = birth_rate

    def do_action(self, action):
        """Make this agent do a specific action. 0: up, 1: down, 2: left, 3: right, 4: reproduce"""

        self.age += 1

        move = self.get_move_from_action( action )
        self.location = self.add_location( move )

    def finish_action(self):

        # Check reproduction -> spawn new
        chance = randrange(0, 101)
        if chance <= self.birth_rate:
            self.environment.spawn_prey()
            self.environment.preys_born += 1

        # Check max age -> die
        if self.age >= self.max_age:
            self.environment.kill_prey( self )
            self.environment.prey_deaths_by_age += 1

    def move(self):
        # Do a random move
        move = self.get_random_move()
        self.location = self.add_location( move )

        # Check reproduction -> spawn new
        chance = randrange(0, 101)
        if chance <= self.birth_rate:
            self.environment.spawn_prey()
            self.environment.preys_born += 1

        # Check max age -> die
        if self.age >= self.max_age:
            self.environment.kill_prey( self )
            self.environment.prey_deaths_by_age += 1

    def get_actions(self):
        return[self.add_location([0,1]), self.add_location([0,-1]), self.add_location([-1,0]), self.add_location([1,0])]

    def get_state(self):
        closestLoc = self.environment.get_nearest_hunter(self.location)
        if closestLoc == 0:
            closestX = self.environment.size_x
            closestY = self.environment.size_y
        else:
            closestX = closestLoc.location[0] - self.location[0]
            closestY = closestLoc.location[1] - self.location[1]
        return [self.age, closestX, closestY]
