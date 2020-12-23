from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from ray.rllib.agents import with_common_config
from ray.rllib.agents.trainer_template import build_trainer

from dqn.dqn_policy import DQNPolicy
from dqn.prey_policy import PreyPolicy


logger = logging.getLogger(__name__)

DEFAULT_CONFIG = with_common_config({
    # Agent parameters.
    "lr": 0.001,
    "gamma": 0.9,
    "eps_start": 1,
    "eps_end": 0.05,
    "eps_decay": 0.9995,
    "replay_memory_size": 10000,
    "target_update_frequency": 10,

    "dqn_model": {
        "custom_model": "DQNModel",
        "custom_model_config": {
        },  # Extra options to pass to your model (e.g. network of model).
    }
})

# Custom trainer.
DQNTrainer = build_trainer(
    name="DQNAlgorithm",
    default_policy=DQNPolicy,
    default_config=DEFAULT_CONFIG)
