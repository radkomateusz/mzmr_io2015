import unittest
from common.models import *
from parsing.prefferences import parse_preferences


class TestPeopleAndPreferencesParsing(unittest.TestCase):
    def test_parsing(self):
        preferences = parse_preferences('''
[258668]
global:0:100:0
645277:645373,0;645372,8;
645279:645391,8;645388,0;
[258669]
global:0:100:0
645277:645373,3;645372,5;''')
        self.assertEquals(preferences, frozenset([
            Preference(person=Person(id=258668)),
            Preference(person=Person(id=258669))
        ]))

        points = {preference.person.id: preference.term_ids_to_points for preference in preferences}
        self.assertEquals(points, {
            258668: {645388: 0, 645372: 8, 645373: 0, 645391: 8},
            258669: {645372: 5, 645373: 3}
        })

    if __name__ == '__main__':
        unittest.main()
