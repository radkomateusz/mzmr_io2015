import copy
from random import randint, random, sample, shuffle
import itertools


class RandomChanges:
    @staticmethod
    def single(source_assignments):
        assignments = copy.deepcopy(source_assignments)
        RandomChanges.do_single_change(assignments)
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
        common_subjects = set(assignment_first.keys()).intersection(assignment_second.keys())
        if len(common_subjects) > 0:
            subject = sample(common_subjects, 1)[0]
            return RandomChanges.do_change(assignments, first, second, subject)

    @staticmethod
    def do_change(assignments, first, second, subject):
        assignment_first = dict(assignments[first].subject_ids_to_term_ids)
        assignment_second = dict(assignments[second].subject_ids_to_term_ids)

        tmp = assignment_second[subject]
        assignment_second[subject] = assignment_first[subject]
        assignment_first[subject] = tmp

        assignments[first].subject_ids_to_term_ids = assignment_first
        assignments[second].subject_ids_to_term_ids = assignment_second
        return first, second

    def iterate_chained(self, assignments, depth=2):
        people_involved_count = depth + 1

        size = len(assignments)
        combinations = list(itertools.combinations(xrange(size), people_involved_count))
        shuffle(combinations)
        for indices in combinations:
            subjects = [set(assignments[x].subject_ids_to_term_ids.keys()) for x in indices]
            for subject in set.intersection(*subjects):
                terms = [assignments[x].subject_ids_to_term_ids[subject] for x in indices]
                # persons = [assignments[x].person.id for x in indices]

                if len(set(terms)) < people_involved_count:
                    continue

                for x in xrange(1, people_involved_count):
                    RandomChanges.do_change(assignments, indices[0], indices[x], subject)

                yield assignments

                for x in xrange(1, people_involved_count):
                    RandomChanges.do_change(assignments, indices[x - 1], indices[x], subject)

    @staticmethod
    def chained(source_assignments, depth=1):
        assignments = copy.deepcopy(source_assignments)

        first, second = RandomChanges.do_single_change(assignments)

        people_to_avoid = set()
        for i in xrange(depth - 1):
            people_to_avoid.add(first)
            first, second = RandomChanges.do_single_change(assignments, person_to_use=second,
                                                           people_to_avoid=people_to_avoid)

        return assignments
