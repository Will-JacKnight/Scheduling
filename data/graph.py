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


class DAG:
    def __init__(self) -> None:
        # define edges
        self.node_num = 31
        self.G_matrix = np.zeros([self.node_num, self.node_num], dtype=int)
        edges = [(0, 30), (1, 0), (2, 7), (3, 2), (4, 1),
              (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
              (10, 0), (11, 4), (12, 11), (13, 12), (16, 14),
              (14, 10), (15, 4), (16, 15), (17, 16), (18, 17),
              (19, 18), (20, 17), (21, 20), (22, 21), (23, 4),
              (24, 23), (25, 24), (26, 25), (27, 25), (28, 26),
              (28, 27), (29, 3), (29, 9), (29, 13), (29, 19),
              (29, 22), (29, 28)]
        for row, col in edges:
            self.G_matrix[row, col] = 1
        print(self.G_matrix)

        # load from data.xlsx, and define nodes
        self.nodes = {}
        df = pd.read_excel("data/data.xlsx", usecols="A:D")
        for _, row in df.iterrows():
            self.nodes[row['Index'] - 1] = Node(row['Index'], row['Type'], row['Processing Time'], row['Due Date'])
            # print(self.nodes[row['Index']])

        self.V = [i for i in range(self.node_num) if np.sum(self.G_matrix[i]) == 0]      # initialise with last node

    def pop_node(self, node_index):       # popped the passed in node, and return the list of new last nodes index (starts from 0)
        outgoing_counts = [np.sum(self.G_matrix[i]) for i in range(self.node_num)]  # calculate outgoing edges

        if node_index in self.V:
            self.V.remove(node_index)

        for i in range(self.node_num):
            if self.G_matrix[i][node_index] != 0:
                outgoing_counts[i] -= 1
                self.G_matrix[i][node_index] = 0        # remove this edge
                
                if outgoing_counts[i] == 0:
                    self.V.append(i)                   # row as the end node index


# testing
graph = DAG()
print(graph.nodes[30])
print(len(graph.G_matrix))
graph.pop_node(np.int64(30))
print(graph.V)
graph.pop_node(np.int64(0))
print(graph.V)


