from src.algorithm import LCL
from data.graph import DAG

# utilising lcl to find the optimal solution for 1|prec|g*max problem
graph = DAG()
algo = LCL(graph=graph)
algo.find_schedule()

S = algo.schedule
print([int(S[i]) for i in range(len(S))])