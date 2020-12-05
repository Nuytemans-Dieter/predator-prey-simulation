import random
import torch
from collections import namedtuple

# Experience class.
Experience = namedtuple(
    "Experience",
    ("state", "action", "next_state", "reward", "done")
)


# Replay buffer, or memory, to store Experiences.
class ReplayMemory:
    # The buffer will have some set capacity.
    def __init__(self, capacity):
        self.capacity = capacity
        # A memory attribute equal to an empty list.
        # Holds the stored experiences.
        self.memory = []
        # Keep track of how many experiences we've added to memory.
        self.push_count = 0

    def push(self, experience):
        # There is room left in memory.
        if len(self.memory) < self.capacity:
            # Append the experience to memory.
            self.memory.append(experience)
        else:
            # Push new experiences onto the front of memory.
            # Overriding old experiences first.
            self.memory[self.push_count % self.capacity] = experience
        self.push_count += 1

    # Sample experiences from replay memory.
    # We will use these experiences to train our DQN.
    # Batch_size = number of randomly sampled experiences returned.
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    # Returns a boolean value whether or not we can sample from memory.
    def can_provide_sample(self, batch_size):
        return len(self.memory) >= batch_size


# Extract all the states, actions, rewards, next_states & dones into their own tensors
# from a given batch of experiences.
def extract_tensors(experiences):
    batch = Experience(*zip(*experiences))

    t1 = torch.stack(batch.state)
    t2 = torch.stack(batch.action)
    t3 = torch.stack(batch.next_state)
    t4 = torch.stack(batch.reward)
    t5 = torch.stack(batch.done)

    return t1, t2, t3, t4, t5
