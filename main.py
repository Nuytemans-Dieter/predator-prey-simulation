from EnvironmentSimulator import EnvironmentSimulator
from visuals.plotter import Plotter

if __name__ == '__main__':

    start_num_hunters = 25
    start_num_preys = 150

    print('Starting simulation...')

    env = EnvironmentSimulator()
    i = 0
    while i < max(start_num_hunters, start_num_preys):
        if i < start_num_hunters:
            env.spawn_hunter()
        if i < start_num_preys:
            env.spawn_prey()
        i += 1

    i = 0
    while env.get_num_hunters() > 0:
        env.simulate_step()
        i += 1

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
