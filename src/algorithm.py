import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from graph import DAG


class LCL:
    '''
    Apply Least Cost Last (LCL) algorithm on a Directed Acyclic Graph (DAG).

    Args:
        graph (DAG): DAG to be optimized on.
    '''
    def __init__(self, graph: DAG):
        self.graph = graph
        # initialize with empty schedule
        self.schedule = []
        # initialize with total completion time
        self.completion_time_j = np.sum([self.graph.nodes[i].processing_time for i in range(self.graph.node_num)])
        self.iteration = 0
        self.g_max_list = []

    def cost_function(self, j: int):
        '''
        Calculate cost for a given job, the cost function is defined as tardiness.

        Args:
            j (int): Index of job.
        '''
        dj = self.graph.nodes[j].due_date
        Cj = self.completion_time_j
        # definition of tardiness
        gj_Cj = np.max([0, Cj - dj])

        self.completion_time_j -= self.graph.nodes[j].processing_time
        return gj_Cj
    

    def find_schedule(self, verbose: bool=False):
        '''
        Apply LCL algorithm to minimize g*max.

        Note: Printouts are 1 indexed while internal calculations are based on 0 indexing.
        
        Args:
            verbose (bool): Optional, set True to print iteration results. Default is False.
        '''
        for self.iteration in range(self.graph.node_num):
            # store original G_matrix and set V as these values will be modified in DAG instance
            G_matrix_copy = self.graph.G_matrix.copy()
            V_copy = self.graph.V.copy()
            
            # calculate and store all last jobs' cost inside gj_list
            gj_list = [self.cost_function(node_index) for node_index in self.graph.V]
            # get index of the job in within V set with the least cost
            min_index = np.argmin(gj_list)
            # calculate gl(Cl) and put it into g_max_list
            # convert to actual job index by indexing set V
            self.g_max_list.append(gj_list[min_index])
            # convert from 0 indexing to 1 indexing to get original node number
            # add node to the front of schedule (schedule in a reversed order)
            self.schedule = np.insert(self.schedule, 0, self.graph.V[min_index] + 1)
            # pop out the node with the least cost
            self.graph.pop_node(self.graph.V[min_index])
            
            # print intermediate iteration schedule
            if (verbose):
                iteration_type = "final" if self.iteration == self.graph.node_num - 1 else "partial"
                schedule_list = [int(node) for node in self.schedule]
                print(f"In iteration {self.iteration + 1}: ")
                print(f"{iteration_type} schedule S = {schedule_list}\n")

        # print the optimal schedule
        print("\nThe optimal schedule for 1|prec|g*max problem is:")
        print(f"S = {[int(self.schedule[i]) for i in range(self.graph.node_num)]}")
        print(f"where g*max = {max(self.g_max_list)}\n")
        
        # restore original values in DAG instance
        self.graph.G_matrix = G_matrix_copy
        self.graph.V = V_copy    


class TabuSearch:
    '''
    Apply Tabu Search algorithm on a Directed Acyclic Graph (DAG).

    Args:
        graph (DAG): DAG to be optimized on.
    '''
    def __init__(self, graph: DAG):
        self.graph = graph

    def find_schedule(self, L: int, K: int, gamma: int, initial_schedule: list=None, generate_initial_schedule: bool=True, aspiration_criterion: bool=False, verbose: bool=False):
        '''
        Apply tabu search with initialized parameters to minimize total tardiness.
        
        Note: User input and printouts are 1 indexed while internal calculations are based on 0 indexing.

        Args:
            L (int): Length of tabu list.
            K (int): Maximum number of iterations / solutions (initial solution is k=0).
            gamma (int): Tolerance from g_best to accept solution. 
            initial_schedule (list): Optional, force initial solution to this schedule (1 indexed). Default is None.
            generate_initial_schedule (bool): Creates an initial solution considering precedence constraints. 
                                              initial_schedule takes precedence before random_initial_solution. Default is True.
            aspiration_criterion (bool): Optional aspiration criterion that accepts solution included in tabu list if it improves g_best. Default is False.
            verbose (bool): Optional, set True to print intermediate results when accepted solution improved g_best. Default is False.
        '''

        # set values of tabu search
        self.L = L
        self.K = K
        self.gamma = gamma
        
        if initial_schedule is not None:
            # take initial schedule and convert to 0 indexing as user input in 1 indexed
            self.schedule = [x - 1 for x in initial_schedule]
            # check initial schedule for validity
            if self.check_validity() == False:
                raise ValueError("Initial solution does not meet precedence constraints. Provide a valid initial solution.")
        elif generate_initial_schedule == True:
            adjacency_matrix = self.graph.G_matrix.copy()
            self.schedule = []
            while len(self.schedule) < self.graph.node_num:
                # schedule ready nodes with no precedences
                for col in range(self.graph.node_num):
                    if np.sum(adjacency_matrix[:, col]) == 0 and col not in self.schedule:
                        self.schedule.append(col)
                # remove these from the adjacency matrix
                for scheduled_node in self.schedule:
                    adjacency_matrix[scheduled_node, :] = 0
        
        # index where new cycle starts
        new_cycle_index = 0
        # tracker of amount of solutions found 
        k = 0
        # empty tabu list
        tabu_list = []

        # calculate initial solution
        g_best = self.total_tardiness()
        best_solution = self.schedule.copy()
        # have 1 indexed printed solution
        print_solution = [x + 1 for x in best_solution]
        print(f"The initial solution S = {print_solution} has a total tardiness of {g_best}")

        # infinite loop stopped when K solutions found or no better solution found in one complete cycle
        while k < self.K:
            # track if solution found in current cycle
            found_solution_in_cycle = False

            # iterate from last position where solution was found
            for i in range(new_cycle_index, new_cycle_index + self.graph.node_num - 1):
                # restrict indices to possible indices of list using modulo
                current_index = i % (self.graph.node_num - 1)
                
                # define swap pair and sort them
                swap_pair = (self.schedule[current_index], self.schedule[current_index + 1])
                swap_pair = tuple(sorted(swap_pair))

                # swap two neighbouring nodes
                self.schedule[current_index], self.schedule[current_index + 1] = self.schedule[current_index + 1], self.schedule[current_index]

                # check validity of solution and skip current iteration if not valid
                if self.check_validity() == False:
                    # swap back
                    self.schedule[current_index], self.schedule[current_index + 1] = self.schedule[current_index + 1], self.schedule[current_index]        
                    continue
                
                # calculate tardiness of current schedule
                current_tardiness = self.total_tardiness()
                
                # calculate delta of current schedule
                delta = g_best - current_tardiness
                
                # accept solution if delta is higher than -gamma and not from tabu list
                # if aspiration_criterion is set to true also check this criterion (one of both criterion to accept solution)
                if (delta > (- self.gamma) and (swap_pair not in tabu_list)) or (aspiration_criterion==True and current_tardiness < g_best):
                    found_solution_in_cycle = True
                    
                    # save solution if better than current g_best
                    if current_tardiness < g_best: 
                        g_best = current_tardiness
                        best_solution = self.schedule.copy()
                        if verbose:
                            print(f"Improved solution found with total tardiness = {g_best} (current k = {k+1})")
                    
                    # update where new cycle should start
                    new_cycle_index = current_index + 1
                    
                    # add swap pair to tabu list and remove the oldest entry if the list is too long
                    tabu_list.append(swap_pair)
                    if len(tabu_list) > self.L:
                        tabu_list.pop(0)
                        
                    # increment amount of solutions found and start new cycle
                    k += 1
                    break
                    
                else:
                    # revert swap if not accepted as a solution
                    self.schedule[current_index], self.schedule[current_index + 1] = self.schedule[current_index + 1], self.schedule[current_index]
                    
            # terminate search if no solution found in one cycle
            if not found_solution_in_cycle:
                # have 1 indexed printed solution
                print_solution = [x + 1 for x in best_solution]
                print(f"\nNo further improvements found. Terminated search at k = {k}.")
                print(f"Best solution: S = {print_solution}")
                print(f"Total Tardiness = {g_best}\n")
                return

        # have 1 indexed printed solution
        print_solution = [x + 1 for x in best_solution]
        print(f"\nTerminated search at k = {k}.") 
        print(f"Best solution found: S = {print_solution}")
        print(f"Total Tardiness of {g_best}\n")
        return


    def check_validity(self):
        '''
        Check if the current schedule is valid based on DAG dependencies in adjacency matrix.
        '''
        # keep track of already scheduled jobs
        scheduled_set = set()

        for scheduled_node in self.schedule:
            # add current node to schedule
            scheduled_set.add(scheduled_node)

            # check if all predecessors are already scheduled
            for pred_node in range(self.graph.node_num):
                if self.graph.G_matrix[pred_node, scheduled_node] == 1 and pred_node not in scheduled_set:
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
            node = self.graph.nodes[scheduled_node]
            total_processing_time += node.processing_time
            
            # calculate tardiness of current node and add to total
            tardiness = max(node.due_date - total_processing_time, 0)
            total_tardiness += tardiness

        return total_tardiness