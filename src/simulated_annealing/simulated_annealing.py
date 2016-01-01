from random import random
from random import randint
import math
import copy
from datetime import datetime
from parsing.parser import parse
from ranker.goal import evaluate_goal


class SimulatedAnnealing:
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

    def generate_next_assignments(self, assignments):
        assignments = copy.deepcopy(assignments)

        size = len(assignments)
        i = j = randint(0, size - 1)
        while i == j:
            j = randint(0, size - 1)

        self.swap_common_subjects_for_given_persons(assignments, i, j)

        return assignments

    def swap_common_subjects_for_given_persons(self, assignments, i, j):
        assignment_first = dict(assignments[i].subject_ids_to_term_ids)
        assignment_second = dict(assignments[j].subject_ids_to_term_ids)
        for key in assignment_first:
            if key in assignment_second:
                if random() > 0.5:  # todo: co to robi?
                    tmp = assignment_second[key]
                    assignment_second[key] = assignment_first[key]
                    assignment_first[key] = tmp
        assignments[i].subject_ids_to_term_ids = assignment_first
        assignments[j].subject_ids_to_term_ids = assignment_second
        pass

    def acceptance_probability(self, old_cost, new_cost, T):
        # print "newcost: ",new_cost
        # print "oldcost: ",old_cost
        # print "ap: ", math.exp((new_cost - old_cost)/T)
        try:
            ap = math.exp(1000 * (new_cost - old_cost) / T)
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
        alpha = 0.999

        with open('results_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv', 'a') as file:
            file.write(
                "Starting temperature: " + str(temperature) +
                "\nTemperature to stop at: " + str(self.MIN_TEMPERATURE) +
                "\nalpha: " + str(alpha) +
                "\n\n Goal function values:\n")

            while temperature > self.MIN_TEMPERATURE:
                new_assignments = self.generate_next_assignments(self.current_assignments)
                new_cost = self.cost(new_assignments)

                self.save_if_best_solution(new_assignments, new_cost)

                if self.acceptance_probability(self.current_cost, new_cost, temperature) > random():
                    self.current_assignments = new_assignments
                    self.current_cost = new_cost

                file.write("{0}\n".format(self.current_cost))
                temperature *= alpha

        return self.current_assignments, self.current_cost, self.best_assignments, self.best_cost


configuration, assignments = parse()

annealing_engine = SimulatedAnnealing(configuration, list(assignments))
assignments, current_cost, best_assignments, best_cost = annealing_engine.anneal()

print "Current goal value: " + str(current_cost)
print "Best cost: " + str(best_cost)

# TODO maybe printout the solution
# print "Best solution: " + str(best_assignments)
