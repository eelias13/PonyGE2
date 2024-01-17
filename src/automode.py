import random
import numpy as np

from fitness.base_ff_classes.base_ff import base_ff
from fitness_function import to_metic
from my_utilities import get_real_bot_data, transform_from_dict, run_experiment

AUTOMODE_EXE = "/home/elias/code/cps-seminar/libs/AutoMoDe/bin/automode_main"
SCENARIO = "/home/elias/code/cps-seminar/data/generated/mission_29/mission_29_fsm_local.argos"
EXPERIMENT_CSV = "/home/elias/code/cps-seminar/data/chocolate-bag-epuck-positions/all_bot_pos.csv"

SWARM_SIZE = 15
EXPERIMENT_LEN = 1200
NUM_OF_SEEDS = 10
LOG_EVERY_X_EVOLUTIONS = 100

class ff_automode(base_ff):

    def __init__(self):
        super().__init__()

        data = get_real_bot_data(EXPERIMENT_CSV)
        data = transform_from_dict(data)
        if len(data) > EXPERIMENT_LEN:
            start = (len(data) - EXPERIMENT_LEN) / 2
            data = data[start:(start+EXPERIMENT_LEN)]
        self.real_swarm_metic = to_metic(data)

        self.evolution = 0

        
    def evaluate(self, ind, **kwargs):
        controller = ind.phenotype.split(" ")
        metics, seeds = evaluate_controller(controller)
        dists = []
        for metic in metics:
            dists.append(np.linalg.norm(metic - self.real_swarm_metic))
        self.evolution += 1

        if self.evolution % LOG_EVERY_X_EVOLUTIONS == 0:
            save_data(controller, metics, seeds, self.evolution)

        fitness = np.mean(np.array(dists))
        return fitness

def evaluate_controller(controller_cmd: list[str]) -> (list, list):
    # create 10 random seeds
    seeds = [random.randint(0, 2147483647) for _ in range(NUM_OF_SEEDS)]
    metics = []
    for seed in seeds:
       pos = run_experiment(controller_cmd, seed, SWARM_SIZE, AUTOMODE_EXE, SCENARIO)
       metic = to_metic(pos)
       metics.append(metic)
    return metics, seeds


def save_data(controller: list[str], metics: list, seeds: list[int], evolution: int):
    # TODO log to sqlite db
    print(controller, metics, seeds, evolution)