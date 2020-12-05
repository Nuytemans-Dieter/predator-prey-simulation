from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ray.rllib.agents import with_common_config
from ray.rllib.agents.trainer_template import build_trainer

from dqn_hunter.hunter_policy import HunterPolicy

import logging


# Create logger.
logger = logging.getLogger(__name__)

DEFAULT_CONFIG = with_common_config({
    # Agent parameters.
    "lr": 0.001,
    "gamma": 0.999,
    "eps_start": 1,
    "eps_end": 0.001,
    "eps_decay": 0.0001,
    "replay_memory_size": 20000,
    "target_update_frequency": 10,

    "dqn_model": {
        "custom_model": "DQNModel",
        "custom_model_config": {
        },  # extra options to pass to your model (e.g. network of model)
    }
})

# Custom trainer.
DQNTrainer = build_trainer(
    name="DQNModel",
    # The default policy class to use.
    default_policy=HunterPolicy,
    default_config=DEFAULT_CONFIG)
