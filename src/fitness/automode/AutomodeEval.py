import subprocess
from fitness.base_ff_classes.base_ff import base_ff
from algorithm.parameters import params

CORRECT_CONTROLLER = "--nstates 4 --s0 5 --rep0 4.85 --n0 4 --n0x0 1 --c0x0 0 --p0x0 0.96 --n0x1 0 --c0x1 0 --p0x1 0.36 --n0x2 2 --c0x2 2 --p0x2 0.4 --n0x3 2 --c0x3 3 --p0x3 7 --w0x3 5.59 --s1 2 --n1 3 --n1x0 2 --c1x0 4 --p1x0 6 --w1x0 19.16 --n1x1 1 --c1x1 3 --p1x1 10 --w1x1 7.73 --n1x2 1 --c1x2 4 --p1x2 7 --w1x2 6.72 --s2 3 --n2 3 --n2x0 0 --c2x0 0 --p2x0 0.17 --n2x1 1 --c2x1 2 --p2x1 0.65 --n2x2 2 --c2x2 4 --p2x2 9 --w2x2 5.19 --s3 0 --rwm3 61 --n3 2 --n3x0 0 --c3x0 0 --p3x0 0.83 --n3x1 2 --c3x1 4 --p3x1 4 --w3x1 14.54".split(" ")

class AutomodeEval(base_ff):
    maximise = False

    def __init__(self):
        super().__init__()
        self.eval_bin = params['TARGET']
        
    def evaluate(self, ind, **kwargs):
        controller = ind.phenotype.split(" ")
        args = [ self.eval_bin, "--eval-controller" ]

        args.extend(controller)
        p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        fitness = stdout.decode('utf-8')
        try:
            fitness = float(fitness)
        except:
            fitness = 1000000
        return fitness
