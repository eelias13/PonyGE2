
def node(id: int) -> str:
  result = ""
  result += f"""<node-{id}> ::= \
  <explore-{id}> | <stop-{id}> |<phototaxis-{id}> | <anti_phototaxis-{id}> | <attraction-{id}> | <repulsion-{id}>\n\n"""
  
  result += f"<explore-{id}>           ::= --s{id} 0 --rwm{id} <0-100>\n"
  result += f"<stop-{id}>              ::= --s{id} 1\n"
  result += f"<phototaxis-{id}>        ::= --s{id} 2\n"
  result += f"<anti_phototaxis-{id}>   ::= --s{id} 3\n"
  result += f"<attraction-{id}>        ::= --s{id} 4 --att{id} <0-5>\n"
  result += f"<repulsion-{id}>         ::= --s{id} 4 --rep{id} <0-5>\n\n\n"

  return result


def transition(from_id: int, num_id: int, nodes: int) -> str:
  result = f"""<transition-{from_id}-{num_id}> ::= \
  <black_floor-{from_id}-{num_id}> | <gray_floor-{from_id}-{num_id}> | <white_floor-{from_id}-{num_id}> | <fixed_potability-{from_id}-{num_id}> |\
  <light-{from_id}-{num_id}> | <neighbors_count-{from_id}-{num_id}>  | <inverted_neighbors_count-{from_id}-{num_id}> \n\n"""

  result += f"<black_floor-{from_id}-{num_id}>               ::= --n{from_id}x{num_id} <0-{nodes-1}> --c{from_id}x{num_id} 0 --p{from_id}x{num_id} <percent> \n"
  result += f"<gray_floor-{from_id}-{num_id}>                ::= --n{from_id}x{num_id} <0-{nodes-1}> --c{from_id}x{num_id} 1 --p{from_id}x{num_id} <percent> \n"
  result += f"<white_floor-{from_id}-{num_id}>               ::= --n{from_id}x{num_id} <0-{nodes-1}> --c{from_id}x{num_id} 2 --p{from_id}x{num_id} <percent> \n" 
  result += f"<neighbors_count-{from_id}-{num_id}>           ::= --n{from_id}x{num_id} <0-{nodes-1}> --c{from_id}x{num_id} 3 --p{from_id}x{num_id} <1-10_p> --w{from_id}x{num_id} <0-20_p> \n" 
  result += f"<inverted_neighbors_count-{from_id}-{num_id}>  ::= --n{from_id}x{num_id} <0-{nodes-1}> --c{from_id}x{num_id} 4 --p{from_id}x{num_id} <1-10_p> --w{from_id}x{num_id} <0-20_p> \n"
  result += f"<fixed_potability-{from_id}-{num_id}>          ::= --n{from_id}x{num_id} <0-{nodes-1}> --c{from_id}x{num_id} 5 --p{from_id}x{num_id} <percent> \n"
  result += f"<light-{from_id}-{num_id}>                     ::= --n{from_id}x{num_id} <0-{nodes-1}> --c{from_id}x{num_id} 6 --p{from_id}x{num_id} <percent> \n" 

  return result


def transitions(id: int, max_id: int) -> str:
  result = f"<transitions-{id}> ::= "

  for i in range(0,max_id):
    result += f"--n{id} {i+1} "
    for j in range(0,i+1):
      result += f" <transition-{id}-{j}> "
    if i != max_id -1:
      result += " | "

  return result

def int_range(start:int, end: int) -> str:
  result = f"<{start}-{end}> ::= "
  for i in range(start,end):
    result += f"{i}|"
  result += f"{end}\n"
  return result

def fsm(nodes:int):
  result = f"<FSM> ::= --fsm-config --nstates {nodes}"

  for i in range(0, nodes):
    result += f" <node-{i}> <transitions-{i}>"

  result += "\n\n\n\n"

  for i in range(0, nodes):
    result += node(i)

  for i in range(0, nodes):
    result += "\n\n"
    result += transitions(i, nodes)
  

  for i in range(0,nodes):
    for j in range(0,nodes):
      result += "\n\n"
      result += transition(j, i, nodes)

  result += "\n\n\n\n"
  result += "<percent>  ::= <0-1>.<0-99>\n"
  result += "<1-10_p>   ::= <1-10>.<0-99>\n"
  result += "<0-20_p>   ::= <0-20>.<0-99>\n\n"
  result += int_range(1,10)
  result += int_range(0,20)
  result += int_range(0,99)
  result += int_range(0,100)
  result += int_range(0,5)
  result += int_range(0,nodes-1)
  result += "<0-1>      ::= 0|1"

  return result


with open("automode_fsm.bnf","w") as f:
  f.write(fsm(4))



