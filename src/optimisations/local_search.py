# coding=utf-8
from random import random, randint
import math
import copy
from datetime import datetime

from optimisations.onlybetterchangesiterator import OnlyBetterChangesIterator
from parsing.parser import parse
from ranker.goal import evaluate_goal
from randomchanges import RandomChanges


class LocalSearch:
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

    def find_next_solution_via_full_search(self, assignments, depth):
        result = assignments
        result_delta = -1
        iterator = OnlyBetterChangesIterator(self.configuration, assignments)

        for assignments, delta in iterator.next_change(assignments, depth=3):
            if delta > result_delta:
                result_delta = delta
                result = copy.deepcopy(assignments)
        return result

    def find_next_solution(self, assignments, depth):
        iterator = OnlyBetterChangesIterator(self.configuration, assignments)

        for assignments, delta in iterator.next_change(assignments, depth=2):
            if delta > 0:
                return assignments

        for assignments, delta in iterator.next_change(assignments, depth=3):
            if delta > 0:
                return assignments

        for assignments, delta in iterator.next_change(assignments, depth=4):
            if delta > 0:
                return assignments

        return None

    def save_if_best_solution(self, new_assignments, new_cost):
        if new_cost > self.best_cost:
            self.best_assignments = copy.deepcopy(new_assignments)
            self.best_cost = new_cost
        pass

    def search(self):
        depth = 2
        iter_num = 1
        with open('local_search_results_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv', 'a') as file:
            file.write(
                "\n\n Goal function values:\n")

            while True:
                new_assignments = self.find_next_solution(self.current_assignments, depth)
                if new_assignments is None:
                    break
                new_cost = self.cost(new_assignments)

                self.save_if_best_solution(new_assignments, new_cost)
                self.current_assignments = copy.deepcopy(new_assignments)
                self.current_cost = new_cost

                print("{0};\t{1}\n".format(iter_num, self.current_cost))
                file.write("{0};\t{1}\n".format(iter_num, self.current_cost))
                iter_num += 1

        return self.current_assignments, self.current_cost, self.best_assignments, self.best_cost


configuration, assignments = parse()

optimiser = LocalSearch(configuration, list(assignments))
assignments, current_cost, best_assignments, best_cost = optimiser.search()

print "Current goal value: " + str(current_cost)
print "Best cost: " + str(best_cost)
