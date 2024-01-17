import numpy as np

DENSITY_RADIUS = 0.01


def fitness_function(sim_swarm_pos: list, real_swarm_pos: list) -> float:
    sim_swarm_metic = to_metic(sim_swarm_pos)
    real_swarm_metic = to_metic(real_swarm_pos)
    return dist(sim_swarm_metic, real_swarm_metic)

def to_metic(all_swarm_pos: list) -> list:
    """apples the swarm_metic function to all positions"""
    swarm_origen = all_swarm_pos[0]
    pre_swarm_pos = swarm_origen
    all_swarm_pos.remove(0)
    result = []
    for swarm_pos in all_swarm_pos:
        result.append(swarm_metic(swarm_pos, swarm_origen, pre_swarm_pos))
        pre_swarm_pos = swarm_pos
    return result

def swarm_metic(swarm_pos, swarm_origen, pre_swarm_pos) -> list:
    """calculates the 8 swarm mercies for a specific swarm position"""

    # 1-Center of mass is computed as the average overall agent locations in the x and the y direction.
    center_of_mass = np.mean(swarm_pos, axis=0)

    return {"center_of_mass": center_of_mass, 
            # 2-Maximum swarm shift is computed as the maximum distance moved among all agents measured at each time-step t.
            "max_swarm_shift": max_dist(swarm_pos, pre_swarm_pos), 
            "swarm_mode_index": swarm_mode_index(swarm_pos, center_of_mass), 
            # 4-Longest path is the maximum distance traveled from the origin among all agents.
            "longest_path":  max_dist(swarm_pos, swarm_origen),  
            # 5-Maximum radius is defined as the maximum distance among the distances between center of mass of the swarm and each agent.
            "max_radius":max_dist(swarm_pos, np.full(len(swarm_pos), center_of_mass)), 
            "local_density": local_density(swarm_pos, DENSITY_RADIUS), 
            "nears_neighbor_distance": nears_neighbor_distance(swarm_pos)}

def nears_neighbor_distance(swarm_pos: np.ndarray) -> float:
    """7-Average nearest neighbour distance is the sum of the distance to the nearest neighbour of each agent averaged over the total number of agents."""
    sum = 0
    for self_pos in swarm_pos:
        nn_dist = 0.0  
        for other_pos in swarm_pos:
            if other_pos == self_pos:
                continue
            if dist(self_pos, other_pos) < nn_dist:
                nn_dist = dist(self_pos, other_pos)
        sum += nn_dist
    return sum / len(swarm_pos)

def local_density(swarm_pos: np.ndarray, radius: float) -> float:
    """6-Average local density is the sum of the number of agents in the local radius r of each agent averaged over the total number of agents."""
    sum = 0
    for self_pos in swarm_pos:
        num_of_neighbor = 0  
        for other_pos in swarm_pos:
            if other_pos == self_pos:
                continue
            if dist(self_pos, other_pos) < radius:
                num_of_neighbor += 1
        sum += num_of_neighbor
    return sum / len(swarm_pos)


def dist(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """calculates the euclidean distance"""
    return  np.linalg.norm(vec1 - vec2)


def max_dist(swarm_pos1: np.ndarray, swarm_pos2: np.ndarray) -> float:
    """calculates the distance of all the points of swarm_pos1 and swarm_pos2 and returns the maximum"""
    max_dist = 0.0
    for (pos1, pos2) in zip(swarm_pos1, swarm_pos2):
        if dist(pos1, pos2) > max_dist:
            max_dist = dist(pos1, pos2)
    return max_dist
    
    #from itertools import starmap
    #return max(list(starmap(lambda pos1, pos2: np.linalg.norm(pos1 - pos2), zip(swarm_pos1, swarm_pos2))))


def swarm_mode_index(swarm_pos: np.ndarray, center_of_mass:np.ndarray) -> float:
    """3-Swarm mode index is used to measure the frequency of the swarm motion.

    It is computed as the distance between the center of mass and the swarm mode at each time-step t.

    The swarm mode is defined as a location in the x and the y direction with maximum frequency among all agent's locations. 
    
    The frequency of location l in the x or the y direction is computed using the following formula"""
    swarm_mode = find_swarm_mode(swarm_pos)
    swarm_mode_index = dist(center_of_mass, swarm_mode)
    return swarm_mode_index

def find_swarm_mode(swarm_pos: np.ndarray) -> float:
    flat_positions = swarm_pos.flatten()
    swarm_mode = np.argmax(np.bincount(flat_positions))
    swarm_mode = np.unravel_index(swarm_mode, swarm_pos.shape)
    return swarm_mode

