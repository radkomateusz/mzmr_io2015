from random import random
from random import randint
import math
from parsing.parser import parse
from ranker.goal import evaluate_goal

LIMIT = 100000


def cost(configuration, assignments):
    value, completness = evaluate_goal(configuration, assignments)
    return value


def neighbor(configuration, assignments):
    size = len(assignments)

    i = j = randint(0, size - 1)
    while i == j:
        j = randint(0, size - 1)

    assignmentOne = dict(assignments[i].subject_ids_to_term_ids)
    assigmentTwo = dict(assignments[j].subject_ids_to_term_ids)

    for key in assignmentOne.iterkeys():
        if assigmentTwo.has_key(key):
            if random() > 0.5:
                tmp = assigmentTwo[key]
                assigmentTwo[key] = assignmentOne[key]
                assignmentOne[key] = tmp

    assignments[i].subject_ids_to_term_ids = assignmentOne
    assignments[j].subject_ids_to_term_ids = assigmentTwo

    return configuration, assignments


def acceptance_probability(old_cost, new_cost, T):
    # print "newcost: ",new_cost
    # print "oldcost: ",old_cost
    # print "ap: ", math.exp((new_cost - old_cost)/T)
    return math.exp((new_cost - old_cost)/T)


def anneal(configuration, assignments):
    old_cost = cost(configuration, assignments)
    best_assigments = assignments
    best_cost = old_cost
    T = 100
    T_min = 0.0001
    alpha = 0.99
    while T > T_min:
        configuration, new_assignments = neighbor(configuration, assignments)
        new_cost = cost(configuration, new_assignments)

        if new_cost > best_cost:
            best_assigments = new_assignments
            best_cost = new_cost
        if acceptance_probability(old_cost, new_cost, T) > random():
            assignments = new_assignments
            old_cost = new_cost

        print T , " , ",  old_cost
        T = T * alpha
    return configuration, assignments, old_cost, best_cost, best_assigments


configuration, assignments = parse()
assignments = list(assignments)

configuration, assignments, cost, best_cost, best_assigments = anneal(configuration, assignments)

print "\nRESULTS:\n"
print cost
print "\nBest cost: "
print best_cost
