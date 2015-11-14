from itertools import groupby
import re
from common.models import *


def parse_collisions(raw_text):
    [all_collisions_raw] = re.findall(r'(?<=\[kolizje\]).*', raw_text, re.DOTALL)
    collisions_raw = re.findall(r'\d+,\d+;\d+,\d+', all_collisions_raw)
    collisions = [re.findall(r'(?<=,)\d+', x) for x in collisions_raw]
    return {int(key): {int(item[1]) for item in group} for key, group in groupby(collisions, lambda x: x[0])}


def parse_subjects_and_terms(raw_text):
    subjects = set()
    terms = dict()

    subjects_raw = re.findall(r'\[\d+\].*?(?=\[|\Z)', raw_text, re.DOTALL)
    for subject_raw in subjects_raw:
        subject_id_raw = re.findall(r'\[(\d+)\]', subject_raw, re.DOTALL)
        subject = Subject(id=int(subject_id_raw[0]))
        subjects.add(subject)

        terms_raw = re.findall(r'^\d+:\d+', subject_raw, re.DOTALL | re.MULTILINE)
        for [id_raw, capacity_raw] in [x.split(':') for x in terms_raw]:
            term = Term(id=int(id_raw), capacity=int(capacity_raw), subject=subject)
            terms[term.id] = term

    collisions = parse_collisions(raw_text)
    for term in terms.values():
        term_collisions = [terms[id] for id in collisions.get(term.id, {})]
        term.collisions = frozenset(term_collisions)

    return frozenset(subjects), frozenset(terms.values())
