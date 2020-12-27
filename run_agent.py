import ray
from ray import tune
from ray.rllib.models import ModelCatalog

from dqn import DQNTrainer, DQNModel
from dqn.prey_policy import PreyPolicy
from dqn.hunter_policy import HunterPolicy
from gym_multipreypredator.envs.RlLibWrapperHunterPrey import RlLibWrapperHunterPrey
import json


# Map the appropriate policy to every agent based on their names.
def policy_mapping(agent_name):
    if "hunter" in agent_name:
        return "hunter"
    else:
        return "prey"


if __name__ == "__main__":
    # TODO: Different model for hunters and preys? Wouter does this.
    # TODO: Investigate reward functions. "calculate_reward_differential" returns imaginary numbers.
    # What reward function is better? Experiment with results.
    # TODO: Create Tensorboard Graphs.
    # For preys against random behaviour.
    # For hunters against random behaviour
    # For hunters and preys training against each other.

    # Read configuration file.
    with open('config.JSON') as config_file:
        config = json.load(config_file)

    # Initialize Ray.
    ray.init()

    # Register a custom model.
    ModelCatalog.register_custom_model("DQNModel", DQNModel)

    policy_config = {
        "hunter_policy_config": {
            # Predator environment.
            "env": "gym_predatorprey:predator-v0",
            # Prey environment.
            # "env": "gym_prey:prey-v0",
            # Prey & Predator environment.
            # "env": "gym_multipreypredator:preypredator-v0",
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
        },
        "prey_policy_config": {
            # Predator environment.
            "env": "gym_predatorprey:predator-v0",
            # Prey environment.
            # "env": "gym_prey:prey-v0",
            # Prey & Predator environment.
            # "env": "gym_multipreypredator:preypredator-v0",
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
    }

    test_env = RlLibWrapperHunterPrey(config)
    policies = {"hunter": (HunterPolicy,
                           test_env.observation_space_hunter,
                           test_env.action_space_hunter,
                           policy_config['hunter_policy_config']),
                "prey": (PreyPolicy,
                         test_env.observation_space_prey,
                         test_env.action_space_prey,
                         policy_config['prey_policy_config'])}

    tune.run(
        # Custom trainer.
        DQNTrainer,
        checkpoint_at_end=True,
        # Do a total of 1000 episodes.
        stop={"episodes_total": 1000},
        # Or do a total of 200000 steps.
        # stop={"timesteps_total": 10000},
        # Configuration.
        config={
            # Predator environment.
            "env": "gym_predatorprey:predator-v0",
            # Prey environment.
            # "env": "gym_prey:prey-v0",
            # Prey & Predator environment.
            # "env": "gym_multipreypredator:preypredator-v0",
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
            "multiagent": {
                "policy_mapping_fn": policy_mapping,
                "policies": policies,
                "policies_to_train": policies,
            },

            # Custom model.
            "dqn_model": {
                # Specify our custom model.
                "custom_model": "DQNModel",
                "custom_model_config": {
                },  # extra options to pass to your model
            },
        }
    )
