import gym as gym

from EnvironmentSimulator import EnvironmentSimulator


class RlLibWrapperPrey(gym.Env):


    def __init__(self):
        self.action_space = EnvironmentSimulator()
        self.observation_space = EnvironmentSimulator()
        self.simulator = EnvironmentSimulator()

    def reset(self):
        self.simulator = EnvironmentSimulator()

    def step(self, action):
        # Geef de eventuele observaties en rewards van elk prooiterug
        #return <obs>, <reward: float>, <done: bool>

        obs = []

        # TODO Reward wordt nog open gelaten
        reward = 0

        for prey in self.simulator.preyModel:
            # TODO Momenteel random stap, moet aangepast worden
            prey.move()
            obs.append({
                "obs": prey.get_state(),
                "reward": reward,
                # TODO: Verplaats het toevoegen van done naar na achter de step van de hunters
                "done": not self.simulator.preyModel.agents.__contains__( prey )
            })

        # Make simulator only move the hunters
        self.simulator.simulate_step(do_hunters=1, do_preys=0)

        return obs
