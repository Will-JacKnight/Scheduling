import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from data.graph import DAG


class LCL:
    def __init__(self) -> None:
        self.graph = DAG()
        self.schedule = []
        
        self.total_completion_time = np.sum([self.graph.nodes[i + 1].processing_time for i in range(self.graph.node_num)])
    
    def cost_function(self, j):
        dj = self.graph.nodes[j].due_date
        Cj = self.total_completion_time
        gj_Cj = np.max([0, Cj - dj])

        self.total_completion_time -= self.graph.nodes[j].processing_time
        return gj_Cj
    
    def find_schedule(self):            # main algorithm
        pass

        

algo = LCL()
print(algo.cost_function(31))