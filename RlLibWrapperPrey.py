from random import randrange

import gym as gym

from EnvironmentSimulator import EnvironmentSimulator
from visuals.renderer import Renderer


class RlLibWrapperPrey(gym.Env):


    def __init__(self):
        self.simulator = EnvironmentSimulator()

        start_num_hunters = 25
        start_num_preys = 150

        # Populate the environment
        i = 0
        while i < max(start_num_hunters, start_num_preys):
            if i < start_num_hunters:
                self.simulator.spawn_hunter()
            if i < start_num_preys:
                self.simulator.spawn_prey()
            i += 1

        print('Starting simulation...')
        self.renderer = Renderer(self.simulator)

    def reset(self):
        self.simulator = EnvironmentSimulator()

    def step(self, action):

        preys = []

        # TODO get a move for everyone first

        # Perform random movements/actions
        for hunter in self.simulator.hunterModel.agents:
            hunter.do_action( randrange(0, 5) )
        for prey in self.simulator.preyModel.agents:
            # TODO get agent action
            prey.do_action( randrange(0, 4) )
            preys.append( prey )

        # Execute the result of these actions
        for hunter in self.simulator.hunterModel.agents:
            hunter.finish_action()
        for prey in self.simulator.preyModel.agents:
            prey.finish_action()

        # Gather step data
        self.simulator.num_hunter_data.append( self.simulator.hunterModel.get_num_agents() )
        self.simulator.num_prey_data.append( self.simulator.preyModel.get_num_agents() )
        print('\nTime step ' + str(self.simulator.time) )
        print('Num preys: ' + str(self.simulator.num_prey_data[-1]) )
        print('Num hunters: ' + str(self.simulator.num_hunter_data[-1]) )

        self.simulator.time += 1
        self.renderer.render_state()

        # TODO Reward moet nog verder over nagedacht worden
        reward = preys.__len__()

        obs = []
        for prey in preys:
            # TODO Momenteel random stap, moet aangepast worden
            obs.append({
                "obs": prey.get_state(),
                "reward": reward,
                "done": not self.simulator.preyModel.agents.__contains__( prey )
            })
        return obs
