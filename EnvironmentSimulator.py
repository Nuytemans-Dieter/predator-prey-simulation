from models.HunterModel import HunterModel
from models.PreyModel import PreyModel


class EnvironmentSimulator:
    time = 0

    # Statistics
    num_hunter_data = []
    num_prey_data = []

    hunters_born = 0
    preys_born = 0

    hunter_deaths_by_energy = 0
    hunter_deaths_by_age = 0
    prey_deaths_by_eaten = 0
    prey_deaths_by_age = 0

    def __init__(self, config):
        # Configuration parameters.
        self.size_x = config['size_x']
        self.size_y = config['size_y']

        # Models.
        self.preyModel = PreyModel(self, config)
        self.hunterModel = HunterModel(self, config)

    def simulate_step(self, do_hunters=1, do_preys=1):
        if do_hunters:
            for hunter in self.hunterModel.agents:
                hunter.energy -= 1
                hunter.age += 1
                hunter.move()

        if do_preys:
            for prey in self.preyModel.agents:
                prey.age += 1
                prey.move()

        self.num_hunter_data.append(self.hunterModel.get_num_agents())
        self.num_prey_data.append(self.preyModel.get_num_agents())
        print('\nTime step ' + str(self.time))
        print('Num preys: ' + str(self.num_prey_data[-1]))
        print('Num hunters: ' + str(self.num_hunter_data[-1]))
        self.time += 1

    def get_preys_near(self, location, distance_squared):
        preys = []
        for prey in self.preyModel.agents:
            if self.get_distance_squared(prey.location, location) <= distance_squared:
                preys.append(prey)
        return preys

    def get_nearest_agent(self, location, agents):
        """Get the nearest agent to this location. Returns 0 if there are no agents"""
        distance = -1
        nearest = 0
        for agent in agents:
            agent_distance = self.get_distance_squared(agent.location, location)
            if agent_distance < distance or distance == -1:
                nearest = agent
        return nearest

    def get_nearest_prey(self, location):
        """Get the nearest prey to this location. Returns 0 if there are no preys"""
        return self.get_nearest_agent(location, self.preyModel.agents)

    def get_nearest_hunter(self, location):
        """Get the nearest hunter to this location. Returns 0 if there are no preys"""
        return self.get_nearest_agent(location, self.hunterModel.agents)

    def kill_prey(self, prey):
        self.preyModel.agents.remove(prey)

    def kill_hunter(self, hunter):
        self.hunterModel.agents.remove(hunter)

    def spawn_prey(self):
        self.preyModel.create_agent()

    def spawn_hunter(self):
        self.hunterModel.create_agent()

    def get_num_hunters(self):
        return self.hunterModel.agents.__len__()

    def get_num_preys(self):
        return self.preyModel.agents.__len__()

    def get_distance_squared(self, loc1, loc2):
        return loc1[0] + loc2[0] + loc1[1] + loc2[1]
