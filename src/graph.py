import pandas as pd
import numpy as np


class Node:
    '''
    Represents a node used in, for example, a Directed Acyclic Graph.

    Args:
        index (int): Index of node (0 indexed).
        type_of_node (str): Type of node.
        processing_time (int): Processing time of node.
        due_date (int): Due date of node.
    '''
    def __init__(self, index: int, type_of_node: str, processing_time: int, due_date: int):
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
    This class includes methods for initializing the graph, tracking outgoing edges, 
    and dynamically updating "last" nodes (nodes with no outgoing edges).

    Args:
        node_num (int): Number of nodes in the DAG.
        node_data (pd.DataFrame): Dataframe containing node data (index, type, processing time, and due date).
                                  Indices are expected to be 1 indexed and converted to 0 indexing.
    '''
    def __init__(self, node_num: int, edges: list, node_data: pd.DataFrame):
        # define edges
        self.node_num = node_num
        self.edges = edges
        # create adjacency matrix 
        self.G_matrix = np.zeros([self.node_num, self.node_num], dtype=int)
        for row, col in edges:
            self.G_matrix[row, col] = 1

        # define nodes
        self.nodes = {}
        for _, row in node_data.iterrows():
            # convert node data from xlsx to 0 indexing (original data is 1 indexed)
            self.nodes[row['Index'] - 1] = Node(row['Index'], row['Type'], row['Processing Time'], row['Due Date'])

        # V stores all current last nodes (no predecessors)
        self.V = [i for i in range(self.node_num) if np.sum(self.G_matrix[i]) == 0]
        # calculate amount of outgoing edges for each node
        self.outgoing_counts = [np.sum(self.G_matrix[i]) for i in range(self.node_num)]

    def pop_node(self, node_index: int):
        '''
        Pop the passed-in node and mutate list with last nodes indices (no outgoing edges) 

        Args:
            node_index (int): Index of node.
        '''      
        if node_index not in self.V:
            return
        else:
            # pop passed-in node   
            self.V.remove(node_index)

        # update outgoing edge counts and adjacency matrix for affected nodes
        for i in range(self.node_num):
            if self.G_matrix[i][node_index] != 0:
                self.outgoing_counts[i] -= 1
                # remove edge
                self.G_matrix[i][node_index] = 0
                
                # add nodes without predecessors to list if not in V
                if self.outgoing_counts[i] == 0 and i not in self.V:
                    self.V.append(i)