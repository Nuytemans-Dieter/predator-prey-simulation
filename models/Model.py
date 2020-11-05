class Model:

    def __init__(self, environment, config):
        self.environment = environment
        self.agents = []
        self.config = config

    def calculate_reward(self, num_agents_before, num_agents_after, exponent):
        return num_agents_before ** exponent

    def calculate_reward_differential(self, num_agents_before, num_agents_after, exponent):
        difference = num_agents_before - num_agents_after
        # Difference > 0: more agents now than at the start -> Good
        # Difference = 0: equal amount -> Meh
        # Difference < 0: less agents now than at the start -> Bad
        difference_altered = difference ** exponent
        do_flip_sign = difference < 0
        if do_flip_sign:
            difference_altered = -difference_altered

        return difference_altered

    def get_num_agents(self):
        return len(self.agents)

    def create_agent(self):
        raise NotImplementedError("Please Implement the create_agent method for all models")
