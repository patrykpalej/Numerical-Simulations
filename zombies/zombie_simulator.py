import numpy as np
from zombies.human import Human
from zombies.zombie import Zombie


class ZombieSimulator:
    def __init__(self, config):
        self.humans = []
        self.zombies = []

        for _ in range(config["n_humans"]):
            x = np.random.normal(*config["human_x"])
            y = np.random.normal(*config["human_y"])
            velocity = np.random.normal(*config["human_v"])
            power = np.random.normal(*config["human_power"])

            single_human = Human(x=x, y=y, velocity=velocity, power=power)
            self.humans.append(single_human)

        for _ in range(config["n_zombies"]):
            x = np.random.normal(*config["zombie_x"])
            y = np.random.normal(*config["zombie_y"])
            velocity = np.random.normal(*config["zombie_v"])
            power = np.random.normal(*config["zombie_power"])

            single_zombie = Zombie(x=x, y=y, velocity=velocity, power=power)
            self.zombies.append(single_zombie)

        self.map2d = np.zeros([100, 100])
        self.t = 0
        self.simulation_speed = config["simulation_speed"]

    def run_single_iteration(self):
        humans_displacements = []
        for human in self.humans:
            delta_x, delta_y = human.choose_new_position(self.zombies)
            humans_displacements.append((delta_x, delta_y))

        zombies_displacements = []
        for zombie in self.zombies:
            delta_x, delta_y = zombie.choose_new_position(self.humans)
            zombies_displacements.append((delta_x, delta_y))

        # Move
        for human, displacement in zip(self.humans, humans_displacements):
            human.move(*displacement)

        for zombie, displacement in zip(self.zombies, zombies_displacements):
            zombie.move(*displacement)

        # Fight
        clashing_pairs = self.find_all_pairs_about_to_clash()
        rivals_number = self.calculate_n_of_rivals(clashing_pairs)
        victories, loosers = self.carry_out_clashes(clashing_pairs, rivals_number)
        self.implement_results(victories, loosers)

    def find_all_pairs_about_to_clash(self, limit_distance=3):
        clashing_pairs = []
        for h, human in enumerate(self.humans):
            for z, zombie in enumerate(self.zombies):
                if np.sqrt((human.x - zombie.x) ** 2 + (human.y - zombie.y) ** 2) < limit_distance:
                    clashing_pairs.append((h, z))
        return clashing_pairs

    def calculate_n_of_rivals(self, clashing_pairs):
        rivals_number = {"humans": [0 for _ in self.humans], "zombies": [0 for _ in self.zombies]}

        for h, z in clashing_pairs:
            rivals_number["humans"][h] += 1
            rivals_number["zombies"][z] += 1

        return rivals_number

    def carry_out_clashes(self, clashing_pairs, rivals_number):
        victories = {"humans": [0 for _ in self.humans], "zombies": [0 for _ in self.zombies]}
        loosers = {"humans": [], "zombies": []}
        for h, z in clashing_pairs:
            result = np.sign(
                (self.humans[h].power + self.humans[h].n_killed) / rivals_number["humans"][h] -
                (self.zombies[z].power + self.zombies[z].n_infected) / rivals_number["zombies"][z])

            if result == 1:
                victories["humans"][h] += 1
                loosers["zombies"].append(z)
            else:
                victories["zombies"][z] += 1
                loosers["humans"].append(h)

        return victories, loosers

    def implement_results(self, victories, loosers):
        # Increase n_killed and n_infected
        for human, human_result in zip(self.humans, victories["humans"]):
            human.n_killed += human_result

        for zombie, zombie_result in zip(self.zombies, victories["zombies"]):
            zombie.n_infected += zombie_result

        # Remove killed zombies and turn infected humans into zombies
        killed_zombies = list(set(loosers["zombies"]))
        killed_zombies.sort(reverse=True)

        for zombie_index in killed_zombies:
            self.zombies.pop(zombie_index)

        # ---
        infected_humans = list(set(loosers["humans"]))
        infected_humans.sort(reverse=True)

        for human_index in infected_humans:
            h = self.humans[human_index]
            self.humans.pop(human_index)
            self.zombies.append(Zombie(x=h.x, y=h.y, velocity=h.velocity, power=h.power))
