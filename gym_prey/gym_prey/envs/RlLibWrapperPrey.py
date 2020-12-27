from random import randrange
from EnvironmentSimulator import EnvironmentSimulator
from visuals.renderer import Renderer
from ray.rllib.env import MultiAgentEnv

import datetime
import json
import gym as gym
import numpy as np


class RlLibWrapperPrey(gym.Env, MultiAgentEnv):

    def __init__(self, config):
        # print("RlLibWrapperPrey: __init__")

        # The action space ranges [0, 3] where:
        #  `0` move up
        #  `1` move down
        #  `2` move left
        #  `3` move right
        self.action_space = gym.spaces.Discrete(4)

        # Observation           min         max:
        # age                   0           max age
        # x closest hunter      -width      width
        # y closest hunter      -height     height
        low = np.array([0, -config['size_x'], -config['size_y']], dtype=np.float32)
        high = np.array([config['max_age_prey'] + 1, config['size_x'], config['size_y']], dtype=np.float32)
        self.observation_space = gym.spaces.Box(
            low = low,
            high = high,
            dtype = np.float32
        )

        # Configuration environment.
        self.config = config

        # Max amount of steps per episode.
        self.max_steps = config['max_steps']

        # The maximum amount of time for one timestep.
        self.time_limit = config['step_limit_time']

        # Reset the environment to the start of an episode.
        self.reset()

    def reset(self):
        # print("RlLibWrapperPrey: reset")

        # Create new simulator.
        self.simulator = EnvironmentSimulator(self.config)

        # First time step.
        self.simulator.time = 0

        # Number of hunters and preys.
        self.start_num_hunters = self.config['start_num_hunters']
        self.start_num_preys = self.config['start_num_preys']

        # Populate the environment.
        i = 0
        while i < max(self.start_num_hunters, self.start_num_preys):
            if i < self.start_num_hunters:
                self.simulator.spawn_hunter()
            if i < self.start_num_preys:
                self.simulator.spawn_prey()
            i += 1

        # Create dictionary for observations.
        observations = {}

        # Provide an initial observation.
        for prey in self.simulator.preyModel.agents:
            observations[prey.name] = prey.get_state()

        return observations

    def step(self, actions):
        # print("RlLibWrapperPrey: step")

        # Original preys.
        preys_before_step = self.simulator.preyModel.agents.copy()

        # Starting time.
        start = datetime.datetime.now()

        # Perform actions.
        for hunter in self.simulator.hunterModel.agents:
            # Hunter does random action.
            hunter.do_action( randrange(0, 5) )
        for prey in self.simulator.preyModel.agents:
            # Agent does given action.
            if prey.name in actions:
                prey.do_action(actions[prey.name])

        # Max age? Food nearby? Reproduce?
        hunters = self.simulator.hunterModel.agents.copy()
        for hunter in hunters:
            hunter.finish_action()

        preys = self.simulator.preyModel.agents.copy()
        # Max age? Eaten? Reproduce?
        for prey in preys:
            prey.finish_action()

        # Next timestep.
        self.simulator.time += 1

        # Gather step data.
        self.simulator.num_hunter_data.append(self.simulator.hunterModel.get_num_agents())
        self.simulator.num_prey_data.append(self.simulator.preyModel.get_num_agents())

        # Print step data.
        # self.simulator.print_step_data()

        # Calculate joint reward.
        num_agents_before = preys_before_step.__len__()
        num_agents_after = self.simulator.preyModel.agents.__len__()

        reward = self.simulator.preyModel.calculate_reward(num_agents_before, num_agents_after, 1.2)
        # reward = self.simulator.preyModel.calculate_reward_differential(num_agents_before, num_agents_after, 1.2)

        # Ending time.
        end = datetime.datetime.now()

        # Difference in time.
        delta = (end - start).seconds

        # Whether to stop the episode or not...
        timeout = delta >= self.time_limit                   # Because it takes to long.
        last_step = self.simulator.time == self.max_steps    # Because we have reached the last step.

        # Are all hunters or preys dead?
        is_group_dead = self.simulator.preyModel.agents.__len__() == 0 or self.simulator.hunterModel.agents.__len__() == 0

        # Create dictionaries for observations, rewards and dones.
        observations = {}
        rewards = {}
        dones = {}

        # Get observations, rewards, dones from preys before step.
        for prey in preys_before_step:
            observations[prey.name] = prey.get_state()
            rewards[prey.name] = reward
            # Check if prey stil exists after step.
            # If not, it must have died (eaten or maximum age).
            done = (not self.simulator.preyModel.agents.count(prey) > 0) \
                   or is_group_dead \
                   or timeout \
                   or last_step
            dones[prey.name] = done

        # Get observations, rewards, dones from preys born during step.
        for prey in self.simulator.preyModel.agents:
            # Found new prey.
            if (not preys_before_step.count(prey) > 0):
                observations[prey.name] = prey.get_state()
                rewards[prey.name] = reward
                done = is_group_dead or timeout or last_step
                dones[prey.name] = done

        # Stop episode if..
        # 1) All agents are dead
        # 2) Step execution time is too high
        # 3) Reached maximum step.
        if is_group_dead or timeout or last_step:
            dones['__all__'] = True
        else:
            dones['__all__'] = False

        # print(observations)
        # print(dones)
        return observations, rewards, dones, {}

    def render(self, mode='human', close=False):
        # print("RlLibWrapperPrey: render")
        pass

    def close(self):
        # print("RlLibWrapperPrey: close")
        pass
