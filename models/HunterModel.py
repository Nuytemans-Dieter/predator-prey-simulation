from random import randrange

from agents.Hunter import Hunter
from models.Model import Model


class HunterModel(Model):

    def __init__(self, environment, config):
        super().__init__(environment, config)
        self.max_birth_rate = 100
        self.max_age = 50

    def create_agent(self):
        self.total = self.total + 1
        name = "hunter " + str(self.total)

        location = (
            randrange(0, self.environment.size_x),
            randrange(0, self.environment.size_y)
        )
        # Read configuration parameters.
        max_age = self.config['max_age_hunter']
        starting_energy = self.config['starting_energy']
        energy_to_reproduce = self.config['energy_to_reproduce']
        energy_per_prey_eaten = self.config['energy_per_prey_eaten']

        # Randomize parameters.
        # max_age = randrange(0, 51)
        # starting_energy = 0
        # energy_to_reproduce = randrange(0, 101)
        # energy_per_prey_eaten = randrange(0, 31)

        hunter = Hunter(
            self.environment,
            starting_energy,
            location,
            max_age,
            energy_to_reproduce,
            energy_per_prey_eaten,
            name
        )
        self.agents.append( hunter )
