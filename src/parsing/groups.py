import re
from common.models import *


def parse_groups(raw_text):
    groups = []
    for line in raw_text.splitlines():
        [subject_id_raw, people_ids_raw] = line.split(':')
        people = [Person(id=int(x)) for x in people_ids_raw.strip().split(',')]
        subject = Subject(id=int(subject_id_raw.strip()))
        groups.append(Group(subject=subject, participants=frozenset(people)))
    return frozenset(groups)
