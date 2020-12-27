from gym.envs.registration import register

register(
    id='preypredator-v0',
    entry_point='gym_multipreypredator.envs:RlLibWrapperHunterPrey',
)
