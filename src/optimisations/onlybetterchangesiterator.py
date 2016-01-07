import copy
from random import randint, random, sample

import itertools

from ranker.goal import evaluate_goal


class PersonContext:
    def __init__(self):
        pass


class OnlyBetterChangesIterator:
    def __init__(self, configuration, initial_assignments):
        self.preferences = configuration.preferences
        self.configuration = configuration

        self.term_id_to_term = {term.id: term for term in configuration.terms}
        self.term_ids = self.term_id_to_term.keys()
        self.term_id_to_subject_id = {term.id: term.subject.id for term in configuration.terms}

        self.person_to_assignments = {ass.person.id: ass.subject_ids_to_term_ids for ass in initial_assignments}

        self.person_context = {}
        for preference in self.preferences:
            context = PersonContext()
            person_id = preference.person.id

            self.person_context[person_id] = context

            context.impossibilities = {term_id for term_id in self.term_ids if
                                       term_id not in preference.term_ids_to_points.keys()}

            context.points = preference.term_ids_to_points

            context.assigned = set(self.person_to_assignments[person_id].values())

            context.groups = {}
            for term in configuration.terms:
                groups = [g for g in configuration.groups if
                          person_id in [p.id for p in g.participants] and g.subject.id == term.subject.id]
                if len(groups) > 0:
                    context.groups[term.id] = frozenset([p.id for p in groups[0].participants])

            context.maxes = {}
            for term_id in self.term_ids:
                subject = self.term_id_to_term[term_id].subject
                points = preference.term_ids_to_points.get(term_id, -1)
                context.maxes[subject.id] = max(points, context.maxes.get(subject.id, -1))

        self.capacity_left = {term.id: term.capacity for term in configuration.terms}
        for assignment in initial_assignments:
            for term_id in assignment.subject_ids_to_term_ids.values():
                self.capacity_left[term_id] -= 1

    def evaluate_change(self, person, src, dst):
        context = self.person_context[person]

        capacity_exceded = self.capacity_left[dst] < 1
        impossibility = dst in context.impossibilities
        collision = False

        collisions = self.term_id_to_term[dst].collisions
        for term_id in context.assigned:
            if self.term_id_to_term[term_id] in collisions:
                collision = True
                break

        subject_max = context.maxes[self.term_id_to_term[dst].subject.id]
        dst_ = context.points.get(dst, -1)
        src_ = context.points.get(src, -1)
        scaled_points_delta = float(dst_ - src_) / subject_max

        applicable = not (capacity_exceded or impossibility or collision)
        return applicable, scaled_points_delta

    def update_on_change(self, person, src, dst):
        self.capacity_left[src] += 1
        self.capacity_left[dst] -= 1
        self.person_context[person].assigned.remove(src)
        self.person_context[person].assigned.add(dst)

    def next_change(self, assignments, depth=3):
        size = len(assignments)
        for indices in itertools.combinations(xrange(size), depth):
            subjects = [set(assignments[x].subject_ids_to_term_ids.keys()) for x in indices]
            for subject in set.intersection(*subjects):
                terms = [assignments[x].subject_ids_to_term_ids[subject] for x in indices]
                persons = [assignments[x].person.id for x in indices]

                if len(set(terms)) < depth:
                    continue

                applicable = True
                scaled_delta_total = 0

                for x in xrange(depth):
                    next_x = (x + 1) % depth
                    tmp_applicable, tmp_scaled_delta = self.evaluate_change(persons[x], terms[x], terms[next_x])
                    applicable = applicable and tmp_applicable
                    scaled_delta_total += tmp_scaled_delta

                if applicable and scaled_delta_total > 0:

                    for x in xrange(depth):
                        next_x = (x + 1) % depth
                        self.update_on_change(persons[x], terms[x], terms[next_x])

                    for x in xrange(1, depth):
                        OnlyBetterChangesIterator.swap_people(assignments, indices[0], indices[x], subject)

                    yield assignments, scaled_delta_total

                    for x in xrange(depth):
                        next_x = (x + 1) % depth
                        self.update_on_change(persons[x], terms[next_x], terms[x])

                    for x in xrange(1, depth):
                        OnlyBetterChangesIterator.swap_people(assignments, indices[x - 1], indices[x], subject)

    @staticmethod
    def swap_people_back(assignments, first, second, subject):
        OnlyBetterChangesIterator.swap_people(assignments, second, first, subject)

    @staticmethod
    def swap_people(assignments, first, second, subject):
        assignment_first = assignments[first].subject_ids_to_term_ids
        assignment_second = assignments[second].subject_ids_to_term_ids

        tmp = assignment_second[subject]
        assignment_second[subject] = assignment_first[subject]
        assignment_first[subject] = tmp
