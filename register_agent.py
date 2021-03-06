from ray.tune import register_env


def env_creator(name, config):
    if name == "predator-v0":
        from gym_predatorprey.envs.RlLibWrapperHunter import RlLibWrapperHunter as Env
    elif name == "prey-v0":
        from gym_prey.gym_prey import RlLibWrapperPrey as Env
    elif name == "preypredator-v0":
        from gym_multipreypredator.envs.RlLibWrapperHunterPrey import RlLibWrapperHunterPrey as Env
    else:
        raise NotImplementedError
    return Env(config)


# with open('config.JSON') as config_file:
#     config = json.load(config_file)

name = "predator-v0"
# env = env_creator("predator-v0")
register_env(name, lambda config: env_creator(name, config))
