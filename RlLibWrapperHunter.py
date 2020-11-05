from random import randrange

import gym as gym

from EnvironmentSimulator import EnvironmentSimulator
from visuals.renderer import Renderer


class RlLibWrapperPrey(gym.Env):


    def __init__(self, config):
        self.config = config
        self.simulator = EnvironmentSimulator(config)

        start_num_hunters = config['start_num_hunters']
        start_num_preys = config['start_num_preys']

        # Populate the environment
        i = 0
        while i < max(start_num_hunters, start_num_preys):
            if i < start_num_hunters:
                self.simulator.spawn_hunter()
            if i < start_num_preys:
                self.simulator.spawn_prey()
            i += 1

        print('Starting simulation...')
        self.renderer = Renderer(self.simulator, config)

    def reset(self):
        self.simulator = EnvironmentSimulator(self.config)

    def step(self, action):

        hunters = []

        # TODO get an action for all hunters first

        # Perform random movements/actions
        for hunter in self.simulator.hunterModel.agents:
            # TODO get agent action
            hunter.do_action( randrange(0, 5) )
            hunters.append( hunter )
        for prey in self.simulator.preyModel.agents:
            prey.do_action( randrange(0, 4) )

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
        reward = hunters.__len__()

        obs = []
        for hunter in hunters:
            # TODO Momenteel random stap, moet aangepast worden
            obs.append({
                "obs": hunter.get_state(),
                "reward": reward,
                "done": (not self.simulator.preyModel.agents.count(hunter) > 0) or
                        self.simulator.preyModel.agents.__len__() == 0 or
                        self.simulator.hunterModel.agents.__len__() == 0
            })
        return obs
