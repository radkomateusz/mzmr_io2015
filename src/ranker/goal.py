from itertools import groupby


class Context:
    def __init__(self):
        self.capacity_excessions = []
        self.groups_broken = 0
        self.people_with_unassigned = 0
        self.people_count = 0
        self.missing_assignments_count = 0
        self.total_assignments = 0
        self.total_maxes = 0
        self.total_assigned = 0
        self.assigned_impossibilities = 0
        self.people_with_impossibilities = 0


def get_maxes_for_subjects(term_ids_to_points, term_id_to_term):
    pairs = [(term_id_to_term[id].subject.id, points) for id, points in term_ids_to_points.iteritems()]
    return {subject_id: max([x[1] for x in items]) for subject_id, items in groupby(pairs, lambda x: x[0])}


def get_points_for_assigned(assignment, person_preferences):
    return {subject_id: person_preferences.term_ids_to_points.get(term_id, 0) for subject_id, term_id in
            assignment.subject_ids_to_term_ids.iteritems()}


def evaluate_goal(configuration, assignments):
    term_id_to_term = {term.id: term for term in configuration.terms}
    person_id_to_assignments = {assignment.person.id: assignment.subject_ids_to_term_ids for assignment in assignments}
    person_id_to_preferences = {pref.person.id: pref for pref in configuration.preferences}

    person_id_to_subject_to_max = {pref.person.id: get_maxes_for_subjects(pref.term_ids_to_points, term_id_to_term)
                                   for pref in configuration.preferences}

    person_id_to_subject_to_assigned = {assignment.person.id: get_points_for_assigned(
        assignment, person_id_to_preferences[assignment.person.id]
    ) for assignment in assignments}

    context = Context()
    account_person_prefs(context, person_id_to_assignments, person_id_to_preferences, person_id_to_subject_to_assigned,
                         person_id_to_subject_to_max)
    account_groups(configuration, context, person_id_to_assignments)
    account_capacity(assignments, configuration, context)

    # print context.__dict__
    return evaluate_goal_value(context), evaluate_completness(context)


def account_capacity(assignments, configuration, context):
    pairs = [pair for ass in assignments for pair in ass.subject_ids_to_term_ids.items()]
    counts = {term_id: 0 for _, term_id in pairs}
    for _, term_id in pairs:
        counts[term_id] += 1
    for term in configuration.terms:
        if term.capacity < counts.get(term.id, 0):
            # print term.id, '================'
            context.capacity_excessions.append(counts[term.id] - term.capacity)


def account_person_prefs(context, person_id_to_assignments, person_id_to_preferences, person_id_to_subject_to_assigned,
                         person_id_to_subject_to_max):
    for person_id in person_id_to_preferences.keys():
        person_maxes = person_id_to_subject_to_max[person_id]
        person_assigned = person_id_to_subject_to_assigned.get(person_id, {})

        selected_subjects = set(person_maxes.keys())
        unassigned = len(selected_subjects ^ set(person_assigned.keys()))
        context.missing_assignments_count += unassigned
        context.total_assignments += len(selected_subjects)
        context.people_with_unassigned += 1 if unassigned > 0 else 0

        context.total_maxes += sum([points for id, points in person_maxes.iteritems()])
        context.total_assigned += sum([points for id, points in person_assigned.iteritems()])

        impossibilities = sum([1 for term_id in person_id_to_assignments.get(person_id, {}).values()
                               if term_id not in person_id_to_preferences[person_id].term_ids_to_points.keys()])
        context.assigned_impossibilities += impossibilities
        context.people_with_impossibilities += 1 if impossibilities > 0 else 0

        context.people_count += 1


def account_groups(configuration, context, person_id_to_assignments):
    for group in configuration.groups:
        if len({person_id_to_assignments[person.id][group.subject.id] for person in group.participants}) > 1:
            context.groups_broken += 1


def evaluate_goal_value(context):
    impossibilities_factor = float(100 * context.people_with_impossibilities) / context.people_count
    missing_factor = 2. * context.people_with_unassigned / context.people_count
    groups_factor = context.groups_broken / context.people_count
    capacity_factor = sum([float(x * x) for x in context.capacity_excessions]) / context.people_count
    base = float(context.total_assigned) / context.total_maxes
    return base - impossibilities_factor - missing_factor - groups_factor - capacity_factor


def evaluate_completness(context):
    impossibilities_factor = float(context.people_with_impossibilities) / context.people_count
    assigned = context.total_assigned - context.missing_assignments_count
    completness = float(assigned) / context.total_assigned - impossibilities_factor
    return completness * 100
