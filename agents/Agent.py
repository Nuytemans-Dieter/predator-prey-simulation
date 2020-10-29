from random import randrange


class Agent:

    def __init__(self, environment, location, max_age):

        self.age = 0
        self.location = (0, 0)
        self.max_age = 0

        self.environment = environment
        self.location = location
        self.max_age = max_age

    def get_random_move(self):
        direction = randrange(0, 4)

        if direction == 0:
            move = [0, 1]
        elif direction == 1:
            move = [0, -1]
        elif direction == 2:
            move = [1, 0]
        else:
            move = [-1, 0]

        out_of_upper = self.location[0] + move[0] >= self.environment.size_x or self.location[1] + move[1] >= self.environment.size_y
        out_of_lower = self.location[0] + move[0] < 0 or self.location[1] + move[1] < 0
        if out_of_upper or out_of_lower:
            move = (-1 * move[0], -1 * move[1])

        return move

    def get_move_from_action(self, direction):
        """Get the movement for a specific direction. 0: up, 1: down, 2: left, 3: right, other: nothing [0, 0]"""
        if direction == 0:
            move = [0, 1]
        elif direction == 1:
            move = [0, -1]
        elif direction == 2:
            move = [-1, 0]
        elif direction == 3:
            move = [1, 0]
        else:
            move = [0, 0]

        return move

    def add_location(self, add):
        return self.location[0] + add[0], self.location[1] + add[1]

    def do_action(self, action):
        raise NotImplementedError("Please Implement the do_action method for all Agents")

    def get_state(self):
        raise NotImplementedError("Please Implement the get_state method for all Agents")

    def get_actions(self):
        raise NotImplementedError("Please Implement the get_actions method for all Agents")

    def move(self):
        raise NotImplementedError("Please Implement the move method for all Agents")
