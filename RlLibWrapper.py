import gym as gym


class RlLibWrapper(gym.Env):


    def __init__(self):
        print('Wrapper')
        # self.action_space = (num_agents, num_actions)
        # self.observation_space = (num_agents, 2)
        # self.simulator #referentie naar die simulator die je gebouwd hebt

    def reset(self):
        # Reset de simulator terug naar de startpositie
        print('Reset')


    def step(self, action):
        # voer een bepaalde actie uit voor elke prooi agent en verander de state van de prooi.
        # Voer de step methode van alle hunters uit
        # Geef de eventuele observaties en rewards van elk prooiterug
        #return <obs>, <reward: float>, <done: bool>
        return 0
