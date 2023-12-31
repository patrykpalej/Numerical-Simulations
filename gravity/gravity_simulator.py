import json
import time
import numpy as np
from datetime import datetime


class GravitySimulator:
    G: float = 1e-4  # gravity constant
    REFERENCE_DELTA_T: float = 0.1  # default time step
    PROXIMITY_THRESHOLD = 0.03  # collision distance, may be interpreted as diameter of a planet

    def __init__(self, show_points: bool, show_field: bool, show_trajectory: bool, save_logs: bool,
                 on_collision: str, time_speed: int, initial_x: np.array, initial_y: np.array,
                 mass_vector: np.array, initial_vx: np.array, initial_vy: np.array):
        self.counter = 0
        self.map_length = 100  # resolution of gravity heatmap

        self.show_points = show_points
        self.show_field = show_field
        self.show_trajectory = show_trajectory
        self.save_logs = save_logs
        self.on_collision = on_collision
        self.time_speed = time_speed
        self.x = initial_x
        self.y = initial_y
        self.m = mass_vector
        self.vx = initial_vx
        self.vy = initial_vy

        self.is_frozen = np.full((len(mass_vector),), False)
        self.is_annihilited = np.full((len(mass_vector),), False)

        self.x_history = np.empty([0, len(mass_vector)])
        self.y_history = np.empty([0, len(mass_vector)])
        self.vx_history = np.empty([0, len(mass_vector)])
        self.vy_history = np.empty([0, len(mass_vector)])
        self.m_history = np.empty([0, len(mass_vector)])
        self.delta_t_history = np.array([])
        self.sleep_time_history = np.array([])

        self._update_history_of_location_and_velocity()

    @property
    def _max_v_value(self):
        return max([np.linalg.norm([vx_, vy_]) for vx_, vy_ in zip(self.vx, self.vy)])

    @property
    def _delta_t(self):
        """Too fast planets will not be able to appear in their collision zones
           Therefore delta_t must be less than distance_threshold / (v_max + eps) (in case of v=0)
        """
        return 0.5 * self.PROXIMITY_THRESHOLD / (self._max_v_value + 1e-2)

    @property
    def _sleep_time(self):
        adjustment = self._delta_t / self.REFERENCE_DELTA_T
        return 0.2 * adjustment / self.time_speed

    def _update_history_of_location_and_velocity(self):
        """
        Updating during init and after each iteration. For N iterations history has N+1 elements
        """
        try:
            self.x_history = np.append(self.x_history, [self.x], axis=0)
            self.y_history = np.append(self.y_history, [self.y], axis=0)
            self.vx_history = np.append(self.vx_history, [self.vx], axis=0)
            self.vy_history = np.append(self.vy_history, [self.vy], axis=0)
            self.m_history = np.append(self.m_history, [self.m], axis=0)
        except ValueError:
            length = self.m_history.shape[1]
            self.x_history = np.append(self.x_history,
                                       [np.pad(self.x, (0, length - len(self.x)),
                                               'constant')], axis=0)
            self.y_history = np.append(self.y_history,
                                       [np.pad(self.y, (0, length - len(self.y)),
                                               'constant')], axis=0)

            self.vx_history = np.append(self.vx_history,
                                        [np.pad(self.vx, (0, length - len(self.vx)),
                                                'constant')], axis=0)
            self.vy_history = np.append(self.vy_history,
                                        [np.pad(self.vy, (0, length - len(self.vy)),
                                                'constant')], axis=0)
            self.m_history = np.append(self.m_history,
                                       [np.pad(self.m, (0, length - len(self.m)),
                                               'constant')], axis=0)

    def _update_history_of_time(self):
        """
        Updating only after each iteration. For N iterations history has N elements
        """
        self.delta_t_history = np.append(self.delta_t_history, self._delta_t)
        self.sleep_time_history = np.append(self.sleep_time_history, self._sleep_time)

    def _calculate_a_matrix(self):
        """
        Calculates matrix of a_x, a_y with shape of [2, N]
        """
        locations_matrix = np.vstack([self.x, self.y])
        a_matrix = np.zeros_like(locations_matrix, dtype=float)

        for i in range(len(self.m)):
            p0 = locations_matrix[:, i]
            points = np.delete(locations_matrix, i, axis=1)
            masses = np.delete(self.m, i)
            distances = np.linalg.norm(points.T - p0, axis=1)
            xy_deltas = points.T - p0

            a_vector = np.sum(
                xy_deltas * masses.reshape(-1, 1) * self.G / distances.reshape(-1, 1) ** 3, axis=0)
            a_matrix[:, i] = a_vector

        return a_matrix

    def _calculate_v_matrix(self, a_matrix):
        """
        Calculates matrix of v_x, v_y with shape of [2, N]
        """
        v_matrix = np.vstack([self.vx, self.vy]) + a_matrix * self._delta_t
        v_matrix[:, self.is_frozen] = 0
        return v_matrix

    def _calculate_xy_matrix(self, v_matrix):
        """
        Calculates matrix of x, y with shape of [2, N]
        """
        return np.vstack([self.x, self.y]) + v_matrix * self._delta_t

    @property
    def gravitational_field(self):
        """
        Returns (100x100) matrix representing filed of gravitational potential
        """
        length = self.map_length
        field = np.zeros([length, length])
        x_coords, y_coords = np.meshgrid(np.arange(length, dtype=float),
                                         np.arange(length, dtype=float))
        x_coords = (x_coords - length / 2) / (length / 2)
        y_coords = (y_coords - length / 2) / (length / 2)

        for x, y, m in zip(self.x, self.y, self.m):
            distances = np.sqrt((x_coords - x) ** 2 + (y_coords - y) ** 2)
            distances[distances < self.PROXIMITY_THRESHOLD/2] = np.nan

            field += self.G * m / distances

        return field

    def find_close_pairs(self, points):
        distances_matrix = np.linalg.norm(points[:, np.newaxis, :] - points[:, :, np.newaxis],
                                          axis=0)
        np.fill_diagonal(distances_matrix, self.PROXIMITY_THRESHOLD + 1)
        close_pairs = np.where(distances_matrix < self.PROXIMITY_THRESHOLD)
        unique_close_pairs = np.unique(np.sort(close_pairs, axis=0), axis=1)
        return unique_close_pairs

    def simulate_one_iteration(self):
        """
        Calculates new: acceleration, velocity and location. Updates history
        """
        self._update_history_of_time()

        self.counter += 1
        time.sleep(self._sleep_time)

        a_matrix = self._calculate_a_matrix()
        v_matrix = self._calculate_v_matrix(a_matrix)
        xy_matrix = self._calculate_xy_matrix(v_matrix)

        self.x = xy_matrix[0]
        self.y = xy_matrix[1]

        self.vx = v_matrix[0]
        self.vy = v_matrix[1]

        close_pairs = self.find_close_pairs(xy_matrix)

        if self.on_collision == "Annihilate" and close_pairs.any():
            self._handle_annihilation(close_pairs)
        elif self.on_collision == "Freeze" and close_pairs.any():
            self._handle_freezing(close_pairs)
        elif self.on_collision == "Bounce" and close_pairs.any():
            self._handle_bouncing(close_pairs)

        self._update_history_of_location_and_velocity()

    def _handle_freezing(self, close_pairs):
        for p1, p2 in close_pairs.T:
            self.is_frozen[p1] = True
            self.is_frozen[p2] = True

    def _handle_bouncing(self, close_pairs):
        for p1, p2 in close_pairs.T:
            m1 = self.m[p1]
            m2 = self.m[p2]
            v1x, v1y = np.array([self.vx[p1], self.vy[p1]])
            v2x, v2y = np.array([self.vx[p2], self.vy[p2]])

            self.vx[p1], self.vy[p1] = m2/m1 * v2x, m2/m1 * v2y
            self.vx[p2], self.vy[p2] = m1/m2 * v1x, m1/m2 * v1y

    def _handle_annihilation(self, close_pairs):
        points_to_remove = np.unique(close_pairs.flatten())

        self.x = np.delete(self.x, points_to_remove)
        self.vx = np.delete(self.vx, points_to_remove)
        self.y = np.delete(self.y, points_to_remove)
        self.vy = np.delete(self.vy, points_to_remove)
        self.m = np.delete(self.m, points_to_remove)
        self.is_frozen = np.delete(self.is_frozen, points_to_remove)
        self.is_annihilited = np.delete(self.is_annihilited, points_to_remove)

    def dump_logs_to_file(self):
        results = {
            "x_history": self.x_history.tolist(),
            "y_history": self.y_history.tolist(),
            "vx_history": self.vx_history.tolist(),
            "vy_history": self.vy_history.tolist(),
            "m_history": self.m_history.tolist(),
            "delta_t_history": self.delta_t_history.tolist(),
            "sleep_time_history": self.sleep_time_history.tolist(),
        }
        filename = datetime.now().strftime("%H-%M")
        with open(f"gravity/logs/{filename}.json", "w") as f:
            json.dump(results, f, indent=4)
