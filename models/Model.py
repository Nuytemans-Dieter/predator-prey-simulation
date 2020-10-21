class Model:

    agents = []

    def __init__(self, environment):
        print('Model')
        self.environment = environment

    def get_num_agents(self):
        return len( self.agents )

    def create_agent(self):
        raise NotImplementedError("Please Implement the create_agent method for all models")
