from agents.Agent import Agent


class Hunter(Agent):

    smell_distance = 2

    def __init__(self, environment, energy, location, max_age, energy_to_reproduce, energy_per_prey_eaten):
        super().__init__(environment, location, max_age)
        self.energy = energy
        self.energy_to_reproduce = energy_to_reproduce
        self.energy_per_prey_eaten = energy_per_prey_eaten

        self.doReproduce = False

    def do_action(self, action):
        """Make this agent do a specific action. 0: up, 1: down, 2: left, 3: right, 4: reproduce"""

        self.age += 1
        self.energy -= 1

        if action == 4:
            self.doReproduce = True
        else:
            move = self.get_move_from_action( action )
            self.location = ( self.location[0] + move[0], self.location[1] + move[1] )

    def finish_action(self):

        if self.doReproduce:

            self.doReproduce = False

            # Check reproduction rules and spawn new if allowed
            if self.energy >= self.energy_to_reproduce:
                self.environment.spawn_hunter()
                self.environment.hunters_born += 1

        prey = self.environment.get_nearest_prey(self.location)
        # If there is a near prey and the location matches that of the predator
        if prey != 0 and self.location[0] == prey.location[0] and self.location[1] == prey.location[1]:
            self.energy += self.energy_per_prey_eaten
            self.environment.kill_prey( prey )
            self.environment.prey_deaths_by_eaten += 1

        # Check if max age is reached -> die
        # Check nog enough energy -> die
        if self.age > self.max_age or self.energy <= 0:
            self.environment.kill_hunter(self)
            if self.energy <= 0:
                self.environment.hunter_deaths_by_energy += 1
            else:
                self.environment.hunter_deaths_by_age += 1

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

    def get_actions(self):
        return[[0, 1], [0, -1], [-1, 0], [1, 0], self.energy_to_reproduce >= self.energy]

    def get_state(self):
        closestLoc = self.environment.get_nearest_prey(self.location)
        if closestLoc == 0:
            closestX = self.environment.size_x
            closestY = self.environment.size_y
        else:
            closestX = closestLoc.location[0] - self.location[0]
            closestY = closestLoc.location[1] - self.location[1]
        return [self.age, self.energy, closestX, closestY]
