import copy
import random
import math
from .algorithm_mutations import Algorithm
from .malus import calculate_malus


class GeneticHillClimber(Algorithm):
    """
    This class creates instances of the Genetic Hill Climbing algorithm. The algorithm works by
    generating n amount of neighbours, which are deepcopy's of the current best timetable
    with x amount of random swaps applied to it. Then the best neighbour is chosen based on 
    the neighbour that has the least malus points. If the best neighbour has a malus score 
    lower then the current best timetable, this neighbour now becomes the new best timetable
    and the next iteration starts. If the best neighbour is not better then the current best 
    timetable, the timetable is not updated and the next iteration of the algorithm starts.
    """
    def __init__(self, timetable):
        super().__init__(timetable)

        self.value = calculate_malus(timetable)
        self.iteration_values = {}
        self.best_iteration = 0


    def generate_individual_neighbour(self, n_swaps):
        """
        This method generates a single neighbour by deepcopying the current 
        best timetable and then aplies n amount of swaps to this deepcopy.
        """
        timetable = copy.deepcopy(self.timetable)
        for i in range(n_swaps):
            self.apply_random_swap(timetable)

        return timetable
    

    def choose_best_neighbour(self, neighbours):
        """
        This method loops over all generated neighbours and calculates their
        malus scores. It then stores the neighbour with the best malus score
        in self.
        """
        # reset neighbours for a new iteration
        self.best_neighbour_value = None
        self.best_neighbour = None

        for neighbour in neighbours:
            neighbour_malus = calculate_malus(neighbour)

            # make the first neighbour always overwrite the best neighbour
            if self.best_neighbour_value == None:
                self.best_neighbour_value = neighbour_malus
                self.best_neighbour = neighbour
            
            if neighbour_malus < self.best_neighbour_value:
                self.best_neighbour_value = neighbour_malus
                self.best_neighbour = neighbour


    def check_solution(self):
        """
        This method checks if the malus score of the best neighbour is lower
        then the current best timetable and if so it assigns the best neighbour
        as the new current best timetable in self and also the associated malus
        score.
        """
        new_value = self.best_neighbour_value
        old_value = copy.deepcopy(self.value)

        if new_value < old_value:
            self.timetable = self.best_neighbour
            self.value = new_value

            return True


    def run(self, neighbours, swaps_per_neighbour, iterations, verbose_alg=False, heuristic=False):
        """
        This method runs the Genetic Hill climber algorithm. It takes in the parameters: 
        - neighbours: the amount of neighbours generated each iteration
        - swaps per neighbour: the amount of swaps applied to each neighbour
        - iterations: the amount of iterations the algorithm runs
        - verbose_alg: if True, prints updates at every iteration.
        - heuristic: if True, lowers the swaps_per_neighbour at every 250 iterations to become more specific.
        """
        self.iterations = iterations
        self.swaps = swaps_per_neighbour

        for iteration in range(iterations):
            neighbour_list = []
            
            # print an update statement every 500 iterations
            if iteration % 500 == 0:
                print(f'Now at iteration {iteration} with {self.value} malus points ')

            if verbose_alg:
                print(f'Iteration {iteration}/{iterations} now running, value of timetable malus points is now {self.value} and amount of swaps is {self.swaps}')
            
            # generate all neighbours and add to the neighbour_list
            for i in range(neighbours):
                neighbour_list.append(self.generate_individual_neighbour(swaps_per_neighbour))
            
            # choose the best neighbour out of the list
            self.choose_best_neighbour(neighbour_list)
            
            if heuristic:
                self.decrease_swaps(iteration)
       
            if self.restart_condition(iteration):
                print('Restart conditions met, now restarting Algorithm.')
                return self.value
            
        return self.value


    def restart_condition(self, iteration):
        """
        This method checks if the stop conditions for restarting an algorithm have
        been met. If so the method returns True and the hill climber loop stops.
        If not the method returns false and the algorithm will keep running.
        """
        improved = self.check_solution()

        self.iteration_values[iteration] = self.value

        # update best_iteration if the value has been improved at current iteration
        if improved:
            self.best_iteration = iteration

        # calculate how long ago a best score was reached
        i_since_last_best = iteration - self.best_iteration
        
        # if the value of the best timetable is not less than 1000 at iteration 10000 the loop stops
        if iteration == 10000 and self.value > 1000:
            return True

        # if there hasnt been an improvement in 1000 iterations the loop stops
        if i_since_last_best == 1000:
            print(f'{iteration} iterations')

            return True
        
        return False
    
              
    def decrease_swaps(self, iteration):
        """
        This method decreases the number of swaps with 1 every 250 iterations.
        However, the swaps minimum number is 2.
        """
        if iteration % 250 == 0 and iteration > 1:
            if self.swaps > 1:
                self.swaps = self.swaps - 1
        