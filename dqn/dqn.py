from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from ray.rllib.agents import with_common_config
from ray.rllib.agents.trainer_template import build_trainer

from dqn.dqn_policy import DQNPolicy

# Create a logger with name "__name__".
logger = logging.getLogger(__name__)

DEFAULT_CONFIG = with_common_config({
    ########################################
    # Parameters Agent
    ########################################
    "lr": 1,
    "gamma": 1,
    "eps_start": 1,
    "eps_end": 1,
    "eps_decay": 1,
    "replay_memory_size": 1,
    "target_update_frequency": 1,


    "dqn_model": {
        "custom_model": "?",
        "custom_model_config": {
        },  # extra options to pass to your model
    }
})

# Define a custom trainer.
DQNTrainer = build_trainer(
    name="DQNAlgorithm",
    # The default policy class to use.
    default_policy=DQNPolicy,
    default_config=DEFAULT_CONFIG)

