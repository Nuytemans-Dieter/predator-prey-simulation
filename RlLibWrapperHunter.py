import gym as gym

from EnvironmentSimulator import EnvironmentSimulator


class RlLibWrapperPrey(gym.Env):


    def __init__(self):
        self.simulator = EnvironmentSimulator()

    def reset(self):
        self.simulator = EnvironmentSimulator()

    def step(self, action):
        # Geef de eventuele observaties en rewards van elk prooiterug
        #return <obs>, <reward: float>, <done: bool>

        obs = []

        # TODO Reward wordt nog open gelaten
        reward = 0

        for hunter in self.simulator.hunterModel:
            # TODO Momenteel random stap, moet aangepast worden
            hunter.move()
            obs.append({
                "obs": hunter.get_state(),
                "reward": reward,
                # TODO: Verplaats het toevoegen van done naar na achter de step van de hunters
                "done": not self.simulator.hunterModel.agents.__contains__( hunter )
            })

        # Make simulator only move the hunters
        self.simulator.simulate_step(do_hunters=0, do_preys=1)

        return obs
