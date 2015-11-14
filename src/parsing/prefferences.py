import re
from common.models import *


def parse_preferences(raw_text):
    preferences = set()

    preferences_raw = re.findall(r'\[\d+\].*?(?=\[|\Z)', raw_text, re.DOTALL)
    for preference_raw in preferences_raw:
        [person_id_raw] = re.findall(r'\[(\d+)\]', preference_raw)

        points_raw = [raw.split(',') for raw in re.findall(r'\d+,\d+', preference_raw)]
        term_id_to_points = {int(term_id): int(points) for [term_id, points] in points_raw}

        preference = Preference(person=Person(id=int(person_id_raw)), term_ids_to_points=term_id_to_points)
        preferences.add(preference)

    return frozenset(preferences)
