import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from data.graph import DAG


class LCL:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.schedule = []
        # initialise with total completion time
        self.completion_time_j = np.sum([self.graph.nodes[i].processing_time for i in range(self.graph.node_num)])
        self.iteration = 0
    
    def cost_function(self, j) -> float:
        dj = self.graph.nodes[j].due_date
        Cj = self.completion_time_j
        gj_Cj = np.max([0, Cj - dj])

        self.completion_time_j -= self.graph.nodes[j].processing_time
        return gj_Cj
    
    def find_schedule(self, printEachIteration):
        for self.iteration in range(self.graph.node_num):
            gj_list = [self.cost_function(node_index) for node_index in self.graph.V]
            min_index = np.argmin(gj_list)
            # print(self.graph.V)
            self.schedule = np.insert(self.schedule, 0, self.graph.V[min_index] + 1)          # +1 to convert the index to normal readable format, insert to the front of the schedule list
            self.graph.pop_last_nodes(self.graph.V[min_index])                      # pop out the node with least cost

            if (printEachIteration):
                # print("-----------------------------------------------------")
                print(f"In iteration {self.iteration}: ")
                print(f"partial schedule S = {[int(self.schedule[i]) for i in range(len(self.schedule))]}")


class Tabu_Search:
    def __init__(self) -> None:

        df = pd.read_excel("data/data.xlsx", usecols="A:D")
        edges = [(0, 30), (1, 0), (2, 7), (3, 2), (4, 1),
        (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
        (10, 0), (11, 4), (12, 11), (13, 12), (16, 14),
        (14, 10), (15, 4), (16, 15), (17, 16), (18, 17),
        (19, 18), (20, 17), (21, 20), (22, 21), (23, 4),
        (24, 23), (25, 24), (26, 25), (27, 25), (28, 26),
        (28, 27), (29, 3), (29, 9), (29, 13), (29, 19),
        (29, 22), (29, 28)]

        self.graph = DAG(node_num=31, edges=edges, dataframe=df)
        self.schedule = []
        self.candidates = self.graph.V_first_nodes

    def generate_initial_candidates(self):          # need to take into account the DAG graph order
        # get V, pop oout rando
        
        for i in range(self.graph.node_num):
            if self.graph.V_first_nodes:
                self.candidates.append(self.graph.nodes[i])
            self.graph.pop_first_nodes(self.graph.V_first_nodes)
            self.candidates.append(self.graph.nodes[i])



# algorithim local testing

# algo = LCL(graph=graph)
# algo.find_schedule()
# print(algo.schedule)