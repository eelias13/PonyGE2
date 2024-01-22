import random
import numpy as np
import sqlite3

from fitness.base_ff_classes.base_ff import base_ff
from fitness.automode.fitness_function import to_metic
from fitness.automode.my_utilities import get_real_bot_data, transform_from_dict, run_experiment


AUTOMODE_EXE = "/home/elias/code/cps-seminar/libs/AutoMoDe/bin/automode_main"
SCENARIO = "/home/elias/code/cps-seminar/data/generated/mission_29/mission_29_fsm_local.argos"
EXPERIMENT_CSV = "/home/elias/code/cps-seminar/data/chocolate-bag-epuck-positions/all_bot_pos.csv"
DB_PATH = "data.db"

SWARM_SIZE = 15
EXPERIMENT_LEN = 1200
NUM_OF_SEEDS = 10
LOG_EVERY_X_EVOLUTIONS = 100

CORRECT_CONTROLLER = "--nstates 4 --s0 5 --rep0 4.85 --n0 4 --n0x0 1 --c0x0 0 --p0x0 0.96 --n0x1 0 --c0x1 0 --p0x1 0.36 --n0x2 2 --c0x2 2 --p0x2 0.4 --n0x3 2 --c0x3 3 --p0x3 7 --w0x3 5.59 --s1 2 --n1 3 --n1x0 2 --c1x0 4 --p1x0 6 --w1x0 19.16 --n1x1 1 --c1x1 3 --p1x1 10 --w1x1 7.73 --n1x2 1 --c1x2 4 --p1x2 7 --w1x2 6.72 --s2 3 --n2 3 --n2x0 0 --c2x0 0 --p2x0 0.17 --n2x1 1 --c2x1 2 --p2x1 0.65 --n2x2 2 --c2x2 4 --p2x2 9 --w2x2 5.19 --s3 0 --rwm3 61 --n3 2 --n3x0 0 --c3x0 0 --p3x0 0.83 --n3x1 2 --c3x1 4 --p3x1 4 --w3x1 14.54".split(" ")


class AutomodeEval(base_ff):
    maximise = False

    def __init__(self):
        super().__init__()

        con = sqlite3.connect(DB_PATH)
        self.cur = con.cursor()

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
        # self.evolution += 1

        # if self.evolution % LOG_EVERY_X_EVOLUTIONS == 0:
        #     save_data(controller, metics, seeds, self.evolution, self.cur)

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


def save_data(controller: list[str], metics: list, seeds: list[int], evolution: int, cur: sqlite3.Cursor):
    controller = " ".join(controller)
    metics = str(metics)
    seeds = str(seeds)
    evolution = str(evolution)
    cur.execute(f"INSERT INTO projects(controller, metics, seeds, evolution) VALUES({controller},{metics},{seeds},{evolution})")


## fitnis function
    




# def main():
#     con = sqlite3.connect(DB_PATH)
#     cur = con.cursor()
#     cur.execute("""CREATE TABLE IF NOT EXISTS movie(
#                     controller TEXT NOT NULL, 
#                     metics TEXT NOT NULL,
#                     seeds TEXT NOT NULL,
#                     evolution INTEGER NOT NULL)""")
#     metics, seeds = evaluate_controller(CORRECT_CONTROLLER)
#     save_data(CORRECT_CONTROLLER, metics, seeds, -1, cur)