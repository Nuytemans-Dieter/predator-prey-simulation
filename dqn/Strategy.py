import math


class EpsilonGreedyStrategy:
    # Starting, ending & decay values of Epsilon.
    def __init__(self, start, end, decay):
        self.start = start
        self.end = end
        self.decay = decay

    # Calculates the exploration rate for the current time step.
    # Epsilon = the probability that our agent will explore the environment rather than exploit it.
    def get_exploration_rate(self, current_step):
        return self.end + (self.start - self.end) * \
               math.exp(-1. * current_step * self.decay)
