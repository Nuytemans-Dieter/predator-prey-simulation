from random import randrange
from time import sleep

import gym
import gym_predatorprey
import gym_prey

from EnvironmentSimulator import EnvironmentSimulator
from visuals.plotter import Plotter
from visuals.renderer import Renderer

import json

if __name__ == '__main__':

    # Read configuration file.
    with open('config.JSON') as config_file:
        config = json.load(config_file)

    # Read configuration parameters.
    start_num_hunters = config['start_num_hunters']
    start_num_preys = config['start_num_preys']

    print('Starting simulation...')

    env = EnvironmentSimulator(config)
    renderer = Renderer(env, config)

    test = gym.make('prey-v0', config=config)

    # Populate the environment
    i = 0
    while i < max(start_num_hunters, start_num_preys):
        if i < start_num_hunters:
            env.spawn_hunter()
        if i < start_num_preys:
            env.spawn_prey()
        i += 1

    time = 0
    while env.get_num_hunters() > 0 and env.get_num_preys() > 0:
        # env.simulate_step()

        # Perform random movements/actions
        for hunter in env.hunterModel.agents:
            hunter.do_action( randrange(0, 5) )
        for prey in env.preyModel.agents:
            prey.do_action( randrange(0, 4) )

        # Execute the result of these actions
        for hunter in env.hunterModel.agents:
            hunter.finish_action()
        for prey in env.preyModel.agents:
            prey.finish_action()

        # Gather step data
        env.num_hunter_data.append( env.hunterModel.get_num_agents() )
        env.num_prey_data.append( env.preyModel.get_num_agents() )
        print('\nTime step ' + str(env.time) )
        print('Num preys: ' + str(env.num_prey_data[-1]) )
        print('Num hunters: ' + str(env.num_hunter_data[-1]) )

        env.time += 1
        time += 1
        renderer.render_state()
        sleep(1)

    print("\nBirth statistics")
    print("Born preys: " + str(env.preys_born))
    print("Born hunters: " + str(env.hunters_born))

    print("\nPrey deaths")
    print("By age: " + str(env.prey_deaths_by_age))
    print("By eaten: " + str(env.prey_deaths_by_eaten))
    print("Hunter deaths")
    print("By age: " + str(env.hunter_deaths_by_age))
    print("By energy: " + str(env.hunter_deaths_by_energy))

    plotter = Plotter()
    plotter.drawPlot(env.num_prey_data, env.num_hunter_data)
