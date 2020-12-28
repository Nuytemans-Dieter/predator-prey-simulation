from random import randrange
from EnvironmentSimulator import EnvironmentSimulator
from visuals.renderer import Renderer
from ray.rllib.env import MultiAgentEnv

import datetime
import json
import gym as gym
import numpy as np


class RlLibWrapperHunter(gym.Env, MultiAgentEnv):

    def __init__(self, config):
        # print("RlLibWrapperHunter: __init__")

        # The action space ranges [0, 3] where:
        #  `0` move up
        #  `1` move down
        #  `2` move left
        #  `3` move right
        #  `4` reproduce (if hunter has enough energy)
        self.action_space = gym.spaces.Discrete(5)

        # Observation           min         max:
        # age                   0           max age
        # energy                0
        # x closest hunter      -width      width
        # y closest hunter      -height     height
        low = np.array([0, 0, -config['size_x'], -config['size_y']], dtype=np.float32)
        high = np.array([config['max_age_hunter'], float('inf'), config['size_x'], config['size_y']], dtype=np.float32)
        self.observation_space = gym.spaces.Box(
            low=low,
            high=high,
            dtype=np.float32
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
        # print("RlLibWrapperHunter: reset")

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
        for hunter in self.simulator.hunterModel.agents:
            observations[hunter.name] = hunter.get_state()

        return observations

    def step(self, actions):
        # print("RlLibWrapperHunter: step")

        # Agents before time step.
        hunters_before_step = self.simulator.hunterModel.agents.copy()

        # Starting time.
        start = datetime.datetime.now()

        # Perform actions.
        for hunter in self.simulator.hunterModel.agents:
            # Agent does given action.
            if hunter.name in actions:
                hunter.do_action(actions[hunter.name])
        for prey in self.simulator.preyModel.agents:
            # Prey does random action.
            prey.do_action(randrange(0, 4))

        # Max age? Food nearby? Reproduce?
        hunters = self.simulator.hunterModel.agents.copy()
        for hunter in hunters:
            hunter.finish_action()

        # Max age? Eaten? Reproduce?
        preys = self.simulator.preyModel.agents.copy()
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
        num_agents_before = hunters_before_step.__len__()
        num_agents_after = self.simulator.hunterModel.agents.__len__()

        reward = self.simulator.hunterModel.calculate_reward(num_agents_before, num_agents_after, 1.2)
        print("INDIVIDUAL REWARD: ", reward)
        print("SUM OF REWARDS: ", reward * num_agents_before)
        # reward = self.simulator.hunterModel.calculate_reward_differential(num_agents_before, num_agents_after, 1.2)

        # Ending time.
        end = datetime.datetime.now()

        # Difference in time.
        delta = (end - start).seconds

        # Whether to stop the episode or not...
        timeout = delta >= self.time_limit  # Because it takes to long.
        last_step = self.simulator.time == self.max_steps  # Because we have reached the last step.

        # Are all hunters or preys dead?
        is_group_dead = self.simulator.preyModel.agents.__len__() == 0 or self.simulator.hunterModel.agents.__len__() == 0

        # Create dictionaries for observations, rewards and dones.
        observations = {}
        rewards = {}
        dones = {}

        # Get observations, rewards, dones from hunters before step.
        for hunter in hunters_before_step:
            observations[hunter.name] = hunter.get_state()
            rewards[hunter.name] = reward
            # Check if hunter stil exists after step.
            # If not, it must have died (energy loss or maximum age).
            done = (not self.simulator.hunterModel.agents.count(hunter) > 0) \
                   or is_group_dead \
                   or timeout \
                   or last_step
            dones[hunter.name] = done

        # Get observations, rewards, dones from hunters born during step.
        for hunter in self.simulator.hunterModel.agents:
            # Found new hunter.
            if (not hunters_before_step.count(hunter) > 0):
                observations[hunter.name] = hunter.get_state()
                rewards[hunter.name] = reward
                done = is_group_dead or timeout or last_step
                dones[hunter.name] = done

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
        # print("RlLibWrapperHunter: render")
        pass

    def close(self):
        # print("RlLibWrapperHunter: close")
        pass

