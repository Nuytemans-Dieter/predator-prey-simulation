from random import randrange

from agents.Agent import Agent


class Hunter(Agent):

    smell_distance = 1

    energy = 0
    energy_to_reproduce = 0
    energy_per_prey_eaten = 0

    def __init__(self, environment, energy, location, max_age, energy_to_reproduce, energy_per_prey_eaten):
        super().__init__(environment, location, max_age)
        self.energy = energy
        self.energy_to_reproduce = energy_to_reproduce
        self.energy_per_prey_eaten = energy_per_prey_eaten

    def move(self):
        print('Moving Hunter')
        move = self.get_random_move()
        self.location += move

        prey_indexes = self.environment.get_agent_indexes_at( self.location )
        # Look for preys at this location and eat them

        # Check reproduction chance and spawn new

        # Check if max age is reached -> die

        # Check nog enough energy -> die
