import copy
from random import randint, random, choice, sample


class Changes:
    @staticmethod
    def single(source_assignments):
        assignments = copy.deepcopy(source_assignments)
        Changes.do_single_change(assignments)
        return assignments

    @staticmethod
    def do_single_change(assignments, person_to_use=None, people_to_avoid=None):
        size = len(assignments)

        if not person_to_use:
            person_to_use = randint(0, size - 1)
        if not people_to_avoid:
            people_to_avoid = set()

        first = person_to_use
        possible_changes = set(range(0, size - 1))
        people_to_avoid.add(first)
        possible_changes -= people_to_avoid

        second = sample(possible_changes, 1)[0] if len(possible_changes) > 0 else first

        assignment_first = dict(assignments[first].subject_ids_to_term_ids)
        assignment_second = dict(assignments[second].subject_ids_to_term_ids)
        for key in assignment_first:
            if key in assignment_second:
                if random() > 0.5:
                    tmp = assignment_second[key]
                    assignment_second[key] = assignment_first[key]
                    assignment_first[key] = tmp
        assignments[first].subject_ids_to_term_ids = assignment_first
        assignments[second].subject_ids_to_term_ids = assignment_second

        return first, second

    @staticmethod
    def chained(source_assignments, depth=1):
        assignments = copy.deepcopy(source_assignments)

        first, second = Changes.do_single_change(assignments)

        people_to_avoid = set()
        for i in xrange(depth - 1):
            people_to_avoid.add(first)
            first, second = Changes.do_single_change(assignments, person_to_use=second, people_to_avoid=people_to_avoid)

        return assignments
