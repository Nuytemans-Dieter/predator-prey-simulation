from agents.Agent import Agent


class Prey(Agent):

    birth_rate = 0

    def __init__(self, environment, location, max_age, birth_rate):
        super().__init__(environment, location, max_age)
        print('Prey')
        self.birth_rate = birth_rate

    def move(self):
        print('Moving Hunter')

        # Do a random move
        # Check reproduction -> spawn new
        # Check max age -> die
