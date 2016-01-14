# coding=utf-8
from datetime import datetime
import copy
import time

from parsing.parser import parse
from ranker.goal import evaluate_goal
from randomchanges import RandomChanges


class GreedyLocalSearch:
    STARTING_TEMPERATURE = 100
    MIN_TEMPERATURE = 1e-10

    def __init__(self, configuration, assignments):
        self.configuration = configuration
        self.current_assignments = assignments
        self.current_cost = self.cost(self.current_assignments)
        self.best_assignments = copy.deepcopy(assignments)
        self.best_cost = self.cost(self.best_assignments)

    def cost(self, assignments):
        value, completness = evaluate_goal(self.configuration, assignments)
        return value

    def save_if_best_solution(self, new_assignments, new_cost):
        if new_cost > self.best_cost:
            self.best_assignments = copy.deepcopy(new_assignments)
            self.best_cost = new_cost
        pass

    def run(self):
        depth = 2
        iter_num = 1
        start = time.time()
        with open('results_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv', 'a') as file:
            file.write("Alg:\t{0}\n".format('greedy_randomized'))
            file.write("Depth:\t{0}\n\n".format(depth))
            file.write("Iteration;\tElapsed (s);\tQuality (-inf,1]\n")

            while True:
                changes_found = False
                generator = RandomChanges()
                for new_assignments in generator.iterate_chained(self.current_assignments, depth=depth):
                    new_cost = self.cost(new_assignments)

                    self.save_if_best_solution(new_assignments, new_cost)

                    if self.current_cost < new_cost:
                        self.current_assignments = new_assignments
                        self.current_cost = new_cost

                        changes_found = True
                        break

                file.write("{0};\t\t\t{1};\t{2}\n".format(iter_num, time.time() - start, self.current_cost))
                iter_num += 1

                if not changes_found:
                    break

        return self.current_assignments, self.current_cost, self.best_assignments, self.best_cost


configuration, assignments = parse()

annealing_engine = GreedyLocalSearch(configuration, list(assignments))
assignments, current_cost, best_assignments, best_cost = annealing_engine.run()

print "Current goal value: " + str(current_cost)
print "Best cost: " + str(best_cost)
