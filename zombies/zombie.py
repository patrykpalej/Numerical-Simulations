import numpy as np
from zombies.common import Character


class Zombie(Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n_infected = 0

    def __repr__(self):
        return f"Zombie(x={round(self.x, 2)}, y={round(self.y, 2)}, velo={self.velocity}, power={self.power}, n_inf={self.n_infected})"

    def choose_new_position(self, humans):
        vectors_to_humans = [np.array([h.x - self.x, h.y - self.y]) for h in humans]
        normalized_vectors = [vec / (np.linalg.norm(vec)+.001) for vec in vectors_to_humans]
        weighted_vectors = [vec * (self.power + self.n_infected - h.power - h.n_killed)
                            for vec, h in zip(normalized_vectors, humans)]
        vectors_sum = sum(weighted_vectors)
        normalized_vectors_sum = vectors_sum / (np.linalg.norm(vectors_sum)+.001)

        delta_x, delta_y = normalized_vectors_sum * self.velocity
        return delta_x, delta_y
