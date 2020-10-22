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

    def move(self):
        raise NotImplementedError("Please Implement the move method for all Agents")
