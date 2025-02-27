import random
import math

from .hill_climber import HillClimber
from .malus import calculate_malus


class SimulatedAnnealing(HillClimber):
    """
    The SimulatedAnnealing class performs a random change to the timetable, just as in HillClimber.
    Most of the functions are similar to those of the HillClimber class, which is why
    we use that as a parent class.

    Each improvement or equivalent solution is kept for the next iteration.
    Also sometimes accepts solutions that are worse, depending on the current temperature.
    """
    def __init__(self, timetable, temperature=1):

        # use the init of the Hillclimber class for the timetable
        super().__init__(timetable)

        # starting temperature and current temperature
        self.T0 = temperature
        self.T = temperature

        
    def update_temperature(self):
        """
        This method implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.
        """
        self.T = self.T - (self.T0 / self.iterations)

    def check_solution(self, new_timetable):
        """
        This method checks and accepts better solutions than the current solution.
        Also sometimes accepts solutions that are worse, depending on the current
        temperature.
        """
        new_value = calculate_malus(new_timetable)
        old_value = self.value
        
        # calculate the probability of accepting this new timetable
        delta = new_value - old_value

        # with negative delta (so an improvement) prob is always more than 1 so always larger than random.random()
        prob_before_exp = -delta / self.T

        # cap to prevent math range error
        if prob_before_exp > 1:
            prob_before_exp = 1

        # cap to prevent math range error as -709 is the minimum value my calculator was still able to give a result
        if prob_before_exp < -709:
            prob_before_exp = -709

        probability = math.exp(prob_before_exp)

        # update the temperature
        self.update_temperature()

        # pull a random number between 0 and 1 and see if we accept the timetable!
        if random.random() < probability:
            self.timetable = new_timetable
            self.value = new_value
            
            if new_value < old_value:
                return True

        

        

        

        