import pandas as pd
import numpy as np


class Node:
    '''
    Represents a node used in, for example, a Directed Acyclic Graph.

    Args:
        index (int): Index of node.
        type_of_node (str): Type of node.
        processing_time (int): Processing time of node.
        due_date (int): Due date of node.
    '''
    def __init__(self, index: int, type_of_node: str, processing_time: int, due_date: int) -> None:
        self.index = index
        self.type_of_node = type_of_node
        self.processing_time = processing_time
        self.due_date = due_date
        
    def __repr__(self):
        return f"Node(Index: {self.index}, Type: {self.type_of_node}, Processing Time: {self.processing_time}, Due Date: {self.due_date})"


class DAG:
    '''
    Represents a Directed Acyclic Graph (DAG) where nodes and edges are defined
    based on input data using a adjacency matrix. 
    This class includes methods for initializing the graph, tracking outgoing and ingoing edges, and dynamically updating "last" and "first" nodes
    (nodes with no outgoing or ingoing edges, respectively).

    Args:
        node_num (int): Number of nodes in the DAG.
        node_data (pd.DataFrame): Dataframe containing node data (index, type, processing time, and due date)
    '''
    def __init__(self, node_num: int, edges: list, node_data: pd.DataFrame) -> None:
        # define edges
        self.node_num = node_num
        self.edges = edges
        # create adjacency matrix 
        self.G_matrix = np.zeros([self.node_num, self.node_num], dtype=int)
        for row, col in edges:
            self.G_matrix[row, col] = 1
        # print(self.G_matrix)

        # define nodes
        self.nodes = {}
        for _, row in node_data.iterrows():
            self.nodes[row['Index'] - 1] = Node(row['Index'], row['Type'], row['Processing Time'], row['Due Date'])
            # print(self.nodes[row['Index']])

        # V stores all current last nodes (no predecessors)
        self.V = [i for i in range(self.node_num) if np.sum(self.G_matrix[i]) == 0]
        # calculate amount of outgoing edges for each node
        self.outgoing_counts = [np.sum(self.G_matrix[i]) for i in range(self.node_num)]
        # calculate amount of ingoing edges for each node
        self.ingoing_counts = np.sum(self.G_matrix, axis=0)
        # print(self.ingoing_counts)

        # get first nodes (no successors)
        self.V_first_nodes = []
        for col in range(self.node_num):
            if all(self.G_matrix[row][col] == 0 for row in range(self.node_num)):
                self.V_first_nodes.append(col)

    def pop_node(self, node_index: int, node_type: str="last"):
        '''
        Pop the passed-in node and mutate list with first or last nodes indeces (starts from 0) 

        Args:
            node_index (int): Index of node.
            node_type (str): Type of nodes to consider whereas "last" is default 
                             ("first" for nodes with no incoming edges, 
                             "last" for nodes with no outgoing edges).
        '''      
        # # copy current matrix to prevent modifying original matrix
        # edge_matrix = self.G_matrix.copy()

        # check validity of node index
        if node_type == "first":
            if node_index not in self.V_first_nodes:
                return
            else:
                # pop passed-in node  
                self.V_first_nodes.remove(node_index)

        if node_type == "last":
            if node_index not in self.V:
                return
            else:
                # pop passed-in node   
                self.V.remove(node_index)
        
        if node_type == "first":
            # update ingoing edge counts and adjacency matrix for affected nodes
            for i in range(self.node_num):
                if self.G_matrix[i][node_index] != 0:
                    self.ingoing_counts[i] -= 1
                    # remove edge
                    self.G_matrix[i][node_index] = 0
                    
                    # add nodes without predecessors to list if not in list
                    if self.ingoing_counts[i] == 0 and i not in self.V_first_nodes:
                        self.V_first_nodes.append(i)

        if node_type == "last":
            # update outgoing edge counts and adjacency matrix for affected nodes
            for i in range(self.node_num):
                if self.G_matrix[i][node_index] != 0:
                    self.outgoing_counts[i] -= 1
                    # remove edge
                    self.G_matrix[i][node_index] = 0
                    
                    # add nodes without predecessors to list if not in V
                    if self.outgoing_counts[i] == 0 and i not in self.V:
                        self.V.append(i)
    

    # def pop_first_nodes(self, node_index: int):
    #     edge_matrix = self.G_matrix               # create a copy to prevent messing up with the original matrix

    #     # pop passed-in node 
    #     if node_index in self.V_first_nodes:

    #     # pop passed-in node   
    #     self.V_first_nodes.remove(node_index)

    #     # update ingoing edge counts and adjacency matrix for affected nodes
    #     for i in range(self.node_num):
    #         if edge_matrix[node_index][i] != 0:
    #             self.ingoing_counts[i] -= 1
    #             edge_matrix[node_index][i] = 0

    #             # add nodes without successors to list if not in list
    #             if self.ingoing_counts[i] == 0:
    #                 self.V_first_nodes.append(i)


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

# graph = DAG(node_num=31, edges=edges, node_data=df)
# print(graph.V_first_nodes)
# graph.pop_node(29, node_type = "first")
# print(graph.V_first_nodes)

# print(graph.nodes[30])
# print(len(graph.G_matrix))
# graph.pop_node(np.int64(30))
# print(graph.V)
# graph.pop_node(np.int64(0))
# print(graph.V)


