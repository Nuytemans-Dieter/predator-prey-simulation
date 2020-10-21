from random import randrange

from agents.Hunter import Hunter
from models.Model import Model


class HunterModel(Model):

    max_birth_rate = 100
    max_age = 20

    def __init__(self, environment):
        super().__init__(environment)
        print('Hunter model')

    def create_agent(self):
        location = (
            randrange(0, self.environment.size_x),
            randrange(0, self.environment.size_y)
        )
        max_age = randrange(0, 51)
        energy_to_reproduce = randrange(0, 101)
        energy_per_prey_eaten = randrange(0, 31)
        hunter = Hunter(
            self.environment,
            0,
            location,
            max_age,
            energy_to_reproduce,
            energy_per_prey_eaten
        )
        self.agents.append( hunter )
