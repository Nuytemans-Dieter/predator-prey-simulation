from random import randrange

from agents.Prey import Prey
from models.Model import Model


class PreyModel(Model):

    def __init__(self, environment):
        super().__init__(environment)

    def create_agent(self):
        location = (
            randrange(0, self.environment.size_x),
            randrange(0, self.environment.size_y)
        )
        # max_age = randrange(0, 51)
        max_age = 20
        # birth_rate = randrange(0, 101)
        birth_rate = 1
        prey = Prey(
            self.environment,
            location,
            max_age,
            birth_rate
        )
        self.agents.append(prey)
