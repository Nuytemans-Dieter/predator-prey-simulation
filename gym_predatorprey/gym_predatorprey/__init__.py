from gym.envs.registration import register

register(
    id='predator-v0',
    entry_point='gym_predatorprey.envs:RlLibWrapperHunter',
)
