from gym.envs.registration import register

register(
    id='prey-v0',
    entry_point='gym_prey.envs:RlLibWrapperPrey',
)
