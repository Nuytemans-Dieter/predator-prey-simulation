from agents.Agent import Agent


class Hunter(Agent):

    smell_distance = 2

    def __init__(self, environment, energy, location, max_age, energy_to_reproduce, energy_per_prey_eaten):
        super().__init__(environment, location, max_age)
        self.energy = energy
        self.energy_to_reproduce = energy_to_reproduce
        self.energy_per_prey_eaten = energy_per_prey_eaten

    def move(self):
        move = self.get_random_move()
        self.location = ( self.location[0] + move[0], self.location[1] + move[1] )

        # Look for preys at this location and eat them
        preys = self.environment.get_preys_near(location=self.location, distanceSquared=self.smell_distance)
        if preys.__len__() != 0:

            nearestPrey = preys[0]
            nearestDistance = self.environment.get_distance_squared(self.location, preys[0].location)
            for prey in preys:
                distToPrey = self.environment.get_distance_squared(self.location, preys[0].location)
                if distToPrey < nearestDistance:
                    nearestPrey = prey
                    nearestDistance = distToPrey

            self.energy += self.energy_per_prey_eaten
            self.environment.kill_prey( nearestPrey )
            self.environment.prey_deaths_by_eaten += 1

        # Check reproduction chance and spawn new
        if self.energy >= self.energy_to_reproduce:
            self.environment.spawn_hunter()
            self.environment.hunters_born += 1

        # Check if max age is reached -> die
        # Check nog enough energy -> die
        if self.age > self.max_age or self.energy <= 0:
            self.environment.kill_hunter(self)
            if self.energy <= 0:
                self.environment.hunter_deaths_by_energy += 1
            else:
                self.environment.hunter_deaths_by_age += 1
