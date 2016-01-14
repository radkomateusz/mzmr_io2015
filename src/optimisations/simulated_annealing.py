# coding=utf-8
from random import random, randint
import math
import copy
import time
from datetime import datetime
from parsing.parser import parse
from ranker.goal import evaluate_goal
from randomchanges import RandomChanges


class SimulatedAnnealing:
    STARTING_TEMPERATURE = 1e-2
    MIN_TEMPERATURE = 1e-15
    ALPHA = 0.9998

    def __init__(self, configuration, assignments):
        self.configuration = configuration
        self.current_assignments = assignments
        self.current_cost = self.cost(self.current_assignments)
        self.best_assignments = copy.deepcopy(assignments)
        self.best_cost = self.cost(self.best_assignments)

    def cost(self, assignments):
        value, completness = evaluate_goal(self.configuration, assignments)
        return value

    def generate_next_assignments(self, assignments, temperature):
        depth = randint(1, self.get_max_depth(temperature))
        return RandomChanges.chained(assignments, depth=depth), depth

    def get_max_depth(self, temperature):
        return max(int((temperature * 10000) ** 0.35), 1)

    def acceptance_probability(self, old_cost, new_cost, T):
        try:
            MULT = 1e1
            ap = math.exp(MULT * (new_cost - old_cost) / T)
        except OverflowError:
            ap = 1
        return ap

    def save_if_best_solution(self, new_assignments, new_cost):
        if new_cost > self.best_cost:
            self.best_assignments = copy.deepcopy(new_assignments)
            self.best_cost = new_cost
        pass

    def anneal(self):
        temperature = self.STARTING_TEMPERATURE
        start = time.time()
        iter_num = 1
        with open('annealing_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv', 'a') as file:
            file.write("Alg:\t{0}\n".format('annealing'))
            file.write("Starting temperature: {0}\n".format(str(temperature)))
            file.write("Temperature to stop at: {0}\n".format(str(self.MIN_TEMPERATURE)))
            file.write("Temp. loss factor: {0}\n".format(str(self.ALPHA)))
            file.write("Iteration;\tElapsed (s);\tQuality (-inf,1]\n")

            while temperature > self.MIN_TEMPERATURE:
                new_assignments, depth = self.generate_next_assignments(self.current_assignments, temperature)
                new_assignments = list(new_assignments)
                new_cost = self.cost(new_assignments)

                self.save_if_best_solution(new_assignments, new_cost)

                if self.acceptance_probability(self.current_cost, new_cost, temperature) > random():
                    self.current_assignments = new_assignments
                    self.current_cost = new_cost

                row = "{0};\t{1};\t{2}\n".format(iter_num, time.time() - start, self.current_cost)
                file.write(row)
                if iter_num % 100 == 0:
                    print self.get_max_depth(temperature), '|', row

                temperature *= self.ALPHA
                iter_num += 1

        return self.current_assignments, self.current_cost, self.best_assignments, self.best_cost


configuration, assignments = parse()

annealing_engine = SimulatedAnnealing(configuration, list(assignments))
assignments, current_cost, best_assignments, best_cost = annealing_engine.anneal()

print "Current goal value: " + str(current_cost)
print "Best cost: " + str(best_cost)

# TODO maybe printout the solution
# print "Best solution: " + str(best_assignments)
