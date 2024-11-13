import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from data.graph import DAG


class LCL:
    '''
    Apply Least Cost Last (LCL) algorithm on a Directed Acyclic Graph (DAG).

    Args:
        graph (DAG): DAG to be optimized on.
    '''
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
            self.graph.pop_node(self.graph.V[min_index], node_type="last")                      # pop out the node with least cost

            if (printEachIteration):
                # print("-----------------------------------------------------")
                print(f"In iteration {self.iteration}: ")
                print(f"partial schedule S = {[int(self.schedule[i]) for i in range(len(self.schedule))]}")


class TabuSearch:
    '''
    Apply Tabu Search algorithm on a Directed Acyclic Graph (DAG).

    Args:
        graph (DAG): DAG to be optimized on.
    '''
    def __init__(self, graph) -> None:
        self.graph = graph

    # def generate_initial_candidates(self):          # need to take into account the DAG graph order
    #     # get V, pop oout rando
        
    #     for i in range(self.graph.node_num):
    #         if self.graph.V_first_nodes:
    #             self.candidates.append(self.graph.nodes[i])
    #         self.graph.pop_first_nodes(self.graph.V_first_nodes)
    #         self.candidates.append(self.graph.nodes[i])


    def minimizer(self, L: int, K: int, gamma: int, initial_schedule: list):
        '''
        Apply tabu search with initialized parameters to minimize total tardiness.

        Args:
            L (int): Length of tabu list.
            K (int): Amount of solutions found (initial solution is 0).
            gamma (int): Tolerance from g_best to accept solution. 
            initial_schedule (list): Schedule to be optimized on.
        '''

        # set values of tabu search
        self.L = L
        self.K = K
        self.gamma = gamma
        self.schedule = initial_schedule.copy()

        # get index where last solution was found (-1 as cycles start at i + 1)
        solution_found_index = -1
        # tracker of amount of solutions found 
        K_solutions = 0
        # empty tabu list
        tabu_list = []

        # calculate initial solution
        g_best = self.total_tardiness()
        best_solution = self.schedule.copy()
        print(f"The initial solution S = {best_solution} has a total tardiness of {g_best}")

        # infinite loop stopped when K iterations reached or no better solution found in some iteration
        while K_solutions < self.K:
            # track if solution found in current cycle
            found_solution_in_cycle = False

            # iterate from last position where solution was found
            for i in range(solution_found_index + 1, solution_found_index + 1 + self.graph.node_num - 1):
                # restrict indices to possible indices of list
                current_index = i % (self.graph.node_num - 1)
                
                # define swap pair
                swap_pair = (current_index, current_index + 1)

                # check if swap pair in tabu list
                if swap_pair in tabu_list:
                    continue

                # swap two neighbouring nodes
                self.schedule[current_index], self.schedule[current_index + 1] = self.schedule[current_index + 1], self.schedule[current_index]

                # check if new schedule valid
                if self.check_validity():
                    # calculate tardiness of current schedule
                    current_tardiness = self.total_tardiness()

                    # accept solution if it is less than g_best plus tolerance
                    if current_tardiness <= g_best + self.gamma:
                        if current_tardiness < g_best:
                            g_best = current_tardiness
                            best_solution = self.schedule.copy()
                            print(f"Improved solution found with total tardiness = {g_best} (current K={K_solutions + 1})")
                        
                        # update where last solution was found
                        solution_found_index = current_index
                        found_solution_in_cycle = True

                        # add swap pair to tabu list and remove the oldest entry if the list is too long
                        tabu_list.append(swap_pair)
                        if len(tabu_list) > self.L:
                            tabu_list.pop(0)

                        # increment amount of solutions found and start new cycle
                        K_solutions += 1
                        break
                    
                    else:
                        # revert swap if not accepted as a solution
                        self.schedule[current_index], self.schedule[current_index + 1] = self.schedule[current_index + 1], self.schedule[current_index]

                else:
                    # revert swap if not accepted as a solution
                    self.schedule[current_index], self.schedule[current_index + 1] = self.schedule[current_index + 1], self.schedule[current_index]

            # terminate search if no solution found in one cycle
            if not found_solution_in_cycle:
                print(f"\nNo further improvements found. Terminated search at K = {K_solutions}.")
                print(f"Best solution: S = {best_solution}")
                print(f"Total Tardiness = {g_best}\n")
                return

        print(f"Terminated search at K = {K_solutions}.") 
        print(f"Best solution found: S = {best_solution}")
        print(f"Total Tardiness of {g_best}\n")
        return


    def check_validity(self):
        '''
        Check if the current schedule is valid based on DAG dependencies in adjecency matrix.
        '''
        # keep track of already scheduled jobs
        scheduled_set = set()

        for scheduled_node in self.schedule:
            # add current node to schedule
            scheduled_set.add(scheduled_node)

            # check if all predecessors are already scheduled
            for pred_node in range(self.graph.node_num):
                # substract one to scheduled_node to convert to 0 indexing 
                # add one to pred_node to convert to 1 indexing
                if self.graph.G_matrix[pred_node][scheduled_node - 1] == 1 and pred_node + 1 not in scheduled_set:
                    return False
        
        return True
    

    def total_tardiness(self):
        '''
        Calculate the total tardiness for the current schedule.
        '''
        # cumulative processing time as we process each node
        total_processing_time = 0
        # accumulated tardiness
        total_tardiness = 0
        
        # Iterate over each node in the schedule
        for scheduled_node in self.schedule:
            node = self.graph.nodes[scheduled_node - 1]
            total_processing_time += node.processing_time
            
            # calculate tardiness of current node and add to total
            tardiness = max(node.due_date - total_processing_time, 0)
            total_tardiness += tardiness

        return total_tardiness