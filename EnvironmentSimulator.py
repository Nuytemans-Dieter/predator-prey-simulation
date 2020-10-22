from models.HunterModel import HunterModel
from models.PreyModel import PreyModel


class EnvironmentSimulator:

    size_x = 30
    size_y = 30

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

    def __init__(self):
        self.preyModel = PreyModel(self)
        self.hunterModel = HunterModel(self)

    def simulate_step(self):
        for hunter in self.hunterModel.agents:
            hunter.energy -= 1
            hunter.age += 1
            hunter.move()

        for prey in self.preyModel.agents:
            prey.age += 1
            prey.move()

        self.num_hunter_data.append( self.hunterModel.get_num_agents() )
        self.num_prey_data.append( self.preyModel.get_num_agents() )
        print('\nTime step ' + str(self.time) )
        print('Num preys: ' + str(self.num_prey_data[-1]) )
        print('Num hunters: ' + str(self.num_hunter_data[-1]) )
        self.time += 1


    def get_preys_near(self, location, distanceSquared):
        preys = []
        for prey in self.preyModel.agents:
            if self.get_distance_squared( prey.location, location ) <= distanceSquared:
                preys.append( prey )
        return preys

    def kill_prey(self, prey):
        self.preyModel.agents.remove( prey )

    def kill_hunter(self, hunter):
        self.hunterModel.agents.remove( hunter )

    def spawn_prey(self):
        self.preyModel.create_agent()

    def spawn_hunter(self):
        self.hunterModel.create_agent()

    def get_num_hunters(self):
        return self.hunterModel.agents.__len__()

    def get_distance_squared(self, loc1, loc2):
        return loc1[0] + loc2[0] + loc1[1] + loc2[1]
