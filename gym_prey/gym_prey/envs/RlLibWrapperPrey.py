from random import randrange
from numpy import inf
from EnvironmentSimulator import EnvironmentSimulator
from visuals.renderer import Renderer

import datetime
import json
import gym as gym
import numpy as np


class RlLibWrapperPrey(gym.Env):

    def __init__(self, config):
        # Actions: Up, down, left, right.
        self.action_space = gym.spaces.Discrete(4)
        # Observation looks like: [age, closestX, closestY]
        self.observation_space = gym.spaces.Box(
            np.array([0, -config['size_x'], -config['size_y']], dtype=np.float32),
            np.array([config['max_age_prey'], config['size_x'], config['size_y']], dtype=np.float32),
            dtype=np.float32
        )

        # Configuration environment.
        self.config = config

        # Simulator.
        self.simulator = EnvironmentSimulator(config)

        # Number of hunters and preys.
        self.start_num_hunters = config['start_num_hunters']
        self.start_num_preys = config['start_num_preys']

        # The maximum amount of time for one timestep.
        self.time_limit = config['step_limit_time']

        # Populate the environment.
        i = 0
        while i < max(self.start_num_hunters, self.start_num_preys):
            if i < self.start_num_hunters:
                self.simulator.spawn_hunter()
            if i < self.start_num_preys:
                self.simulator.spawn_prey()
            i += 1

        print('START: PREY SIMULATION')

        # Visualize environment.
        # self.renderer = Renderer(self.simulator, self.config)

    def reset(self):
        print("RESETTING THE ENVIRONMENT THROUGH RUN AGENT")

        # Reset the environment
        self.simulator.time = 0
        self.simulator = EnvironmentSimulator(self.config)

        # Provide an initial observation.
        is_group_dead = self.simulator.preyModel.agents.__len__() == 0 or self.simulator.hunterModel.agents.__len__() == 0
        reward = self.simulator.preyModel.calculate_reward(self.start_num_preys, self.start_num_preys, 1.2)

        obs = []
        for prey in self.simulator.preyModel.agents:
            obs.append((
                prey.get_state(),
                reward,
                        (not self.simulator.preyModel.agents.count(prey) > 0) or
                        is_group_dead,
                {}
            ))

        # TODO return obs instead of this placeholder.
        return np.array((4, 4, 2))

    def step(self, action):
        print("PERFORMING A STEP THROUGH RUN AGENT")
        print(action)

        # Starting time.
        start = datetime.datetime.now()

        preys = []

        # TODO get an action for all preys first.

        # Perform random movements/actions for preys.
        for hunter in self.simulator.hunterModel.agents:
            # Hunter does random action.
            hunter.do_action(randrange(0, 5))

        for prey in self.simulator.preyModel.agents:

            # TODO get agent action.

            # Prey does random action.
            prey.do_action(randrange(0, 4))
            # Put prey in the original list.
            preys.append(prey)

        # Execute the result of these actions.
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

        # Next timestep in simulator.
        self.simulator.time += 1
        # Render state of environment.
        # self.renderer.render_state()

        # Calculate joint reward.
        num_agents_before = preys.__len__()
        num_agents_after = self.simulator.preyModel.agents.__len__()
        reward = self.simulator.preyModel.calculate_reward(num_agents_before, num_agents_after, 1.2)

        # Ending time.
        end = datetime.datetime.now()
        # Difference in time.
        delta = (end - start).seconds
        # Whether to stop the episode or not (because it takes to long).
        timeout = delta >= self.time_limit

        is_group_dead = self.simulator.preyModel.agents.__len__() == 0 or self.simulator.hunterModel.agents.__len__() == 0

        obs = []
        for prey in preys:
            # TODO Currently the agents execute a random action. This needs to be the specified action.
            obs.append((
                prey.get_state(),
                reward,
                timeout or (not self.simulator.preyModel.agents.count(prey) > 0) or is_group_dead
            ))

        if is_group_dead:
            self.reset()

        return obs

    def render(self, mode='human', close=False):
        print("RENDERING THROUGH RUN AGENT")
        return 0
