import pandas as pd
import numpy as np


class Node:
    def __init__(self, index, type_of_node, processing_time, due_date) -> None:
        self.index = index;
        self.type_of_node = type_of_node;
        self.processing_time = processing_time;
        self.due_date = due_date;
    def __repr__(self):
        return f"Node(Index: {self.index}, Type: {self.type_of_node}, Processing Time: {self.processing_time}, Due Date: {self.due_date})"

## import incidence matrix of DAG
G_matrix = np.zeros([31,31], dtype=int)
link_pairs = [(0, 30), (1, 0), (2, 7), (3, 2), (4, 1),
              (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
              (10, 0), (11, 4), (12, 11), (13, 12), (16, 14),
              (14, 10), (15, 4), (16, 15), (17, 16), (18, 17),
              (19, 18), (20, 17), (21, 20), (22, 21), (23, 4),
              (24, 23), (25, 24), (26, 25), (27, 25), (28, 26),
              (28, 27), (29, 3), (29, 9), (29, 13), (29, 19),
              (29, 22), (29, 28)]
for row, col in link_pairs:
    G_matrix[row, col] = 1
print(G_matrix)

## import node data
df = pd.read_excel("data/data.xlsx", usecols="A:D")
nodes = [Node(row['Index'], row['Type'], row['Processing Time'], row['Due Date']) for _, row in df.iterrows()]
# for node in nodes:
#     print(node)


