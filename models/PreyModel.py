from random import randrange

from agents.Prey import Prey
from models.Model import Model


class PreyModel(Model):

    def __init__(self, environment, config):
        super().__init__(environment, config)

    def create_agent(self):
        location = (
            randrange(0, self.environment.size_x),
            randrange(0, self.environment.size_y)
        )

        # Read configuration parameters.
        max_age = self.config['max_age_prey']
        birth_rate = self.config['birth_rate_prey']

        # Randomize.
        # max_age = randrange(0, 51)
        # birth_rate = randrange(0, 101)

        prey = Prey(
            self.environment,
            location,
            max_age,
            birth_rate
        )
        self.agents.append(prey)
