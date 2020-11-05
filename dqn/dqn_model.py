from torch import nn, cat
from ray.rllib.utils.annotations import override
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from gym.spaces import Discrete, Box


# Deep Q-Network, or DQN.
# Our network, and all of its layers, will extend the nn.Module class.
class DQNModel(nn.Module, TorchModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config,
                 name):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs,
                              model_config, name)
        nn.Module.__init__(self)

        self.obs_space = obs_space
        self.action_space = action_space
        self.model_config = model_config
        self.name = name

        if isinstance(self.obs_space, Box):
            self.obs_shape = obs_space.shape[0]
        else:
            self.obs_shape = self.obs_space

        # Structure of DQN:
        self.layers = nn.Sequential()
        self.layers.add_module("linear_1", nn.Linear(self.obs_space.shape[0], 64))
        self.layers.add_module("relu_1", nn.ReLU())
        self.layers.add_module("linear_2", nn.Linear(64, 128))
        self.layers.add_module("relu_2", nn.ReLU())
        self.layers.add_module("linear_3", nn.Linear(128, 64))
        self.layers.add_module("relu_3", nn.ReLU())
        self.layers.add_module("linear_4", nn.Linear(64, num_outputs))

    @override(TorchModelV2)
    def forward(self, obs):
        return self.layers(obs)
