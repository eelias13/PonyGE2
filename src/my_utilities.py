import subprocess



seed = 0
controller_cmd = ["--nstates", "1", "--s0", "0", "--rwm0", "1"]


import numpy as np
 
def transform_from_dict(input: dict, swarm_size: int) -> list:
    all_pos = []
    for i in range(len(input[f"bot0_x"])):
        swarm_pos = [] 
        for id in range(swarm_size):
            x = input[f"bot{id}_x"][i]
            y = input[f"bot{id}_y"][i]
            swarm_pos.append([x,y])
        all_pos.append(np.array(swarm_pos))
    return all_pos

def run_experiment(controller_cmd: list[str], seed: int, swarm_size: int, automode_exe: str, scenario: str) -> list:
    args = [automode_exe, "-n", "-c", scenario, "--seed", str(seed), "--fsm-config"]
    args.extend(controller_cmd)

    p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    output = stdout.decode('utf-8')

    robots_x = [[] for _ in range(swarm_size)]
    robots_y = [[] for _ in range(swarm_size)]
    for line in output.splitlines():
        if line[0:2] == "%!":
            args = {}
            for arg in line.split(" ")[1:]:
                key, val = arg.split(':')
                args[key] = float(val)
            robots_x[int(args["i"])].append(args["x"])
            robots_y[int(args["i"])].append(args["y"])

    # TODO: optimize this if to slow
    all_pos = []
    for bot_id in range(swarm_size):
        swarm_pos = [] 
        for time_step in range(len(robots_x)):
            x = robots_x[bot_id][time_step]
            y = robots_y[bot_id][time_step]
            swarm_pos.append([x,y])
        all_pos.append(np.array(swarm_pos))
    return all_pos


def get_real_bot_data(csv_path: str) -> dict:
    with open(csv_path, 'r') as f:
        line_it = iter(f.readlines())
        head = list(map(str.strip, next(line_it).split(",")))
        data = [[] for _ in range(len(head))]
        for line in line_it:
            line = list(map(str.strip, line.split(",")))
            for i, val in enumerate(line):
                data[i].append(float(val))
        
        result = {head[i]: data[i] for i in range(len(head))}
        return result
