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
    def __init__(self, node_num, edges, dataframe) -> None:
        # define edges
        self.node_num = node_num
        self.G_matrix = np.zeros([self.node_num, self.node_num], dtype=int)
        for row, col in edges:
            self.G_matrix[row, col] = 1
        print(self.G_matrix)

        # load from data.xlsx, and define nodes
        self.nodes = {}
        
        for _, row in dataframe.iterrows():
            self.nodes[row['Index'] - 1] = Node(row['Index'], row['Type'], row['Processing Time'], row['Due Date'])
            # print(self.nodes[row['Index']])

        self.V = [i for i in range(self.node_num) if np.sum(self.G_matrix[i]) == 0]         # V_ist stores all current last nodes
        self.outgoing_counts = [np.sum(self.G_matrix[i]) for i in range(self.node_num)]     # calculate outgoing edges


        self.ingoing_counts = np.sum(self.G_matrix, axis=0)     # sum the columns
        print(self.ingoing_counts)

        self.V_first_nodes = []
        for col in range(self.node_num):
            if all(self.G_matrix[row][col] == 0 for row in range(self.node_num)):
                self.V_first_nodes.append(col)                                                  # initialise with first nodes


    def pop_last_nodes(self, node_index):         # popped the passed in node, and return the list of new last nodes index (starts from 0)       
        edge_matrix = self.G_matrix               # create a copy to prevent messing up with the original matrix

        if node_index in self.V:
            self.V.remove(node_index)               # pop out the old last node

        for i in range(self.node_num):
            if edge_matrix[i][node_index] != 0:
                self.outgoing_counts[i] -= 1
                edge_matrix[i][node_index] = 0        # remove this edge
                
                if self.outgoing_counts[i] == 0:
                    self.V.append(i)                   # row as the end node index
    

    def pop_first_nodes(self, node_index):
        edge_matrix = self.G_matrix               # create a copy to prevent messing up with the original matrix

        if node_index in self.V_first_nodes:
            self.V_first_nodes.remove(node_index)       # pop out the old first node

        for i in range(self.node_num):
            if edge_matrix[node_index][i] != 0:
                self.ingoing_counts[i] -= 1
                edge_matrix[node_index][i] = 0
            
                if self.ingoing_counts[i] == 0:
                    self.V_first_nodes.append(i)


# single file testing
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
print(graph.V_first_nodes)
graph.pop_first_nodes(29)
print(graph.V_first_nodes)

# print(graph.nodes[30])
# print(len(graph.G_matrix))
# graph.pop_node(np.int64(30))
# print(graph.V)
# graph.pop_node(np.int64(0))
# print(graph.V)


