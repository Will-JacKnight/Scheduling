import pandas as pd

from src.algorithm import LCL
from src.algorithm import TabuSearch
from data.graph import DAG


# input data, change data here
df = pd.read_excel("data/data.xlsx", usecols="A:D")
edges = [(0, 30), (1, 0), (2, 7), (3, 2), (4, 1),
        (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
        (10, 0), (11, 4), (12, 11), (13, 12), (16, 14),
        (14, 10), (15, 4), (16, 15), (17, 16), (18, 17),
        (19, 18), (20, 17), (21, 20), (22, 21), (23, 4),
        (24, 23), (25, 24), (26, 25), (27, 25), (28, 26),
        (28, 27), (29, 3), (29, 9), (29, 13), (29, 19),
        (29, 22), (29, 28)]
graph = DAG(node_num=31, edges=edges, node_data=df)


# Question 1: utilising lcl to find the optimal solution for 1|prec|g*max problem
algo = LCL(graph=graph)
algo.find_schedule(printEachIteration=True)
S = algo.schedule

print("-----------------------------------------------------")
print("The sorted best schedule for 1|prec|g*max problem is:")
print(f"S = {[int(S[i]) for i in range(len(S))]}\n")


# Question 2: tabu search for approximate optimal solution for 1|prec|sum_Tj problem
initial_solution = [30, 29, 23, 10, 9, 14, 13, 12, 4, 20, 22, 3, 27, 28, 8, 7, 19, 21, 26, 18, 25, 17, 15, 6, 24, 16, 5, 11, 2, 1, 31]
algo = TabuSearch(graph=graph)
# try with different numbers of K (10, 100, 1000)
algo.minimizer(L=20, K=10, gamma=10, initial_schedule=initial_solution)
algo.minimizer(L=20, K=100, gamma=10, initial_schedule=initial_solution)
algo.minimizer(L=20, K=1000, gamma=10, initial_schedule=initial_solution)

