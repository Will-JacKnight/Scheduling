from src.algorithm import LCL
from data.graph import DAG

# utilising lcl to find the optimal solution for 1|prec|g*max problem
graph = DAG()
algo = LCL(graph=graph)
algo.find_schedule(printEachIteration=True)         # control the output of printing iteration data by setting the boolean
S = algo.schedule

print("-----------------------------------------------------")
print("The sorted best schedule for 1|prec|g*max problem is:")
print(f"S = {[int(S[i]) for i in range(len(S))]}")
