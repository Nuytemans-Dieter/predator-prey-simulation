import torch
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

from ray.rllib.policy import Policy
from ray.rllib.models import ModelCatalog

from dqn.QValues import get_current, get_next
from dqn.ReplayMemory import ReplayMemory, Experience, extract_tensors
from dqn.Strategy import EpsilonGreedyStrategy

import random


class HunterPolicy(Policy):

    def __init__(self, observation_space, action_space, config):
        Policy.__init__(self, observation_space, action_space, config)
        self.observation_space = observation_space
        self.action_space = action_space
        self.config = config
        self.action_shape = action_space.n

        # GPU settings
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")

        # This attribute will be incremented every time learn_on_batch is called.
        self.iteration = 0

        # The current time step.
        self.current_step = 0

        # Agent parameters.
        self.lr = self.config["lr"]
        self.gamma = self.config["gamma"]
        self.target_update_frequency = self.config["target_update_frequency"]

        # Strategy
        self.strategy = \
            EpsilonGreedyStrategy(self.config["eps_start"], self.config["eps_end"], self.config["eps_decay"])

        # Replay memory
        self.memory = ReplayMemory(self.config["replay_memory_size"])

        # Policy network
        self.policy_net = ModelCatalog.get_model_v2(
            obs_space=self.observation_space,
            action_space=self.action_space,
            num_outputs=5,
            name="DQNModel",
            model_config=self.config["dqn_model"],
            framework="torch",
        ).to(self.device, non_blocking=True)

        # Target network
        self.target_net = ModelCatalog.get_model_v2(
            obs_space=self.observation_space,
            action_space=self.action_space,
            num_outputs=5,
            name="DQNModel",
            model_config=self.config["dqn_model"],
            framework="torch",
        ).to(self.device, non_blocking=True)

        # Set the weights & biases in the target_net to be the same as those in the policy_net.
        self.target_net.load_state_dict(self.policy_net.state_dict())
        # Put target_net in eval mode. This network will only be used for inference.
        self.target_net.eval()

        # Optimizer.
        self.optimizer = optim.RMSprop(self.policy_net.parameters())

        # The calculated loss.
        self.loss = 0

    def compute_actions(self,
                        obs_batch,
                        state_batches=None,
                        prev_action_batch=None,
                        prev_reward_batch=None,
                        info_batch=None,
                        episodes=None,
                        explore=None,
                        timestep=None,
                        strategy=None,
                        **kwargs):

        # print("DQNPolicy: Compute Actions")

        obs_batch_t = torch.tensor(obs_batch).type(torch.FloatTensor)

        # Get the exploration rate:
        rate = self.strategy.get_exploration_rate(self.current_step)

        # Next time step.
        self.current_step += 1

        epsilon_log = []

        # Exploitation.
        # Turn off gradient tracking.
        with torch.no_grad():
            value_batch_t = self.policy_net(obs_batch_t)
            action_batch_t = torch.argmax(value_batch_t, axis=1)

        # Exploration.
        for index in range(len(action_batch_t)):
            epsilon_log.append(rate)
            if np.random.random() < rate:
                action_batch_t[index] = random.randint(0, self.action_shape - 1)

        actions = action_batch_t.cpu().detach().tolist()
        return actions, [], {}

    def learn_on_batch(self, samples):

        # print("DQNPolicy: Learn On Batch")

        self.iteration += 1

        # Get the states, actions, rewards, next_states & dones.
        states = torch.tensor(np.array(samples["obs"])).type(torch.FloatTensor)
        actions = torch.tensor(np.array(samples["actions"]))
        rewards = torch.tensor(np.array(samples["rewards"])).type(torch.FloatTensor)
        next_states = torch.tensor(np.array(samples["new_obs"])).type(torch.FloatTensor)
        dones = torch.tensor(np.array(samples["dones"])).type(torch.FloatTensor)

        # train_batch_size
        batch_size = len(states)

        # Add experiences to Replay Memory.
        for x in range(batch_size):
            self.memory.push(Experience(states[x], actions[x], next_states[x], rewards[x], dones[x]))

        # Can we get samples from memory to train our DQN?
        if self.memory.can_provide_sample(batch_size):
            # If yes, sample experiences from memory.
            experiences = self.memory.sample(batch_size)
            states, actions, next_states, rewards, dones = extract_tensors(experiences)

            # Get current Q values.
            current_q_values = get_current(self.policy_net, states, actions)
            # Get next Q values.
            next_q_values = get_next(self.target_net, next_states)
            # Get target Q values.
            target_q_values = (next_q_values.unsqueeze(1) * self.gamma) + rewards.unsqueeze(1)

            # Termination states:
            for i in range(batch_size):
                if dones[i] == 1:
                    target_q_values[i] = rewards[i]

            # Calculate the loss.
            self.loss = F.smooth_l1_loss(current_q_values.unsqueeze(1), target_q_values.unsqueeze(1))
            # Zero out the gradients.
            self.optimizer.zero_grad()
            # Calculate the gradient of the loss with respect to all weights and biases int he policy_net.
            self.loss.backward()

            for param in self.policy_net.parameters():
                param.grad.data.clamp_(-1, 1)

            # Updates weights and biases.
            self.optimizer.step()

            # Update the target network every x steps.
            if self.iteration % self.target_update_frequency == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())

        return {"learner_stats": {"loss": self.loss}}

    def get_weights(self):
        # Trainer function
        weights = {}
        weights["dqn_model"] = self.policy_net.cpu().state_dict()
        self.policy_net.to(self.device, non_blocking=False)
        return weights

    def set_weights(self, weights):
        # Worker function
        if "dqn_model" in weights:
            self.policy_net.load_state_dict(weights["dqn_model"], strict=True)
            self.policy_net.to(self.device, non_blocking=False)

