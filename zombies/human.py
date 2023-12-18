import numpy as np
from zombies.common import Character


class Human(Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n_killed = 0

    def calc_dist(self, zombie):
        return np.sqrt((self.x - zombie.x)**2 + (self.y - zombie.y)**2)

    def __repr__(self):
        return f"Human(x={round(self.x, 2)}, y={round(self.y, 2)}, velo={self.velocity}," \
               f" power={self.power}, n_killed={self.n_killed})"

    def choose_new_position(self, zombies):
        vectors_to_zombies = [np.array([z.x - self.x, z.y - self.y]) for z in zombies]
        normalized_vectors = [vec / (np.linalg.norm(vec)+.000001) for vec in vectors_to_zombies]
        weighted_vectors = [vec * (self.power + self.n_killed - z.power - z.n_infected)
                            for vec, z in zip(normalized_vectors, zombies)]
        vectors_sum = sum(weighted_vectors)
        normalized_vectors_sum = vectors_sum / (np.linalg.norm(vectors_sum)+.001)

        delta_x, delta_y = normalized_vectors_sum * self.velocity
        return delta_x, delta_y
