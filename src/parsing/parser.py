from parsing.assignments import parse_assignments
from parsing.groups import parse_groups
from parsing.prefferences import parse_preferences
from parsing.terms import parse_subjects_and_terms


class Configuration:
    def __init__(self, preferences=set(), groups=set(), subjects=set(), terms=set()):
        self.subjects = subjects
        self.groups = groups
        self.preferences = preferences
        self.terms = terms


def parse(pref_fname="preferences.txt", groups_fname="groups.txt", terms_fname="terms.txt", assign_fname="output.txt"):
    preferences = parse_preferences(open(pref_fname).read())
    assignments = parse_assignments(open(assign_fname).read())
    groups = parse_groups(open(groups_fname).read())
    subjects, terms = parse_subjects_and_terms(open(terms_fname).read())

    return Configuration(preferences, groups, subjects, terms), assignments
