class Model:

    def __init__(self, environment, config):
        self.environment = environment
        self.agents = []
        self.config = config

    def get_num_agents(self):
        return len( self.agents )

    def create_agent(self):
        raise NotImplementedError("Please Implement the create_agent method for all models")
