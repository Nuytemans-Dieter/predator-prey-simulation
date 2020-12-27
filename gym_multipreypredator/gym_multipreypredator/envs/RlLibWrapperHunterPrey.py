from EnvironmentSimulator import EnvironmentSimulator
from ray.rllib.env import MultiAgentEnv

import datetime
import gym as gym
import numpy as np

from visuals.renderer import Renderer


class RlLibWrapperHunterPrey(gym.Env, MultiAgentEnv):

    def __init__(self, config):
        # print("RlLibWrapperHunterPrey: __init__")

        ########################################
        # Configuration Preys
        ########################################

        # The action space ranges [0, 3] where:
        #  `0` move up
        #  `1` move down
        #  `2` move left
        #  `3` move right
        self.action_space_prey = gym.spaces.Discrete(4)

        # Observation           min         max:
        # age                   0           max age
        # x closest hunter      -width      width
        # y closest hunter      -height     height
        low = np.array([0, -config['size_x'], -config['size_y']], dtype=np.float32)
        high = np.array([config['max_age_prey'] + 1, config['size_x'], config['size_y']], dtype=np.float32)
        self.observation_space_prey = gym.spaces.Box(
            low=low,
            high=high,
            dtype=np.float32
        )

        ########################################
        # Configuration Hunters
        ########################################

        # The action space ranges [0, 3] where:
        #  `0` move up
        #  `1` move down
        #  `2` move left
        #  `3` move right
        #  `4` reproduce (if hunter has enough energy)
        self.action_space_hunter = gym.spaces.Discrete(5)

        # Observation           min         max:
        # age                   0           max age
        # energy                0
        # x closest hunter      -width      width
        # y closest hunter      -height     height
        low = np.array([0, 0, -config['size_x'], -config['size_y']], dtype=np.float32)
        high = np.array([config['max_age_hunter'], float('inf'), config['size_x'], config['size_y']], dtype=np.float32)
        self.observation_space_hunter = gym.spaces.Box(
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
        # print("RlLibWrapperHunterPrey: reset")

        # Create new simulator.
        self.simulator = EnvironmentSimulator(self.config)

        # Create renderer for visualization.
        self.renderer = Renderer(self.simulator, self.config)

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
        for prey in self.simulator.preyModel.agents:
            observations[prey.name] = prey.get_state()

        return observations

    def step(self, actions):
        # print("RlLibWrapperHunterPrey: step")

        # Agents before time step.
        preys_before_step = self.simulator.preyModel.agents.copy()
        hunters_before_step = self.simulator.hunterModel.agents.copy()

        # Starting time.
        start = datetime.datetime.now()

        # Perform actions.
        for hunter in self.simulator.hunterModel.agents:
            # Hunter does given action.
            if hunter.name in actions:
                hunter.do_action(actions[hunter.name])
        for prey in self.simulator.preyModel.agents:
            # Prey does given action.
            if prey.name in actions:
                prey.do_action(actions[prey.name])

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

        # Calculate joint reward for preys.
        num_preys_before = preys_before_step.__len__()
        num_preys_after = self.simulator.preyModel.agents.__len__()
        reward_for_preys = self.simulator.preyModel.calculate_reward(num_preys_before, num_preys_after, 1.2)

        # Calculate joint reward for hunters.
        num_hunters_before = hunters_before_step.__len__()
        num_hunters_after = self.simulator.hunterModel.agents.__len__()
        reward_for_hunters = self.simulator.hunterModel.calculate_reward(num_hunters_before, num_hunters_after, 1.2)

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

        # Get observations, rewards, dones from preys before step.
        for prey in preys_before_step:
            observations[prey.name] = prey.get_state()
            rewards[prey.name] = reward_for_preys
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
            if not preys_before_step.count(prey) > 0:
                observations[prey.name] = prey.get_state()
                rewards[prey.name] = reward_for_preys
                done = is_group_dead or timeout or last_step
                dones[prey.name] = done

        # Get observations, rewards, dones from hunters before step.
        for hunter in hunters_before_step:
            observations[hunter.name] = hunter.get_state()
            rewards[hunter.name] = reward_for_hunters
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
            if not hunters_before_step.count(hunter) > 0:
                observations[hunter.name] = hunter.get_state()
                rewards[hunter.name] = reward_for_hunters
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

    def render(self, mode='human'):
        # print("RlLibWrapperHunterPrey: render")
        # self.renderer.render_state()
        pass

    def close(self):
        # print("RlLibWrapperHunterPrey: close")
        pass
