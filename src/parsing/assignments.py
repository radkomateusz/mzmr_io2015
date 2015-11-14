import re
from common.models import *


def parse_assignments(raw_text):
    assignments = []

    assignments_raw = re.findall(r'\[\d+\].*?(?=\[|\Z)', raw_text, re.DOTALL)
    for assignment_raw in assignments_raw:
        [person_id_raw] = re.findall(r'\[(\d+)\]', assignment_raw)

        pairs_raw = [raw.split(':') for raw in re.findall(r'\d+:\d+', assignment_raw)]
        mapping = {int(subject_id): int(term_id) for [subject_id, term_id] in pairs_raw}

        assignment = Assignment(person=Person(id=int(person_id_raw)), subject_ids_to_term_ids=mapping)
        assignments.append(assignment)

    return frozenset(assignments)
