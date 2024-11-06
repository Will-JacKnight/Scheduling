import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from data.graph import DAG


class LCL:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.schedule = []
        # initialise with total completion time
        self.completion_time_j = np.sum([self.graph.nodes[i].processing_time for i in range(self.graph.node_num)])
        self.iteration = 0
    
    def cost_function(self, j):
        dj = self.graph.nodes[j].due_date
        Cj = self.completion_time_j
        gj_Cj = np.max([0, Cj - dj])

        self.completion_time_j -= self.graph.nodes[j].processing_time
        return gj_Cj
    
    def find_schedule(self):
        for self.iteration in range(self.graph.node_num):
            gj_list = [self.cost_function(node_index) for node_index in self.graph.V]
            min_index = np.min(gj_list)
            print(self.graph.V)
            np.insert(self.schedule, 0, min_index + 1)          # +1 to convert the index to normal readable format, insert to the front of the schedule list
            self.graph.pop_node(min_index)                      # pop out the node with least cost


# algorithim local testing
graph = DAG()
algo = LCL(graph=graph)
algo.find_schedule()
print(algo.schedule)