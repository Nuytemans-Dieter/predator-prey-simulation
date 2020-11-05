import json

import ray
from ray import tune
from ray.rllib.models import ModelCatalog

from dqn import DQNTrainer, DQNModel

if __name__ == "__main__":

    # Read configuration file.
    with open('config.JSON') as config_file:
        config = json.load(config_file)

    ray.init()
    # Register a custom model that can later be used in the model config.
    ModelCatalog.register_custom_model("DQNModel", DQNModel)

    tune.run(
        # Our custom trainer.
        DQNTrainer,
        #checkpoint_freq=10,
        checkpoint_at_end=True,
        # Do a total of 1000 episodes.
        stop={"episodes_total": 1000},
        config={
            "env": "predator_prey",
            "env_config": config,
            "num_gpus": 0,
            "num_workers": 2,
            "framework": "torch",
            # How many steps back the return will be determined.
            "rollout_fragment_length": 20,
            # The environment we'll be working in.
            "train_batch_size": 2000,

            ########################################
            # Parameters Agent
            ########################################
            "lr": 0.00005,
            "gamma": 0.999,
            "eps_start": 1,
            "eps_end": 0.001,
            "eps_decay": 0.0001,
            "replay_memory_size": 20000,
            "target_update_frequency": 10,

            "dqn_model": {
                # Specify our custom model.
                "custom_model": "DQNModel",
                "custom_model_config": {
                },  # extra options to pass to your model
            }
        }
    )
