import random
import subprocess

import numpy

from fitness.base_ff_classes.base_ff import base_ff
from algorithm.parameters import params

path_to_AutoMoDe_executable = "/home/jkuckling/Documents/MasterThesis/2020_VincentVanPelt/AutoMoDe-BT/bin/automode_main_bt"


class ff_automode(base_ff):
    """
    Basic fitness function template for writing new fitness functions. This
    basic template inherits from the base fitness function class, which
    contains various checks and balances.

    Note that all fitness functions must be implemented as a class.

    Note that the class name must be the same as the file name.

    Important points to note about base fitness function class from which
    this template inherits:

      - Default Fitness values (can be referenced as "self.default_fitness")
        are set to NaN in the base class. While this can be over-written,
        PonyGE2 works best when it can filter solutions by NaN values.

      - The standard fitness objective of the base fitness function class is
        to minimise fitness. If the objective is to maximise fitness,
        this can be over-written by setting the flag "maximise = True".

    """

    # The base fitness function class is set up to minimise fitness.
    # However, if you wish to maximise fitness values, you only need to
    # change the "maximise" attribute here to True rather than False.
    # Note that if fitness is being minimised, it is not necessary to
    # re-define/overwrite the maximise attribute here, as it already exists
    # in the base fitness function class.
    maximise = True

    def __init__(self):
        """
        All fitness functions which inherit from the bass fitness function
        class must initialise the base class during their own initialisation.
        """

        # Initialise base fitness function class.
        super().__init__()

        # get the scenario file from the --target parameter
        self.scenario_file = params['TARGET']

        if not self.scenario_file:
            self.scenario_file = "/home/jkuckling/Documents/MasterThesis/2020_VincentVanPelt/Cedrata_extensions/missions/gianduja_stop_bt.argos"

    def evaluate(self, ind, **kwargs):
        """
        Default fitness execution call for all fitness functions. When
        implementing a new fitness function, this is where code should be added
        to evaluate target phenotypes.

        There is no need to implement a __call__() method for new fitness
        functions which inherit from the base class; the "evaluate()" function
        provided here allows for this. Implementing a __call__() method for new
        fitness functions will over-write the __call__() method in the base
        class, removing much of the functionality and use of the base class.

        :param ind: An individual to be evaluated.
        :param kwargs: Optional extra arguments.
        :return: The fitness of the evaluated individual.
        """

        # Evaluate the fitness of the phenotype
        # print(ind.phenotype)
        # TODO: Check if min < max for all parts of the tree
        # fitness = evaluate_controller("--nroot 3 --nchildroot 1 --n0 0 --nchild0 2 --n00 6 --c00 5 --p00 0.26 --n01 5 --a01 1 --p01 0".split(" "), "/home/jkuckling/Documents/MasterThesis/2020_VincentVanPelt/Cedrata_extensions/missions/foraging_bt.argos")
        scores = evaluate_controller(ind.phenotype.split(" "), self.scenario_file)
        fitness = numpy.mean(scores)
        # print(fitness)
        return fitness

def evaluate_controller(controller_cmd, scenario_file):
    # create 10 random seeds
    seeds = [random.randint(0, 2147483647) for _ in range(0, 10)]
    scores = []
    for seed in seeds:
        # prepare cmd
        args = [path_to_AutoMoDe_executable, "-n", "-c", scenario_file, "--seed", str(seed), "--bt-config"]
        args.extend(controller_cmd)
        # print(" ".join(args))
        p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        # Analyse result
        output = stdout.decode('utf-8')
        lines = output.splitlines()
        try:
            # print(lines[-1])
            score = float(lines[len(lines) - 1].split(" ")[1])
        except:
            score = -100  # Just to be sure
            # print("Args: " + str(args))
            # print("Stderr: " + stderr.decode('utf-8'))
            # print("Stdout: " + stdout.decode('utf-8'))
            # raise
        scores.append(score)
    return scores
