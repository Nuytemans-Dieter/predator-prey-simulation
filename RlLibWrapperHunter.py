from random import randrange

import gym as gym
import datetime

from ray.tune import register_env

from EnvironmentSimulator import EnvironmentSimulator
from visuals.renderer import Renderer


class RlLibWrapperPrey(gym.Env):

    def __init__(self, config):
        self.config = config
        self.simulator = EnvironmentSimulator(config)

        start_num_hunters = config['start_num_hunters']
        start_num_preys = config['start_num_preys']

        self.time_limit = config['step_limit_time']

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

        start = datetime.datetime.now()

        hunters = []

        # TODO get an action for all hunters first

        # Perform random movements/actions
        for hunter in self.simulator.hunterModel.agents:
            # TODO get agent action
            hunter.do_action(randrange(0, 5))
            hunters.append(hunter)
        for prey in self.simulator.preyModel.agents:
            prey.do_action(randrange(0, 4))

        # Execute the result of these actions
        for hunter in self.simulator.hunterModel.agents:
            hunter.finish_action()
        for prey in self.simulator.preyModel.agents:
            prey.finish_action()

        # Gather step data
        self.simulator.num_hunter_data.append(self.simulator.hunterModel.get_num_agents())
        self.simulator.num_prey_data.append(self.simulator.preyModel.get_num_agents())
        print('\nTime step ' + str(self.simulator.time))
        print('Num preys: ' + str(self.simulator.num_prey_data[-1]))
        print('Num hunters: ' + str(self.simulator.num_hunter_data[-1]))

        self.simulator.time += 1
        self.renderer.render_state()

        num_agents_before = hunters.__len__()
        num_agents_after = self.simulator.hunterModel.agents.__len__()
        reward = self.simulator.hunterModel.calculate_reward(num_agents_before, num_agents_after, 1.2)

        end = datetime.datetime.now()
        delta = (end - start).seconds
        timeout = delta >= self.time_limit

        obs = []
        for hunter in hunters:
            # TODO Momenteel random stap, moet aangepast worden
            obs.append({
                "obs": hunter.get_state(),
                "reward": reward,
                "done": timeout or
                        (not self.simulator.preyModel.agents.count(hunter) > 0) or
                        self.simulator.preyModel.agents.__len__() == 0 or
                        self.simulator.hunterModel.agents.__len__() == 0
            })
        return obs


def env_creator(config):
    return RlLibWrapperPrey(config)


register_env("predator-prey", env_creator)
