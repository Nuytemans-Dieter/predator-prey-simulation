from random import randrange

from agents.Hunter import Hunter
from models.Model import Model


class HunterModel(Model):

    def __init__(self, environment):
        super().__init__(environment)
        self.max_birth_rate = 100
        self.max_age = 50

    def create_agent(self):
        location = (
            randrange(0, self.environment.size_x),
            randrange(0, self.environment.size_y)
        )
        # max_age = randrange(0, 51)
        max_age = 30
        # starting_energy = 0
        starting_energy = 10
        # energy_to_reproduce = randrange(0, 101)
        energy_to_reproduce = 100
        # energy_per_prey_eaten = randrange(0, 31)
        energy_per_prey_eaten = 30
        hunter = Hunter(
            self.environment,
            starting_energy,
            location,
            max_age,
            energy_to_reproduce,
            energy_per_prey_eaten
        )
        self.agents.append( hunter )
