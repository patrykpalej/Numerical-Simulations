import numpy as np


def remove_points_after_collision(points, v_matrix, m_vector):
    distances_matrix = np.linalg.norm(points[:, np.newaxis, :] - points[:, :, np.newaxis], axis=0)
    np.fill_diagonal(distances_matrix, THRESHOLD + 1)
    close_pairs = np.where(distances_matrix < THRESHOLD)
    unique_close_pairs = np.unique(np.sort(close_pairs, axis=0), axis=1)
    points_to_remove = np.unique(unique_close_pairs.flatten())

    cleaned_points = np.delete(points, points_to_remove, axis=1)
    cleaned_velocity = np.delete(v_matrix, points_to_remove, axis=1)
    cleaned_masses = np.delete(m_vector, points_to_remove)

    if points_to_remove.any():
        print("To remove:", points_to_remove)
        print("Dist matrix", distances_matrix)

    # return cleaned_points, cleaned_velocity, cleaned_masses
    return points, v_matrix, m_vector

