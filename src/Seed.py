import numpy as np


class Seed:

    def __init__(self, loc):
        self.loc = loc

    def monte_carlo_location(self):
        act = np.random.randint(1, 4)
        x = self.loc[0]
        y = self.loc[1]
        if act == 1:
            x += 1
        elif act == 2:
            y += 1
        elif act == 3:
            x -= 1
        else:
            y -= 1
        return (x,y)

    def get_next_loc(self):
        new_loc = self.monte_carlo_location()

        return self.loc
