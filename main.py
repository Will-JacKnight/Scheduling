from src.algorithm import LCL
from data.graph import DAG

# utilising lcl to find the optimal solution for 1|prec|g*max problem
graph = DAG()
algo = LCL(graph=graph)

S = algo.find_schedule()
print(S)