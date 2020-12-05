from ray import tune
from ray.rllib.models import ModelCatalog
from dqn import DQNTrainer, DQNModel

import json
import ray

if __name__ == "__main__":
    # Read configuration file.
    with open('config.JSON') as config_file:
        config = json.load(config_file)

    # Initialize Ray.
    ray.init()

    # Register a custom model.
    ModelCatalog.register_custom_model("DQNModel", DQNModel)

    tune.run(
        # Custom trainer.
        DQNTrainer,
        checkpoint_at_end=True,
        # Do a total of 1000 episodes.
        stop={"episodes_total": 1000},
        # Configuration.
        config={
            # Predator environment.
            # "env": "gym_predatorprey:predator-v0",
            # Prey environment.
            "env": "gym_prey:prey-v0",
            # Configuration environment.
            "env_config":
                {
                    "config": config
                },

            "num_gpus": 0,
            "num_workers": 1,
            "framework": "torch",

            # How many steps back the return will be determined.
            "rollout_fragment_length": 20,
            # Number of samples processed before the model is updated.
            "train_batch_size": 10,

            # Agent parameters:
            "lr": 4e-3,
            "gamma": 0.985,
            "eps_start": 1,
            "eps_end": 0.001,
            "eps_decay": 0.0001,
            "replay_memory_size": 20000,
            "target_update_frequency": 10,

            # Custom model.
            "dqn_model": {
                # Specify our custom model.
                "custom_model": "DQNModel",
                "custom_model_config": {
                },  # extra options to pass to your model
            },
        }
    )
