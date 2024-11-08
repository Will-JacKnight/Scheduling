import pandas as pd

from src.algorithm import LCL
from data.graph import DAG


# data input, change data here
df = pd.read_excel("data/data.xlsx", usecols="A:D")
edges = [(0, 30), (1, 0), (2, 7), (3, 2), (4, 1),
        (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
        (10, 0), (11, 4), (12, 11), (13, 12), (16, 14),
        (14, 10), (15, 4), (16, 15), (17, 16), (18, 17),
        (19, 18), (20, 17), (21, 20), (22, 21), (23, 4),
        (24, 23), (25, 24), (26, 25), (27, 25), (28, 26),
        (28, 27), (29, 3), (29, 9), (29, 13), (29, 19),
        (29, 22), (29, 28)]
graph = DAG(node_num=31, edges=edges, dataframe=df)

# Question 1: utilising lcl to find the optimal solution for 1|prec|g*max problem
algo = LCL(graph=graph)
algo.find_schedule(printEachIteration=True)         # control the output of printing iteration data by setting the boolean
S = algo.schedule

print("-----------------------------------------------------")
print("The sorted best schedule for 1|prec|g*max problem is:")
print(f"S = {[int(S[i]) for i in range(len(S))]}")


# Question 2: tabu search for approximate optimal solution for 1|prec|sum_Tj problem

