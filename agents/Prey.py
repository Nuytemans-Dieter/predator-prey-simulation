from random import randrange

from agents.Agent import Agent


class Prey(Agent):

    def __init__(self, environment, location, max_age, birth_rate):
        super().__init__(environment, location, max_age)
        self.birth_rate = birth_rate

    def move(self):
        # Do a random move
        move = self.get_random_move()
        self.location = ( self.location[0] + move[0],
                          self.location[1] + move[1] )

        # Check reproduction -> spawn new
        chance = randrange(0, 101)
        if chance <= self.birth_rate:
            self.environment.spawn_prey()
            self.environment.preys_born += 1

        # Check max age -> die
        if self.age >= self.max_age:
            self.environment.kill_prey( self )
            self.environment.prey_deaths_by_age += 1
